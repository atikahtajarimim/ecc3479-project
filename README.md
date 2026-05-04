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
1. **Clone the repository**
   ```bash
   git clone https://github.com/atikahtajarimim/ecc3479-project.git
   cd ecc3479-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Raw → clean** (produces `data/clean/final_pandemic_research_data.csv`)
   ```bash
   python3 code/data_analysis.py
   ```
   *Note:* Ensure the raw Excel files are placed in `data/raw/` as expected by the script.

4. **Clean → analysis → results**
   Open the notebook and run all cells:
   - `code/econometric_analysis.ipynb`

   The notebook writes outputs to the `results/` directory (regression table + figures).

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
3. **Econometric analysis (descriptive)**: regress the change in FTE on baseline salary across study areas with robust (HC3) SEs and bootstrap sensitivity checks.
