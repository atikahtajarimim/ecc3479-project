import pandas as pd
import os

# 1. Professional Display Settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# 2. Define file paths
file_2018 = "data/raw/2018-GOS-National-Report-Tables-xlsx.xlsx"
file_2020 = "data/raw/GOS-2020-National-Tables.xlsx"

def load_and_standardize(file, possible_sheets, value_col, new_value_name):
    """
    Loads a sheet, finds the first column, renames it, and cleans numeric values.
    """
    xls = pd.ExcelFile(file)
    target_sheet = next((s for s in possible_sheets if s in xls.sheet_names), None)
    
    if not target_sheet:
        raise ValueError(f"Could not find sheets {possible_sheets} in {file}")
        
    df = pd.read_excel(file, sheet_name=target_sheet, skiprows=1)
    
    # Force the first column to be 'Study_Area'
    first_col = df.columns[0]
    df = df[[first_col, value_col]].copy()
    df.columns = ['Study_Area', new_value_name]
    
    # Clean text and convert the value column to numeric (handling errors as NaN)
    df['Study_Area'] = df['Study_Area'].astype(str).str.strip()
    df[new_value_name] = pd.to_numeric(df[new_value_name], errors='coerce')
    
    return df.dropna(subset=['Study_Area'])

def run_final_academic_analysis():
    print("--- Final Empirical Analysis: COVID-19 Impact ---")
    os.makedirs("data/clean", exist_ok=True)
    output_path = "data/clean/final_pandemic_research_data.csv"

    try:
        # --- Load all four datasets ---
        # Baseline 2018
        df_18_sal = load_and_standardize(file_2018, ['Table35', 'Table 35'], 'Total 2018', 'Salary_18')
        df_18_emp = load_and_standardize(file_2018, ['Table3', 'Table 3'], 'Full-time employment 2018', 'FTE_18')

        # Pandemic 2020
        df_20_sal = load_and_standardize(file_2020, ['SAL_UG_ALL_2Y_AREA_SEX', 'SAL_UG_ALL_2Y_AREA'], 'Total 2020', 'Salary_20')
        df_20_emp = load_and_standardize(file_2020, ['EMP_UG_ALL_2Y_AREA', 'EMP_UG_ALL_2Y_AREA_SEX'], 'Full-time employment 2020', 'FTE_20')

        # --- Perform Merges ---
        # We use 'reduce' style logic to ensure we don't lose the Salary_18 key
        dfs = [df_18_sal, df_20_sal, df_18_emp, df_20_emp]
        merged = dfs[0]
        for next_df in dfs[1:]:
            merged = pd.merge(merged, next_df, on='Study_Area', how='inner')

        # --- Calculations (Check if columns exist before calculating) ---
        if all(col in merged.columns for col in ['Salary_20', 'Salary_18', 'FTE_20', 'FTE_18']):
            merged['Salary_Diff'] = merged['Salary_20'] - merged['Salary_18']
            merged['FTE_Diff'] = (merged['FTE_20'] - merged['FTE_18']).round(1)
        else:
            raise KeyError(f"Missing columns for calculation. Found: {merged.columns.tolist()}")

        # --- Filter for Research Goals ---
        targets = 'Engineering|Nursing|Tourism'
        deep_dive = merged[merged['Study_Area'].str.contains(targets, na=False, case=False)]

        print("\n--- RESULTS: SALARY VS EMPLOYABILITY (FTE%) ---")
        if not deep_dive.empty:
            print(deep_dive[['Study_Area', 'Salary_Diff', 'FTE_Diff']])
        else:
            print("⚠️ Targets not found. Check Excel names.")
            print("First few areas found:", merged['Study_Area'].head().tolist())

        # Final Save
        merged.to_csv(output_path, index=False)
        print(f"\n✅ SUCCESS!")
        print(f"Results saved to: {output_path}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_final_academic_analysis()  















