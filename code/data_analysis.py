from __future__ import annotations

import difflib
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Union

import pandas as pd

# ----------------------------------------------------------------------------
# Display / logging settings
# ----------------------------------------------------------------------------
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Configuration for the analysis."""

    # CPI factor used to express 2018 salary in 2020 dollars.
    cpi_2018_to_2020: float = 1.027

    # Regex used for the deep-dive filter.
    targets_regex: str = r"Engineering|Nursing|Tourism"

    # Excel files are referenced relative to repository root.
    file_2018: Path = Path("data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx")
    file_2020: Path = Path("data/raw/GOS-2020-National-Tables.xlsx")

    output_csv: Path = Path("data/clean/final_pandemic_research_data.csv")


def _repo_root() -> Path:
    """Return the repository root assuming this file lives in code/."""
    # code/data_analysis.py -> parents[1] is repo root
    return Path(__file__).resolve().parents[1]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip and collapse internal whitespace in all column names."""
    df.columns = [re.sub(r"\s+", " ", str(c).strip()) for c in df.columns]
    return df


def load_and_standardize(
    file_path: Path,
    possible_sheets: Sequence[str],
    value_col: Union[str, Sequence[str]],
    new_value_name: str,
    *,
    skiprows: int = 1,
) -> pd.DataFrame:
    """Load a sheet, standardize the first column as Study_Area, and coerce numeric values.

    ``value_col`` may be a single column name or a list/tuple of acceptable
    alternatives; the first match found in the sheet is used.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    xls = pd.ExcelFile(file_path)
    target_sheet = next((s for s in possible_sheets if s in xls.sheet_names), None)

    if not target_sheet:
        raise ValueError(
            f"Could not find any of sheets {list(possible_sheets)} in {file_path}. "
            f"Available sheets: {xls.sheet_names}"
        )

    df = pd.read_excel(file_path, sheet_name=target_sheet, skiprows=skiprows)
    if df.empty:
        raise ValueError(f"Loaded empty sheet '{target_sheet}' from {file_path}")

    # Normalize column names so minor whitespace variations don't cause mismatches.
    df = _normalize_columns(df)

    # Resolve value_col: accept a single string or a list/tuple of candidates.
    candidates: list[str] = [value_col] if isinstance(value_col, str) else list(value_col)
    found_col = next((c for c in candidates if c in df.columns), None)

    if found_col is None:
        # Use all candidates as sources for close-match suggestions.
        all_cols = df.columns.tolist()
        close: list[str] = []
        for cand in candidates:
            close.extend(difflib.get_close_matches(cand, all_cols, n=3, cutoff=0.5))
        # Deduplicate while preserving order.
        seen: set[str] = set()
        close = [c for c in close if not (c in seen or seen.add(c))]  # type: ignore[func-returns-value]
        raise KeyError(
            f"Could not find any of {candidates} in sheet '{target_sheet}' ({file_path}). "
            f"Available columns: {all_cols}. "
            f"Suggested close matches: {close}"
        )

    logger.info(
        "Using column '%s' from sheet '%s' in %s",
        found_col,
        target_sheet,
        file_path.name,
    )

    # Force the first column to be 'Study_Area'
    first_col = df.columns[0]

    out = df[[first_col, found_col]].copy()
    out.columns = ["Study_Area", new_value_name]

    # Important: drop missing Study_Area BEFORE casting to str, otherwise NaN becomes "nan"
    out = out.dropna(subset=["Study_Area"])
    out["Study_Area"] = out["Study_Area"].astype(str).str.strip()
    out = out[out["Study_Area"].str.lower() != "nan"]

    out[new_value_name] = pd.to_numeric(out[new_value_name], errors="coerce")

    # Inner merges assume one row per Study_Area in each table.
    if out["Study_Area"].duplicated().any():
        examples = out.loc[out["Study_Area"].duplicated(), "Study_Area"].head(10).tolist()
        raise ValueError(
            f"Duplicate Study_Area values detected in {file_path} sheet '{target_sheet}' "
            f"for '{new_value_name}'. Examples: {examples}"
        )

    logger.info(
        "Loaded %d rows from %s [sheet=%s] -> %s",
        len(out),
        file_path.as_posix(),
        target_sheet,
        new_value_name,
    )
    return out


def run_final_academic_analysis(cfg: Config | None = None) -> Path:
    cfg = cfg or Config()

    logger.info("--- Final Empirical Analysis: COVID-19 Impact (Inflation Adjusted) ---")

    root = _repo_root()
    output_path = root / cfg.output_csv
    output_path.parent.mkdir(parents=True, exist_ok=True)

    file_2018 = root / cfg.file_2018
    file_2020 = root / cfg.file_2020

    # --- Load all four datasets ---
    # Baseline 2018
    df_18_sal = load_and_standardize(file_2018, ["Table35", "Table 35"], "Total 2018", "Salary_18")
    df_18_emp = load_and_standardize(
        file_2018, ["Table3", "Table 3"], "Full-time employment 2018", "FTE_18"
    )

    # Pandemic 2020
    df_20_sal = load_and_standardize(
        file_2020,
        ["SAL_UG_ALL_2Y_AREA_SEX", "SAL_UG_ALL_2Y_AREA"],
        "Total 2020",
        "Salary_20",
    )
    df_20_emp = load_and_standardize(
        file_2020,
        ["EMP_UG_ALL_2Y_AREA", "EMP_UG_ALL_2Y_AREA_SEX"],
        "Full-time employment 2020",
        "FTE_20",
    )

    # --- Perform INNER merges (keep only study areas present in all 4 tables) ---
    merged = df_18_sal
    merged = pd.merge(merged, df_20_sal, on="Study_Area", how="inner")
    merged = pd.merge(merged, df_18_emp, on="Study_Area", how="inner")
    merged = pd.merge(merged, df_20_emp, on="Study_Area", how="inner")

    logger.info("Rows after inner-merge across all tables: %d", len(merged))

    # --- Calculations Including Inflation ---
    required_cols = ["Salary_20", "Salary_18", "FTE_20", "FTE_18"]
    missing = [c for c in required_cols if c not in merged.columns]
    if missing:
        raise KeyError(f"Missing columns for calculation: {missing}. Found: {merged.columns.tolist()}")

    merged["Salary_18_Adj"] = (merged["Salary_18"] * cfg.cpi_2018_to_2020).round(0)
    merged["Salary_Diff"] = merged["Salary_20"] - merged["Salary_18_Adj"]
    merged["FTE_Diff"] = (merged["FTE_20"] - merged["FTE_18"]).round(1)

    # --- Filter for Research Goals ---
    deep_dive = merged[merged["Study_Area"].str.contains(cfg.targets_regex, na=False, case=False)]

    logger.info("--- RESULTS: SALARY VS EMPLOYABILITY (FTE%%) ---")
    cols = ["Study_Area", "Salary_18_Adj", "Salary_20", "Salary_Diff", "FTE_Diff"]
    if not deep_dive.empty:
        preview = deep_dive[cols].head(20)
        logger.info("Deep-dive preview (up to 20 rows):\n%s", preview.to_string(index=False))
    else:
        logger.warning("Targets not found. Check Excel naming.")
        logger.info("First few areas found: %s", merged["Study_Area"].head().tolist())

    merged.to_csv(output_path, index=False)
    logger.info("SUCCESS: Results saved to: %s", output_path.as_posix())

    # Save the deep-dive filtered subset as a companion CSV.
    targets_path = output_path.with_name(f"{output_path.stem}_targets{output_path.suffix}")
    deep_dive.to_csv(targets_path, index=False)
    logger.info("Deep-dive subset saved to: %s", targets_path.as_posix())

    return output_path


if __name__ == "__main__":
    try:
        run_final_academic_analysis()
    except Exception:
        logger.exception("ERROR: Analysis failed")
        raise
