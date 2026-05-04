# ecc3479-project

# Impact of COVID-19 on Australian Graduate Outcomes 

## Group Members:
* **Nur Atikah Binti Mohamad Tajarimim** - [36851825]
* **Madeeha Binti Subki** [36856606]

### Research Question
What was the effect of graduating during the COVID-19 economic downturn on the starting salaries and full-time employment rates of fresh Australian undergraduates in 2020 compared to the pre-pandemic cohort of 2018?

## Software Information
This project requires **Python 3** and the following libraries: 
* pandas & openpyxl (Data processing)
* matplotlib & seaborn (Visualization) 

## How to run the Project
Follow these steps to replicate the analysis:
1. **Clone this repository** to your machine.
```bash 
git clone [https://github.com/atikahtajarimim/ecc3479-project.git]
```
2. Enter the Folder: 
```bash
cd ecc3479-project
```
3. **Install dependencies**: Run 
```bash
pip install -r requirements.txt 
```
or 
```bash 
pip3 install -r requirements.txt 
```
depending on your setup.

4. **Manual Step**: Ensure the raw Excel files are inside the 'data/raw/' folder.
5. **Execute**: Run the script using the command: 
```bash
python3 code/data_analysis.py
```
6. View Visuals: Open code/eda_report.ipynb in VS Code and select Run All. 

## Data Codebook
This table defines every column produced by data_analysis.py and stored in final_pandemic_research_data.csv.
| Column Name | Description | Units | 
| :--- | :--- | :--- |
| **Study_Area** | Academic field of study. | Text |
| **Salary_18** | Nominal median starting salary in 2018. | AUD ($) |
| **Salary_20** | Nominal median starting salary in 2020. | AUD ($) |
| **Salary_18_Adj** | 2018 Salary adjusted to 2020 dollars (inflation-adjusted). | AUD ($) |
| **Salary_Diff** | Real change in salary (Salary_20 - Salary_18_Adj). | AUD ($) |
| **FTE_18** | Full-Time Employment rate (2018). | % |
| **FTE_20** | Full-Time Employment rate (2020). | % |
| **FTE_Diff** | Difference in FTE rate between 2020 and 2018 (FTE_20 - FTE_18). | Percentage Points | 

## Methodology 
1. **Data Integration**: Merged 2018 and 2020 QILT Graduate Outcomes Survey data. 
2. **Inflation Adjustment**: Adjusted 2018 salary figures to 2020 values using a CPI multiplier of **1.027** to ensure a real-term economic comparison. 
3. **Cleaning**: Excluded aggregate national averages and statistical error rows to focus on 21 distinct study areas. 

Note: The Script will automatically read from data/raw/output the final processed results into the data/clean/folder. 
