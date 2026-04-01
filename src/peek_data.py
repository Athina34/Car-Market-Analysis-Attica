from pathlib import Path
import pandas as pd

from data_cleaning import load_raw_data, clean_column_names

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def main():
    try:
        df = load_raw_data()
        df = clean_column_names(df)

        print("=" * 60)
        print("RAW DATA AUDIT")
        print("=" * 60)

        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nData types:")
        print(df.dtypes)

        print("\nMissing values per column:")
        print(df.isna().sum().sort_values(ascending=False))

        print("\nExact duplicate rows:")
        print(df.duplicated().sum())

        numeric_preview_cols = [col for col in ["Κυβικά", "Ιπποδύναμη", "Χιλιόμετρα", "Τιμή", "Εγγραφή"] if col in df.columns]
        if numeric_preview_cols:
            print("\nDescriptive preview for key columns:")
            print(df[numeric_preview_cols].describe(include="all"))

        categorical_preview_cols = [col for col in ["Καύσιμο", "Μετάδοση", "Κατασκευαστής", "Κατάσταση", "Περιοχή"] if col in df.columns]
        for col in categorical_preview_cols:
            print(f"\nTop values for '{col}':")
            print(df[col].value_counts(dropna=False).head(10))

        print("\nAudit completed successfully.")

    except Exception as e:
        print(f"An error occurred during dataset audit: {e}")


if __name__ == "__main__":
    main()