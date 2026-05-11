# src/dashboard/kpi_cards.py
# ============================================================
# KPI card rendering layer για το Streamlit dashboard
# Car Market Analysis Attica – Issue #18
# ============================================================

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# 1. Registry schema configuration
# ------------------------------------------------------------

# Ελάχιστες στήλες που πρέπει να υπάρχουν στο Notebook 7 cards registry.
# Κρατάμε το validation συντηρητικό ώστε να μη σπάει το app αν αλλάξουν
# optional metadata columns.
REQUIRED_KPI_CARD_COLUMNS = [
    "card_id",
    "section_id",
    "component_type",
]


# Πιθανές στήλες label/value.
# Το module χρησιμοποιεί την πρώτη διαθέσιμη στήλη από κάθε λίστα.
LABEL_COLUMN_CANDIDATES = [
    "kpi_label_el",
    "card_label_el",
    "card_title_el",
    "title_el",
    "label_el",
    "metric_label_el",
    "kpi_name",
    "card_id",
]

VALUE_COLUMN_CANDIDATES = [
    "display_value",
    "formatted_value",
    "kpi_value",
    "metric_value",
    "value",
    "raw_value",
]

ORDER_COLUMN_CANDIDATES = [
    "card_order",
    "component_order",
    "order",
    "display_order",
]


# Επιθυμητή σειρά για τα ελληνικά price segments.
# Αν στο μέλλον προστεθεί άλλο segment, θα μπει μετά από αυτά.
PREFERRED_PRICE_SEGMENT_ORDER = [
    "Χαμηλή",
    "Χαμηλομεσαία",
    "Μεσοϋψηλή",
    "Υψηλή",
]


# ------------------------------------------------------------
# 2. Internal utility helpers
# ------------------------------------------------------------

def _is_missing(value: Any) -> bool:
    """
    Επιστρέφει True για κενές / missing scalar τιμές.

    Έτσι αποφεύγουμε να εμφανίζονται στο dashboard τιμές όπως:
    'nan', '<NA>' ή κενά strings.
    """
    if value is None:
        return True

    # Αν δοθεί μη-scalar αντικείμενο, δεν το χειριζόμαστε ως missing εδώ.
    if isinstance(value, (pd.Series, pd.DataFrame, list, tuple, set, dict)):
        return False

    try:
        return bool(pd.isna(value)) or str(value).strip() == ""
    except (TypeError, ValueError):
        return str(value).strip() == ""


def _safe_text(value: Any, fallback: str = "—") -> str:
    """
    Ασφαλής μετατροπή οποιασδήποτε scalar τιμής σε καθαρό string.
    """
    if _is_missing(value):
        return fallback

    return str(value).strip()


def _first_existing_column(
    df: pd.DataFrame,
    candidate_columns: list[str],
) -> str | None:
    """
    Επιστρέφει την πρώτη στήλη που υπάρχει πραγματικά στο DataFrame.
    """
    for column in candidate_columns:
        if column in df.columns:
            return column

    return None


def _missing_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> list[str]:
    """
    Επιστρέφει τις required στήλες που λείπουν από το DataFrame.
    """
    return [column for column in required_columns if column not in df.columns]


def _build_metric_help(card_row: pd.Series) -> str | None:
    """
    Δημιουργεί προαιρετικό help text για κάθε KPI card.

    Το help εμφανίζεται σαν tooltip στο st.metric και βοηθάει στο
    traceability προς source metric/table.
    """
    help_parts: list[str] = []

    metadata_columns = {
        "source_metric": "Metric",
        "source_table": "Source table",
        "source_file": "Source file",
        "value_type": "Type",
        "unit": "Unit",
    }

    for column, label in metadata_columns.items():
        if column not in card_row.index:
            continue

        value = _safe_text(card_row.get(column), fallback="")
        if value:
            help_parts.append(f"{label}: {value}")

    if not help_parts:
        return None

    return " | ".join(help_parts)


# ------------------------------------------------------------
# 3. Public data preparation helpers
# ------------------------------------------------------------

def prepare_kpi_cards(
    cards_df: pd.DataFrame,
    section_id: str | None = None,
    price_segment: str | None = None,
    component_type: str = "kpi_card",
) -> pd.DataFrame:
    """
    Φιλτράρει και ταξινομεί τα KPI cards που θα εμφανιστούν.

    Parameters
    ----------
    cards_df:
        Το Notebook 7 cards registry.

    section_id:
        Προαιρετικό filter για συγκεκριμένο dashboard section.

    price_segment:
        Προαιρετικό filter για segment-level KPIs.
        Αν είναι None, κενό ή 'ALL', δεν εφαρμόζεται segment filter.

    component_type:
        Από προεπιλογή κρατάμε rows με component_type == 'kpi_card'.

    Returns
    -------
    pd.DataFrame
        KPI cards έτοιμα για rendering.
    """
    if cards_df is None or cards_df.empty:
        return pd.DataFrame()

    df = cards_df.copy()

    if "component_type" in df.columns:
        df = df.loc[
            df["component_type"].astype("string").str.strip() == component_type
        ]

    if section_id is not None and "section_id" in df.columns:
        df = df.loc[
            df["section_id"].astype("string").str.strip()
            == str(section_id).strip()
        ]

    if price_segment not in (None, "", "ALL") and "price_segment" in df.columns:
        segment_series = df["price_segment"].astype("string").str.strip()

        # Κρατάμε και global cards, αν υπάρχουν με price_segment == ALL.
        df = df.loc[
            segment_series.isin([str(price_segment).strip(), "ALL"])
        ]

    order_column = _first_existing_column(df, ORDER_COLUMN_CANDIDATES)

    sort_columns = [
        column
        for column in ["section_id", "price_segment", order_column, "card_id"]
        if column is not None and column in df.columns
    ]

    if sort_columns:
        df = df.sort_values(sort_columns, na_position="last")

    return df.reset_index(drop=True)


def get_price_segment_options(cards_df: pd.DataFrame) -> list[str]:
    """
    Επιστρέφει διαθέσιμα price segments από το cards registry.

    Χρησιμοποιείται από το Streamlit app για section-level selector,
    ώστε το segment_profile να μη δείχνει όλα τα segment cards μαζί.
    """
    if cards_df is None or cards_df.empty or "price_segment" not in cards_df.columns:
        return []

    available_segments = (
        cards_df["price_segment"]
        .astype("string")
        .dropna()
        .str.strip()
    )

    unique_segments = {
        segment
        for segment in available_segments.tolist()
        if segment and segment != "ALL"
    }

    ordered_segments = [
        segment
        for segment in PREFERRED_PRICE_SEGMENT_ORDER
        if segment in unique_segments
    ]

    extra_segments = sorted(unique_segments.difference(ordered_segments))

    return ordered_segments + extra_segments


# ------------------------------------------------------------
# 4. Streamlit rendering helpers
# ------------------------------------------------------------

def render_single_kpi_card(
    card_row: pd.Series,
    label_column: str | None = None,
    value_column: str | None = None,
) -> None:
    """
    Κάνει render ένα KPI card με st.metric.

    Το registry ιδανικά παρέχει έτοιμο display value. Αν δεν υπάρχει,
    χρησιμοποιούμε fallback από άλλες πιθανές value columns.
    """
    if label_column is not None:
        label = _safe_text(card_row.get(label_column), fallback="")
    else:
        label = ""

    if not label:
        label = _safe_text(card_row.get("card_id"), fallback="KPI")

    if value_column is not None:
        value = _safe_text(card_row.get(value_column), fallback="—")
    else:
        value = "—"

    st.metric(
        label=label,
        value=value,
        help=_build_metric_help(card_row),
    )


def render_kpi_cards_grid(
    cards_df: pd.DataFrame,
    section_id: str | None = None,
    price_segment: str | None = None,
    cards_per_row: int = 4,
) -> None:
    """
    Κάνει render KPI cards σε grid ανά section.

    Περιλαμβάνει fallback behavior ώστε το app να μη σπάει όταν:
    - λείπει registry,
    - λείπουν βασικές στήλες,
    - δεν υπάρχουν cards για το section,
    - δεν υπάρχει διαθέσιμη value column.
    """
    if cards_df is None or cards_df.empty:
        st.info("Δεν υπάρχουν διαθέσιμα KPI cards για εμφάνιση.")
        return

    missing_columns = _missing_columns(cards_df, REQUIRED_KPI_CARD_COLUMNS)
    if missing_columns:
        st.warning(
            "Το KPI cards registry δεν έχει την ελάχιστη αναμενόμενη δομή. "
            f"Λείπουν στήλες: {', '.join(missing_columns)}"
        )
        return

    section_cards = prepare_kpi_cards(
        cards_df=cards_df,
        section_id=section_id,
        price_segment=price_segment,
    )

    if section_cards.empty:
        section_label = (
            section_id
            if section_id is not None
            else "το επιλεγμένο section"
        )
        st.info(f"Δεν βρέθηκαν KPI cards για {section_label}.")
        return

    label_column = _first_existing_column(section_cards, LABEL_COLUMN_CANDIDATES)
    value_column = _first_existing_column(section_cards, VALUE_COLUMN_CANDIDATES)

    if value_column is None:
        st.warning(
            "Βρέθηκαν KPI cards, αλλά δεν υπάρχει διαθέσιμη στήλη τιμής. "
            "Αναμενόταν μία από: "
            f"{', '.join(VALUE_COLUMN_CANDIDATES)}"
        )
        return

    safe_cards_per_row = max(1, min(cards_per_row, 6))

    for start_idx in range(0, len(section_cards), safe_cards_per_row):
        row_df = section_cards.iloc[start_idx:start_idx + safe_cards_per_row]
        columns = st.columns(len(row_df))

        for column, (_, card_row) in zip(columns, row_df.iterrows()):
            with column:
                render_single_kpi_card(
                    card_row=card_row,
                    label_column=label_column,
                    value_column=value_column,
                )


def render_section_kpi_cards(
    registries: dict[str, pd.DataFrame],
    section_id: str,
    price_segment: str | None = None,
    cards_per_row: int = 4,
) -> None:
    """
    Wrapper για rendering απευθείας από το registries dictionary.

    Αναμένει dictionary όπως αυτό που επιστρέφει το
    load_notebook7_registries(), με key 'cards'.
    """
    cards_df = registries.get("cards")

    if cards_df is None:
        st.warning(
            "Δεν φορτώθηκε το Notebook 7 cards registry. "
            "Έλεγξε ότι υπάρχει το αρχείο "
            "`data/processed/notebook7_dashboard_cards_registry.csv`."
        )
        return

    render_kpi_cards_grid(
        cards_df=cards_df,
        section_id=section_id,
        price_segment=price_segment,
        cards_per_row=cards_per_row,
    )