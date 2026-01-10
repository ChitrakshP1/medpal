import pandas as pd
import os

def validate_csv(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return

    df = pd.read_csv(file_path)
    errors_found = False

    print(f"--- 🔍 Validating {file_path} ---")

    # 1. Check for Empty Rows or Cells
    if df.isnull().values.any():
        print("⚠️ Warning: Empty cells found in your database!")
        print(df[df.isnull().any(axis=1)])
        errors_found = True

    # 2. Check for Duplicate Symptoms
    duplicates = df[df.duplicated(subset=['symptom'], keep=False)]
    if not duplicates.empty:
        print("⚠️ Warning: Duplicate symptoms detected!")
        print(duplicates[['symptom']])
        errors_found = True

    # 3. Check Risk Level Spelling
    valid_risks = ['High', 'Medium', 'Low']
    invalid_risks = df[~df['risk_level'].isin(valid_risks)]
    if not invalid_risks.empty:
        print(f"⚠️ Warning: Invalid Risk Levels found (Must be {valid_risks})!")
        print(invalid_risks[['symptom', 'risk_level']])
        errors_found = True

    if not errors_found:
        print("✅ Data is clean and ready for production!")

if __name__ == "__main__":
    validate_csv("database/symptoms_data.csv")