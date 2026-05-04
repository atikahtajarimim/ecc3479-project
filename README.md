# ecc3479-project

## Impact of COVID-19 on Australian Graduate Outcomes

Analysis of how graduating during the COVID-19 economic downturn affected:
* median starting salaries, and
* full-time employment (FTE) rates
for Australian undergraduates in **2020** compared with **pre-pandemic (2018)** outcomes.

## Group Members
* **Nur Atikah Binti Mohamad Tajarimim** - [36851825]
* **Madeeha Binti Subki** [36856606]

## Research Question
What was the effect of graduating during the COVID-19 economic downturn on the starting salaries and full-time employment rates of fresh Australian undergraduates in 2020 compared to the pre-pandemic years?

## Software Information
This project requires **Python 3** and the following libraries:
* pandas & openpyxl (Data processing)
* matplotlib & seaborn (Visualization)

## How to run the Project
Follow these steps to replicate the analysis:

1. **Clone this repository** to your machine.
```bash
git clone https://github.com/atikahtajarimim/ecc3479-project.git
```

2. **Enter the folder**
```bash
cd ecc3479-project
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Manual step: add raw data files**
Place the following Excel files into `data/raw/` **with these exact filenames** (the script uses these paths directly):
- `data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx`
- `data/raw/GOS-2020-National-Tables.xlsx`

5. **Execute**: Run the script using the command:
```bash
python3 code/data_analysis.py
```

6. **View visuals**: Open `code/eda_report.ipynb` in VS Code (or Jupyter) and select **Run All**.

## Outputs
After the script runs successfully, it generates:
- `data/clean/final_pandemic_research_data.csv`

## Notes on expected Excel structure (important)
The script expects specific sheet/column names in the raw Excel files:
- 2018 salary: sheet `Table35` (or `Table 35`) with column `Total 2018`
- 2018 employment: sheet `Table3` (or `Table 3`) with column `Full-time employment 2018`
- 2020 salary: sheet `SAL_UG_ALL_2Y_AREA_SEX` or `SAL_UG_ALL_2Y_AREA` with column `Total 2020`
- 2020 employment: sheet `EMP_UG_ALL_2Y_AREA` or `EMP_UG_ALL_2Y_AREA_SEX` with column `Full-time employment 2020`

If the filenames, sheet names, or column headers differ, the script may raise an error.

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
| **FTE_Diff** | Difference in FTE rate (`FTE_20 - FTE_18`). | Percentage Points |

## Methodology
1. **Data Integration**: Merged 2018 and 2020 QILT Graduate Outcomes Survey data.
2. **Inflation Adjustment**: Adjusted 2018 salary figures to 2020 values using a CPI multiplier of **1.027** to ensure a real-term economic comparison.
3. **Cleaning**: Excluded aggregate national averages and statistical error rows to focus on 21 distinct study areas.

## Troubleshooting
- **FileNotFoundError**: Confirm the Excel files exist in `data/raw/` and the filenames match exactly what the script expects.
- **ValueError about missing sheets**: The Excel workbook may have different sheet names than expected.
- **Missing column error**: Column headers in your Excel file may differ (e.g., extra spaces or different wording).
