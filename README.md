# ecc3479-project

# Impact of COVID-19 on Australian Graduate Outcomes

## Group Members
- **Nur Atikah Binti Mohamad Tajarimim** - [36851825]
- **Madeeha Binti Subki** - [36856606]

## Research question (declared ambition: descriptive)
This project studies how graduate outcomes changed between 2018 and 2020 across Australian undergraduate study areas.

**Ambition declaration (DESCRIPTIVE / ASSOCIATIONAL):** The econometric analysis reports **conditional correlations** between baseline (2018) salary and the **change in full-time employment (FTE)** between 2018 and 2020 across study areas. With only two cross-sections, we do **not** claim to identify a causal “COVID treatment effect”.

## Repository structure
- `data/raw/` — raw Excel inputs (place files here)
- `data/clean/` — cleaned dataset(s) used for analysis
- `code/` — scripts + notebooks
- `results/` — generated tables/figures from the econometric notebook

## Software / dependencies
Python 3 with packages in `requirements.txt`.

## Reproducibility: full pipeline (raw → clean → analysis → results)

### 1) Clone the repository
```bash
git clone https://github.com/atikahtajarimim/ecc3479-project.git
cd ecc3479-project
```

### 2) Create an environment and install dependencies
Using `pip`:
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows (PowerShell)

pip3 install -r requirements.txt    # pip install -r requirements.txt (depending on your setup)
```

### 3) Raw → clean (creates the analysis dataset)
Run the cleaning script:
```bash
python3 code/data_analysis.py
```

Expected output file:
- `data/clean/final_pandemic_research_data.csv`

**Input requirement:** Place the raw Excel inputs in `data/raw/` in the filenames/format expected by `code/data_analysis.py`.

### 4) Clean → analysis → results (runs end-to-end)
Open and run all cells in the primary analysis notebook:
- `code/econometric_analysis.ipynb`

The notebook reads:
- `data/clean/final_pandemic_research_data.csv`

and writes outputs to:
- `results/`

Expected artifacts created in `results/` include:
- `table1_regression_results.csv`
- `table1_regression_results.md`
- `model_coefficients_hc3.csv`
- `bootstrap_summary.csv`
- `exhibit1_scatter_salary_delta_fte.png`
- `exhibit2_qqplot_residuals.png`
- `exhibit3_bootstrap_beta.png`

### 5) Robustness Analysis
Run the robustness analysis notebook after generating the clean dataset: 
- `code/robustness_analysis.ipynb`

The notebook reproduces all robustness checks and robustness tables used in the report. 

### Notes (for markers / replication)
- Paths in the notebook are **relative to the repository**, so it should run on any machine after Step 3.
- If you get a “clean data file not found” error, run Step 3 first to generate `data/clean/final_pandemic_research_data.csv`.
- If the notebook raises an error related to `tabulate`, install the missing dependency using:
```bash 
!pip install tabulate
```
or 
```bash
import sys
!{sys.executable} -m pip install tabulate
```

## Data codebook
This table defines columns in `data/clean/final_pandemic_research_data.csv`.

| Column Name | Description | Units |
| :--- | :--- | :--- |
| **Study_Area** | Academic field of study | Text |
| **Salary_18** | Nominal median starting salary in 2018 | AUD ($) |
| **Salary_20** | Nominal median starting salary in 2020 | AUD ($) |
| **Salary_Diff** | Nominal change in salary (Salary_20 − Salary_18) | AUD ($) |
| **FTE_18** | Full-Time Employment rate (2018) | % |
| **FTE_20** | Full-Time Employment rate (2020) | % |
| **FTE_Diff** | Difference in FTE rate between 2020 and 2018 (FTE_20 − FTE_18) | Percentage points |

## Methodology (high level)
1. **Data integration**: merge 2018 and 2020 QILT Graduate Outcomes Survey data.
2. **Cleaning**: exclude aggregate rows and summary statistics rows.
3. **Econometric analysis (descriptive)**: regress the change in FTE on baseline salary across study areas using HC3 robust standard errors. Robustness checks include alternative functional forms, outlier sensitivity test, and subsample analysis excluding health-related disciplines.
