# ecc3479-project

# Impact of COVID-19 on Australian Graduate Outcomes

## Research Question 
What was the effect of graduating during the COVID-19 economic downturn on the starting salaries and full-time employment rates of fresh Australian undergraduates in 2020 compared to the pre-pandemic cohort of 2018? 

## Repository Structure
* **code/**: Contains 'data_analysis.py' (the Python script used to transform and merge raw data). 
* **data/raw/**: Contains the original QILT GOS Excel files for 2018 and 2020. 
* **data/clean/**: Contains 'final_pandemic_research_data.csv' (the merged dataset ready for analysis). 
* **requirements.txt**: The list of libraries (pandas,openpyxl) needed to run this.

## Software Information
This project is written in **Python 3**. To run the code, I must have the following packages installed: 
* 'pandas'
* 'openpyxl'

## How to run the Project
Follow these steps to replicate the analysis:
1. **Clone this repository** to your machine.
2. Enter the Folder: 
```bash
cd ecc3479-project
```
3. **Install dependencies**: Run 
```bash
pip install -r requirements.txt
```
4. **Manual Step**: Ensure the raw Excel files are inside the 'data/raw/' folder.
5. **Execute**: Run the script using the command: 
```bash
python3 code/data_analysis.py
```
## Data Codebook
* **Study_Area**: Field of study (e.g., Engineering, Nursing).
* **Salary_Diff**: The change in median salary between 2018 and 2020 ($).
* **FTE_Diff**: The change in Full-Time Employment rate percentage points. 

Note: The Script will automatically read from data/raw/output the final processed results into the data/clean/folder. 