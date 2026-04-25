# src/dashboard/data_loader.py
# ============================================================
# Data loading & validation layer για το Streamlit dashboard
# Car Market Analysis Attica – Issue #16
# ============================================================

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.dashboard.config import EXPECTED_MIN_COLUMNS, NOTEBOOK7_REGISTRY_FILES


def find_project_root(start_path: Path) -> Path:
    """
    Εντοπίζει το root του repository με βάση σταθερά project markers.

    Αυτό αποφεύγει hardcoded absolute paths και κάνει το dashboard
    πιο ασφαλές για εκτέλεση από διαφορετικά περιβάλλοντα.
    """
    current_path = start_path.resolve()

    for candidate_path in [current_path] + list(current_path.parents):
        has_readme = (candidate_path / "README.md").exists()
        has_data_processed = (candidate_path / "data" / "processed").exists()
        has_notebooks = (candidate_path / "notebooks").exists()

        if has_readme and has_data_processed and has_notebooks:
            return candidate_path

    raise FileNotFoundError(
        "Δεν ήταν δυνατό να εντοπιστεί το root του project. "
        "Τρέξε την εφαρμογή από τον φάκελο Car-Market-Analysis-Attica."
    )


def get_processed_dir(project_root: Path) -> Path:
    """
    Επιστρέφει τον φάκελο με τα processed CSV outputs.
    """
    return project_root / "data" / "processed"


def load_csv_registry(file_path: Path) -> pd.DataFrame:
    """
    Διαβάζει ένα CSV registry από το data/processed.

    Χρησιμοποιούμε utf-8-sig ώστε να διαβάζονται σωστά ελληνικά labels
    και τυχόν αρχεία που έχουν αποθηκευτεί με BOM.
    """
    return pd.read_csv(file_path, encoding="utf-8-sig")


def validate_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
) -> list[str]:
    """
    Επιστρέφει τις αναμενόμενες στήλες που λείπουν από ένα DataFrame.
    """
    return [column for column in expected_columns if column not in df.columns]


def load_notebook7_registries(
    processed_dir: Path,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Φορτώνει όλα τα Notebook 7 registries και δημιουργεί inventory ελέγχου.

    Returns
    -------
    registries:
        Λεξικό με key το registry name και value το αντίστοιχο DataFrame.

    inventory_df:
        Πίνακας validation με πληροφορίες για ύπαρξη αρχείων,
        δυνατότητα ανάγνωσης, πλήθος γραμμών/στηλών και missing columns.
    """
    registries: dict[str, pd.DataFrame] = {}
    inventory_records: list[dict[str, object]] = []

    for registry_key, file_name in NOTEBOOK7_REGISTRY_FILES.items():
        file_path = processed_dir / file_name
        file_exists = file_path.exists()

        if not file_exists:
            inventory_records.append(
                {
                    "registry_key": registry_key,
                    "file_name": file_name,
                    "file_exists": False,
                    "can_read": False,
                    "n_rows": pd.NA,
                    "n_columns": pd.NA,
                    "missing_columns": "file_missing",
                }
            )
            continue

        try:
            df = load_csv_registry(file_path)

            expected_columns = EXPECTED_MIN_COLUMNS.get(registry_key, [])
            missing_columns = validate_columns(df, expected_columns)

            registries[registry_key] = df

            inventory_records.append(
                {
                    "registry_key": registry_key,
                    "file_name": file_name,
                    "file_exists": True,
                    "can_read": True,
                    "n_rows": df.shape[0],
                    "n_columns": df.shape[1],
                    "missing_columns": " | ".join(missing_columns)
                    if missing_columns
                    else "",
                }
            )

        except Exception as exc:
            inventory_records.append(
                {
                    "registry_key": registry_key,
                    "file_name": file_name,
                    "file_exists": True,
                    "can_read": False,
                    "n_rows": pd.NA,
                    "n_columns": pd.NA,
                    "missing_columns": f"read_error: {exc}",
                }
            )

    inventory_df = (
        pd.DataFrame(inventory_records)
        .sort_values("registry_key")
        .reset_index(drop=True)
    )

    return registries, inventory_df


def select_existing_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    """
    Κρατά μόνο τις στήλες που υπάρχουν πραγματικά στο DataFrame.

    Είναι χρήσιμο για prototype rendering, ώστε το app να μη σπάει
    αν κάποιο registry αλλάξει ελαφρώς.
    """
    return [column for column in columns if column in df.columns]