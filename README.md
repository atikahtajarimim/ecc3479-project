# ecc3479-project — Impact of COVID-19 on Australian Graduate Outcomes

This project analyzes how graduating during the COVID-19 economic downturn affected:
- **median starting salaries**, and
- **full-time employment (FTE) rates**

for Australian undergraduates in **2020** compared with **pre-pandemic (2018)** outcomes.

---

## Research Question
**What was the effect of graduating during the COVID-19 economic downturn on the starting salaries and full-time employment rates of fresh Australian undergraduates in 2020 compared to the pre-pandemic (2018) cohort, by field of study?**

---

## Group Members
- **Nur Atikah Binti Mohamad Tajarimim** — 36851825  
- **Madeeha Binti Subki** — 36856606

---

## Repository Structure
- `code/`
  - `data_analysis.py` — main script that cleans/merges data and produces the final dataset
  - `eda_report.ipynb` — exploratory analysis and visualisations
- `data/raw/` — **manually added** raw Excel input files (not included in the repo)
- `data/clean/` — generated cleaned outputs

---

## Requirements
- **Python 3** (recommended: 3.10+)
- Python libraries:
  - `pandas`, `openpyxl` (data processing)
  - `matplotlib`, `seaborn` (visualisation)

Install via:

```bash
pip install -r requirements.txt
```

---

## Quickstart (Recommended)

```bash
git clone https://github.com/atikahtajarimim/ecc3479-project.git
cd ecc3479-project

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python3 code/data_analysis.py
```

Then open the notebook:
- `code/eda_report.ipynb` → **Run All** (VS Code or Jupyter)

---

## Input Data (Manual Step)
Place the following Excel files into `data/raw/` **with these exact filenames** (the script uses these paths directly):

- `data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx`
- `data/raw/GOS-2020-National-Tables.xlsx`

> Note: The raw Excel files are not committed to this repository (file size/licensing).  
> If you obtained files with different names, rename them to match the expected filenames above.

---

## Outputs
After a successful run, the script generates:
- `data/clean/final_pandemic_research_data.csv`

(Any plots/figures are generated in the notebook.)

---

## Notes on Expected Excel Structure (Important)
The script expects specific sheet and column names in the raw Excel files:

- **2018 salary**: sheet `Table35` (or `Table 35`) with column `Total 2018`
- **2018 employment**: sheet `Table3` (or `Table 3`) with column `Full-time employment 2018`
- **2020 salary**: sheet `SAL_UG_ALL_2Y_AREA_SEX` or `SAL_UG_ALL_2Y_AREA` with column `Total 2020`
- **2020 employment**: sheet `EMP_UG_ALL_2Y_AREA` or `EMP_UG_ALL_2Y_AREA_SEX` with column `Full-time employment 2020`

If filenames, sheet names, or column headers differ, the script may raise an error.

---

## Data Codebook
This table defines every column produced by `code/data_analysis.py` and stored in `data/clean/final_pandemic_research_data.csv`.

| Column Name | Description | Units |
| :--- | :--- | :--- |
| **Study_Area** | Academic field of study. | Text |
| **Salary_18** | Nominal median starting salary in 2018. | AUD ($) |
| **Salary_20** | Nominal median starting salary in 2020. | AUD ($) |
| **Salary_18_Adj** | 2018 salary adjusted to 2020 dollars (inflation-adjusted). | AUD ($) |
| **Salary_Diff** | Real change in salary (`Salary_20 - Salary_18_Adj`). | AUD ($) |
| **FTE_18** | Full-time employment rate (2018). | % |
| **FTE_20** | Full-time employment rate (2020). | % |
| **FTE_Diff** | Difference in FTE rate (`FTE_20 - FTE_18`). | Percentage points |

---

## Methodology (Summary)
1. **Data Integration**: Merged 2018 and 2020 QILT Graduate Outcomes Survey data.
2. **Inflation Adjustment**: Adjusted 2018 salary figures to 2020 values using a CPI multiplier of **1.027** to support real-term comparison.
3. **Cleaning**: Excluded aggregate national averages and statistical error rows to focus on 21 distinct study areas.

---

## Troubleshooting

### FileNotFoundError
- Confirm the Excel files exist in `data/raw/`
- Confirm filenames match exactly what the script expects

### Missing sheet (ValueError / KeyError)
- Your Excel workbook may use different sheet names (e.g., `Table 35` vs `Table35`)

### Missing column
- Column headers may differ (extra spaces, different wording). Try inspecting the sheet in Excel and matching the exact header text.

### Running from the wrong directory
- Run commands from the repository root (same level as `code/` and `data/`)
