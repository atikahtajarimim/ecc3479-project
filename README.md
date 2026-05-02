# ecc3479-project

# Impact of COVID-19 on Australian Graduate Outcomes

## Group Members:
• Nur Atikah Binti Mohamad Tajarimim - [36851825]
• Madeeha Binti Muhamad Subki - [36856606]

## Research Question
What was the effect of graduating during the COVID-19 economic downturn on the starting salaries and full-time employment rates of fresh Australian undergraduates in 2020 compared to the pre-pandemic cohort of 2018?

## Repository Structure
• code/: Contains 'data_analysis.py' and 'eda_report.ipynb'.
• data/raw/: Original QILT GOS Excel files.
• data/clean/: 'final_pandemic_research_data.csv'.
• requirements.txt: List of libraries needed (no trailing dots).

## Data Codebook (Full Dataset)
Column Name         Description                                 Units
Study_Area          Academic field of study.                    Text
Salary_18           Median starting salary in 2018.             AUD ($)
Salary_20           Median starting salary in 2020.             AUD ($)
Salary_18_Adj       2018 Salary adjusted to 2020 dollars.       AUD ($)
Salary_Diff         Real change in salary (2020 - 2018_Adj).    AUD ($)
FTE_18              Full-Time Employment rate (2018).           %
FTE_20              Full-Time Employment rate (2020).           %
FTE_Diff            Change in FTE rate (FTE_20 - FTE_18).       pp

## Methodology
1. Inflation Adjustment: 2018 salaries were adjusted to 2020 AUD using a cumulative CPI factor of 1.027 (approx. 2.7% over 2 years) to ensure a "real" comparison.
2. Cleaning: Removed 'All study areas' and 'Standard deviation' rows.

## Software Information
This project is written in **Python 3**. To run the code, I must have the following packages installed: 
* 'pandas'
* 'openpyxl'

## How to run the Project
1. Clone: git clone https://github.com/atikahtajarimim/ecc3479-project.git
2. Install: pip install -r requirements.txt
3. Run: Open 'code/eda_report.ipynb' and select "Run All".