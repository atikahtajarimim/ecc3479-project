import pandas as pd

# ADD THESE TWO LINES HERE:
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define the file paths based on your raw folder
file_2018 = "data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx"
file_2020 = "data/raw/GOS-2020-National-Tables.xlsx"

def load_data():
    print( "--- Starting Data Load ---" )
    # Reading 2018 Salary Table (Table 35) 
    try: 
        df_2018 = pd.read_excel(file_2018, sheet_name='Table35' , skiprows=1) 
        print("✅ 2018 Salary Data Loaded!")
        # Show first 5 rows to confirm it looks right
        print (df_2018.head())
    except Exception as e:
        print(f"❌ Error loading 2018 data: {e}")
        
    # Reading 2020 Salary Table (SAL_UG_ALL_2Y_AREA_SEX)
    try:
        df_2020 = pd.read_excel(file_2020, sheet_name='SAL_UG_ALL_2Y_AREA_SEX' , skiprows=1)
        print( "\n✅ 2020 Salary Data Loaded!" )
        print(df_2020.head())
    except Exception as e: 
        print(f"❌ Error loading 2020 data: {e}")

if __name__ == "__main__":
    load_data()

import pandas as pd

# File paths
file_2018 = "data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx"
file_2020 = "data/raw/GOS-2020-National-Tables.xlsx"

def run_clean_analysis():
    # 1. Process 2018 - Grab only the 'Total' column
    df_18 = pd.read_excel(file_2018, sheet_name='Table35', skiprows=1)
    df_18 = df_18[['Unnamed: 0', 'Total 2018']].dropna()
    df_18.columns = [ 'Study_Area', 'Salary_2018' ] 

    # 2. Process 2020 - Grabbing only the 'Total' column
    df_20 = pd.read_excel(file_2020, sheet_name='SAL_UG_ALL_2Y_AREA_SEX', skiprows=1)
    df_20 = df_20[[ 'Unnamed: 0', 'Total 2020' ]].dropna()
    df_20.columns = [ 'Study_Area', 'Salary_2020' ]

    # 3. Merge and calculate
    merged = pd.merge(df_18, df_20, on='Study_Area')
    merged[ 'Dollar_Diff' ] = merged[ 'Salary_2020' ] - merged[ 'Salary_2018' ]

    # 4. Filter for your 3 target industries for the report
    target_areas = [ 'Engineering', 'Nursing', 'Creative arts' ]
    deep_dive = merged[merged[ 'Study_Area' ].str.contains( '|'.join(target_areas), na=False )]

    print( "--- RESEARCH RESULTS: TOTAL PERSONS MEDIAN SALARY ---" )
    print(merged[[ 'Study_Area', 'Salary_2018', 'Salary_2020', 'Dollar_Diff' ]])

    print( "\n--- DEEP DIVE: KEY INDUSTRIES FOR ANALYSIS ---" )
    print(deep_dive)

    # Save the final cleaned version
    merged.to_csv("data/clean/final_total_salary_comparison.csv", index=False) 
    print( "\n✅ Success! Only 'Total' data is now in  your terminal and saved to your folder." )

if __name__ == "__main__":
    run_clean_analysis()

import pandas as pd 

file_2018 = "data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx"
file_2020 = "data/raw/GOS-2020-National-Tables.xlsx"

def run_final_academic_analysis():
    print( "--- Final Empirical Analysis: COVID-19 Impact ---" )

    # 1. 2018 Data (Baseline)
    df_18_sal = pd.read_excel(file_2018, sheet_name='Table35', skiprows=1)
    df_18_sal = df_18_sal[[ 'Unnamed: 0', 'Total 2018' ]].dropna()
    df_18_sal.columns = [ 'Study_Area', 'Salary_18' ]

    df_18_emp = pd.read_excel(file_2018, sheet_name='Table3', skiprows=1)
    df_18_emp = df_18_emp[[ 'Unnamed: 0', 'Full-time employment 2018' ]].dropna()
    df_18_emp.columns = [ 'Study_Area', 'FTE_18' ]

    # 2. 2020 Data (Treatment)
    df_20_sal = pd.read_excel(file_2020, sheet_name='SAL_UG_ALL_2Y_AREA_SEX', skiprows=1)
    df_20_sal = df_20_sal[[ 'Unnamed: 0', 'Total 2020' ]].dropna()
    df_20_sal.columns = [ 'Study_Area', 'Salary_20']

    df_20_emp = pd.read_excel(file_2020, sheet_name='EMP_UG_ALL_2Y_AREA', skiprows=1)
    df_20_emp = df_20_emp[[ 'Unnamed: 0', 'Full-time employment 2020' ]].dropna()
    df_20_emp.columns = [ 'Study_Area', 'FTE_20' ] 

    # 3. Merge & Calculate Differences
    merged = pd.merge(df_18_sal, df_20_sal, on='Study_Area')
    merged = pd.merge(merged, df_18_emp, on='Study_Area')
    merged = pd.merge(merged, df_20_emp, on='Study_Area') 

    merged[ 'Salary_Diff' ] = merged[ 'Salary_20' ] - merged[ 'Salary_18' ]
    merged[ 'FTE_Diff' ] = (merged[ 'FTE_20' ] - merged[ 'FTE_18' ]).round(1)

    # 4. Filter for your target comparison 
    targets = [ 'Engineering', 'Nursing', 'Creative arts' ]
    deep_dive = merged[merged[ 'Study_Area' ].str.contains( '|'.join(targets), na=False )]

    print( "\n--- RESULTS: SALARY VS EMPLOYABILITY (FTE%) ---" )
    print(deep_dive[[ 'Study_Area', 'Salary_Diff', "FTE_Diff" ]])

    merged.to_csv("data/clean/final_pandemic_research_data.csv", index=False)
    print( "\n✅ DATA READY! Use 'final_pandemic_research_data.csv' for your GitHub." )

if __name__ == "__main__":
    run_final_academic_analysis()

















