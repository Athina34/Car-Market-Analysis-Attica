from pathlib import Path
import re
import numpy as np
import pandas as pd

# =========================================================
# Ρυθμίσεις paths
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Car_DB_Attiki_Y2021_2026_Ext_29_01_2026.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

CLEANED_OUTPUT = PROCESSED_DIR / "cleaned_car_data.csv"
ML_READY_OUTPUT = PROCESSED_DIR / "ml_ready_car_data.csv"


# =========================================================
# Utility functions
# =========================================================
def load_raw_data() -> pd.DataFrame:
    """
    Φορτώνει το raw Excel dataset.
    Χρησιμοποιούμε skiprows=[1] γιατί υπάρχει ενδιάμεση γραμμή labels.
    """
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Δεν βρέθηκε το raw αρχείο: {RAW_FILE}")

    df = pd.read_excel(RAW_FILE, skiprows=[1])
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Καθαρίζει ονόματα στηλών από περιττά κενά.
    """
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df


def safe_numeric_parser(value):
    """
    Ασφαλής μετατροπή σε αριθμό χωρίς το bug του digit-stripping.
    Κρατά σωστά τιμές τύπου 10500.0 και καθαρίζει strings με σημεία/κενά.
    """
    if pd.isna(value):
        return np.nan

    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)

    s = str(value).strip()

    if s == "":
        return np.nan

    invalid_tokens = {
        "nan", "none", "null", "-", "--",
        "electric", "Electric", "ηλεκτρικό", "Ηλεκτρικό"
    }
    if s in invalid_tokens:
        return np.nan

    s = s.replace("\xa0", "")
    s = s.replace(" ", "")
    s = s.replace("€", "")
    s = s.replace("cc", "").replace("CC", "")
    s = s.replace("hp", "").replace("HP", "")
    s = s.replace("km", "").replace("KM", "")
    s = s.replace("χιλ.", "").replace("ΧΙΛ.", "")
    s = s.replace("+", "")

    if re.fullmatch(r"\d+(\.\d+)?", s):
        return float(s)

    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        s = s.replace(".", "").replace(",", "")
        return float(s)

    if re.fullmatch(r"\d+,\d+", s):
        s = s.replace(",", ".")
        return float(s)

    s = re.sub(r"[^0-9.,-]", "", s)

    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", "")

    if s.count(".") > 1:
        s = s.replace(".", "")
    if s.count(",") > 1:
        s = s.replace(",", "")

    if "," in s and "." not in s:
        s = s.replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return np.nan


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Καθαρισμός text columns: strip και αντικατάσταση κενών strings με NA.
    """
    df = df.copy()

    # Διόρθωση για pandas 3.x / future compatibility
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

    for col in text_cols:
        # Διόρθωση: χρησιμοποιούμε string dtype αντί για astype(str)
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace({
            "": pd.NA,
            "nan": pd.NA,
            "None": pd.NA,
            "NULL": pd.NA
        })

    return df


def normalize_fuel_type(value):
    """
    Κανονικοποίηση τιμών καυσίμου.
    """
    if pd.isna(value):
        return np.nan

    s = str(value).strip().lower()

    mapping = {
        "βενζίνη": "Βενζίνη",
        "πετρέλαιο": "Πετρέλαιο",
        "diesel": "Πετρέλαιο",
        "hybrid": "Υβριδικό",
        "υβριδικό": "Υβριδικό",
        "υβριδικό βενζίνη": "Υβριδικό Βενζίνης",
        "υβριδικόβενζίνη": "Υβριδικό Βενζίνης",
        "υβριδικό plug-in βενζίνη": "Plug-in Hybrid Βενζίνης",
        "υβριδικό plug-inβενζίνη": "Plug-in Hybrid Βενζίνης",
        "υβριδικό plug-in benzίνη": "Plug-in Hybrid Βενζίνης",
        "υβριδικό πετρέλαιο": "Υβριδικό Πετρελαίου",
        "υβριδικό plug-in πετρέλαιο": "Plug-in Hybrid Πετρελαίου",
        "ηλεκτρικό": "Ηλεκτρικό",
        "electric": "Ηλεκτρικό",
        "αέριο (lpg) - βενζίνη": "LPG / Βενζίνη",
        "lpg": "LPG",
        "φυσικό αέριο (cng) - βενζίνη": "CNG / Βενζίνη",
        "φυσικό αέριο": "Φυσικό Αέριο",
    }

    return mapping.get(s, str(value).strip())


def normalize_transmission(value):
    """
    Κανονικοποίηση τύπου μετάδοσης.
    """
    if pd.isna(value):
        return np.nan

    s = str(value).strip().lower()

    mapping = {
        "χειροκίνητο": "Χειροκίνητο",
        "manual": "Χειροκίνητο",
        "αυτόματο": "Αυτόματο",
        "automatic": "Αυτόματο",
        "semi-automatic": "Ημιαυτόματο",
        "ημιαυτόματο": "Ημιαυτόματο",
    }

    return mapping.get(s, str(value).strip())


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Καθαρισμός βασικών αριθμητικών στηλών.
    """
    df = df.copy()

    numeric_candidates = ["Κυβικά", "Ιπποδύναμη", "Χιλιόμετρα", "Τιμή", "Εγγραφή"]

    for col in numeric_candidates:
        if col in df.columns:
            df[col] = df[col].apply(safe_numeric_parser)

    return df


def apply_domain_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Εφαρμογή βασικών domain rules.
    """
    df = df.copy()

    if "Καύσιμο" in df.columns:
        df["Καύσιμο"] = df["Καύσιμο"].apply(normalize_fuel_type)

    if "Μετάδοση" in df.columns:
        df["Μετάδοση"] = df["Μετάδοση"].apply(normalize_transmission)

    # Για ηλεκτρικά οχήματα τα κυβικά δεν έχουν ερμηνευτική αξία
    if "Καύσιμο" in df.columns and "Κυβικά" in df.columns:
        electric_mask = df["Καύσιμο"].astype("string").str.contains("Ηλεκτρ", na=False)
        df.loc[electric_mask, "Κυβικά"] = np.nan

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Βασικός χειρισμός missing values.
    Στο παρόν στάδιο αφαιρούμε μόνο εγγραφές χωρίς τιμή.
    """
    df = df.copy()

    if "Τιμή" in df.columns:
        df = df.dropna(subset=["Τιμή"])

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Συντηρητική απομάκρυνση exact duplicate rows.
    """
    df = df.copy()
    df = df.drop_duplicates()
    return df


def create_features(df: pd.DataFrame, reference_year: int = 2026) -> pd.DataFrame:
    """
    Δημιουργία derived features.
    """
    df = df.copy()

    if "Εγγραφή" in df.columns:
        df["Εγγραφή"] = pd.to_numeric(df["Εγγραφή"], errors="coerce")
        df["Ηλικία"] = reference_year - df["Εγγραφή"]

        df.loc[df["Ηλικία"] < 0, "Ηλικία"] = np.nan
        df.loc[df["Ηλικία"] > 50, "Ηλικία"] = np.nan

    return df


def build_ml_ready_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Κατασκευή ML-ready dataset με structured features.
    """
    df = df.copy()

    candidate_cols = [
        "Κατασκευαστής",
        "Τύπος",
        "Εγγραφή",
        "Ηλικία",
        "Καύσιμο",
        "Μετάδοση",
        "Κυβικά",
        "Ιπποδύναμη",
        "Χιλιόμετρα",
        "Κατάσταση",
        "Περιοχή",
        "Τιμή",
    ]

    existing_cols = [col for col in candidate_cols if col in df.columns]
    ml_df = df[existing_cols].copy()

    if "Τιμή" in ml_df.columns:
        ml_df = ml_df.dropna(subset=["Τιμή"])

    return ml_df


def save_outputs(cleaned_df: pd.DataFrame, ml_df: pd.DataFrame) -> None:
    """
    Αποθήκευση αρχείων στο data/processed.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(CLEANED_OUTPUT, index=False, encoding="utf-8-sig")
    ml_df.to_csv(ML_READY_OUTPUT, index=False, encoding="utf-8-sig")


def print_summary(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, ml_df: pd.DataFrame) -> None:
    """
    Εκτύπωση σύντομης αναφοράς cleaning.
    """
    print("=" * 60)
    print("DATA CLEANING SUMMARY")
    print("=" * 60)
    print(f"Raw rows: {len(raw_df):,}")
    print(f"Cleaned rows: {len(cleaned_df):,}")
    print(f"ML-ready rows: {len(ml_df):,}")
    print(f"Cleaned output: {CLEANED_OUTPUT}")
    print(f"ML-ready output: {ML_READY_OUTPUT}")
    print("=" * 60)


def main():
    raw_df = load_raw_data()

    df = raw_df.copy()
    df = clean_column_names(df)
    df = normalize_text_columns(df)
    df = clean_numeric_columns(df)
    df = apply_domain_rules(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = create_features(df)

    cleaned_df = df.copy()
    ml_df = build_ml_ready_dataset(cleaned_df)

    save_outputs(cleaned_df, ml_df)
    print_summary(raw_df, cleaned_df, ml_df)


if __name__ == "__main__":
    main()