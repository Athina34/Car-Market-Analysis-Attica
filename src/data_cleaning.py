import pandas as pd
import os

def clean_numeric_string(value):
    """Removes dots, spaces and converts to numeric."""
    if pd.isna(value) or str(value).strip() == '':
        return None
    # Remove dots and any non-digit characters except possibly decimal points
    clean_val = ''.join(c for c in str(value) if c.isdigit())
    return int(clean_val) if clean_val else None

def main():
    input_path = os.path.join('data', 'raw', 'Car_DB_Attiki_Y2021_2026_Ext_29_01_2026.xlsx')
    output_path = os.path.join('data', 'processed', 'cleaned_car_data.csv')

    print("Starting data cleaning process...")

    # 1. Load data and skip the first labels row (index 0)
    df = pd.read_excel(input_path, skiprows=[1])

    # 2. Clean numeric columns
    numeric_cols = ['Κυβικά', 'Ιπποδύναμη', 'Χιλιόμετρα', 'Τιμή']
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric_string)

    # 3. Handle missing values for critical columns
    # Drop rows where Price is missing as it is our target variable
    initial_count = len(df)
    df = df.dropna(subset=['Τιμή'])
    
    # 4. Save to processed folder
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"Cleaning complete.")
    print(f"Initial rows: {initial_count}")
    print(f"Rows after dropping missing prices: {len(df)}")
    print(f"Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    main()