import pandas as pd
import os

def main():
    # Define file path
    file_path = os.path.join('data', 'raw', 'Car_DB_Attiki_Y2021_2026_Ext_29_01_2026.xlsx')
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        # Load the Excel dataset
        df = pd.read_excel(file_path)
        
        # Display technical summary
        print("Dataset Summary")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        
        print("\nColumn Names:")
        print(df.columns.tolist())
        
        print("\nFirst 5 Rows:")
        print(df.head())
        
        # Display data types and missing values count
        print("\nData Types and Missing Values:")
        print(df.info())

    except Exception as e:
        print(f"An error occurred during file execution: {e}")

if __name__ == "__main__":
    main()