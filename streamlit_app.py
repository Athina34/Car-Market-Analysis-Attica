# streamlit_app.py
# ============================================================
# Streamlit Dashboard Prototype
# Car Market Analysis Attica – Issue #16
# Consume Notebook 7 Registries
# ============================================================

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# 1. Βασικές ρυθμίσεις εφαρμογής
# ------------------------------------------------------------

APP_TITLE = "Car Market Analysis Attica"
APP_SUBTITLE = "Πρώτο Streamlit dashboard prototype με κατανάλωση των Notebook 7 registries"

NOTEBOOK7_REGISTRY_FILES = {
    "sections": "notebook7_dashboard_sections_registry.csv",
    "cards": "notebook7_dashboard_cards_registry.csv",
    "charts": "notebook7_dashboard_charts_registry.csv",
    "section_components": "notebook7_section_component_registry.csv",
    "section_bundles": "notebook7_streamlit_section_bundles.csv",
    "filter_options": "notebook7_dashboard_filter_options_registry.csv",
    "asset_inventory": "notebook7_integration_asset_inventory.csv",
}

EXPECTED_MIN_COLUMNS = {
    "sections": [
        "section_id",
        "section_order",
        "section_title_el",
        "streamlit_tab_name",
    ],
    "cards": [
        "card_id",
        "section_id",
        "component_type",
    ],
    "charts": [
        "chart_id",
        "section_id",
        "chart_type",
        "chart_title_el",
    ],
    "section_components": [
        "section_id",
        "n_cards",
        "n_charts",
    ],
    "section_bundles": [
        "section_id",
        "section_order",
        "section_title_el",
        "n_cards",
        "n_charts",
    ],
    "filter_options": [
        "filter_group",
        "option_order",
        "option_value",
        "option_label_el",
    ],
    "asset_inventory": [
        "asset_stage",
        "asset_id",
        "asset_kind",
        "file_name",
    ],
}


# ------------------------------------------------------------
# 2. Βοηθητικές συναρτήσεις paths
# ------------------------------------------------------------

def find_project_root(start_path: Path) -> Path:
    """
    Εντοπίζει το root του repository με βάση σταθερά project markers.

    Η λογική αυτή κάνει το app πιο ανθεκτικό, ώστε να μπορεί να τρέξει
    από το root του repository χωρίς hardcoded absolute paths.
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


PROJECT_ROOT = find_project_root(Path(__file__).resolve().parent)
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ------------------------------------------------------------
# 3. Data loading με cache
# ------------------------------------------------------------

@st.cache_data(show_spinner="Φόρτωση CSV registry...")
def load_csv_registry(file_path: str, file_mtime_ns: int) -> pd.DataFrame:
    """
    Διαβάζει ένα CSV registry.

    Το file_mtime_ns μπαίνει ως cache argument, ώστε το Streamlit cache
    να ανανεώνεται όταν αλλάξει το αρχείο στο δίσκο.
    """
    return pd.read_csv(file_path, encoding="utf-8-sig")


def validate_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
) -> list[str]:
    """
    Επιστρέφει λίστα με στήλες που λείπουν από ένα DataFrame.
    """
    return [column for column in expected_columns if column not in df.columns]


def load_notebook7_registries() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Φορτώνει όλα τα Notebook 7 registries και δημιουργεί inventory ελέγχου.
    """
    registries: dict[str, pd.DataFrame] = {}
    inventory_records = []

    for registry_key, file_name in NOTEBOOK7_REGISTRY_FILES.items():
        file_path = PROCESSED_DIR / file_name
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
            df = load_csv_registry(
                file_path=str(file_path),
                file_mtime_ns=file_path.stat().st_mtime_ns,
            )

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
                    "missing_columns": " | ".join(missing_columns) if missing_columns else "",
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


# ------------------------------------------------------------
# 4. Μικρά UI helpers
# ------------------------------------------------------------

def select_existing_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    """
    Κρατά μόνο τις στήλες που υπάρχουν πραγματικά στο DataFrame.
    Χρήσιμο για ανθεκτικό prototype rendering.
    """
    return [column for column in columns if column in df.columns]


def render_registry_health(inventory_df: pd.DataFrame) -> None:
    """
    Εμφανίζει βασικό status των Notebook 7 registry inputs.
    """
    all_files_exist = bool(inventory_df["file_exists"].all())
    all_files_read = bool(inventory_df["can_read"].all())
    no_missing_columns = bool((inventory_df["missing_columns"] == "").all())

    col1, col2, col3 = st.columns(3)

    col1.metric("Registry files", f"{inventory_df['file_exists'].sum()} / {len(inventory_df)}")
    col2.metric("Readable files", f"{inventory_df['can_read'].sum()} / {len(inventory_df)}")
    col3.metric(
        "Column checks",
        "OK" if no_missing_columns else "Needs review",
    )

    if all_files_exist and all_files_read and no_missing_columns:
        st.success("Όλα τα βασικά Notebook 7 registries φορτώθηκαν επιτυχώς.")
    else:
        st.warning(
            "Υπάρχει θέμα σε κάποιο registry. Δες τον πίνακα ελέγχου πριν συνεχίσουμε."
        )


def render_sections_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Εμφανίζει πρώτη επισκόπηση των dashboard sections.
    """
    sections_df = registries.get("sections")

    if sections_df is None or sections_df.empty:
        st.info("Δεν βρέθηκε διαθέσιμο sections registry.")
        return

    sort_columns = select_existing_columns(sections_df, ["section_order", "section_id"])
    if sort_columns:
        sections_df = sections_df.sort_values(sort_columns)

    st.subheader("Dashboard sections")

    preview_columns = select_existing_columns(
        sections_df,
        [
            "section_order",
            "section_id",
            "section_title_el",
            "section_description_el",
            "default_component_type",
            "streamlit_tab_name",
        ],
    )

    st.dataframe(
        sections_df[preview_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Αναλυτική επισκόπηση sections")

    for _, row in sections_df.iterrows():
        section_order = row.get("section_order", "")
        section_title = row.get("section_title_el", row.get("section_id", "Άγνωστη ενότητα"))
        section_id = row.get("section_id", "")
        section_description = row.get("section_description_el", "Δεν υπάρχει περιγραφή.")

        with st.expander(f"{section_order}. {section_title} — `{section_id}`"):
            st.write(section_description)

            detail_columns = select_existing_columns(
                sections_df,
                [
                    "primary_table_key",
                    "primary_plot_key",
                    "supports_price_segment_filter",
                    "supports_category_filter",
                ],
            )

            if detail_columns:
                st.dataframe(
                    pd.DataFrame([row[detail_columns]]),
                    use_container_width=True,
                    hide_index=True,
                )


def render_bundles_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Εμφανίζει το streamlit-ready section bundles registry.
    """
    bundles_df = registries.get("section_bundles")

    if bundles_df is None or bundles_df.empty:
        st.info("Δεν βρέθηκε διαθέσιμο section bundles registry.")
        return

    st.subheader("Streamlit-ready section bundles")

    preview_columns = select_existing_columns(
        bundles_df,
        [
            "section_order",
            "section_id",
            "section_title_el",
            "primary_table_key",
            "primary_plot_key",
            "n_cards",
            "n_charts",
            "card_ids",
            "chart_ids",
        ],
    )

    st.dataframe(
        bundles_df[preview_columns],
        use_container_width=True,
        hide_index=True,
    )


def render_cards_and_charts_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Εμφανίζει πρώτη σύνοψη KPI cards και charts.
    """
    cards_df = registries.get("cards")
    charts_df = registries.get("charts")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("KPI cards registry")

        if cards_df is None or cards_df.empty:
            st.info("Δεν βρέθηκε διαθέσιμο cards registry.")
        else:
            st.metric("Συνολικά KPI cards", len(cards_df))

            card_columns = select_existing_columns(
                cards_df,
                [
                    "card_order",
                    "card_id",
                    "section_id",
                    "card_scope",
                    "kpi_label_el",
                    "display_value",
                    "source_table",
                ],
            )

            st.dataframe(
                cards_df[card_columns].head(30),
                use_container_width=True,
                hide_index=True,
            )

    with col2:
        st.subheader("Charts registry")

        if charts_df is None or charts_df.empty:
            st.info("Δεν βρέθηκε διαθέσιμο charts registry.")
        else:
            st.metric("Συνολικά charts", len(charts_df))

            chart_columns = select_existing_columns(
                charts_df,
                [
                    "chart_order",
                    "chart_id",
                    "section_id",
                    "chart_title_el",
                    "chart_type",
                    "data_table_key",
                    "plot_asset_key",
                ],
            )

            st.dataframe(
                charts_df[chart_columns],
                use_container_width=True,
                hide_index=True,
            )


def render_filter_options_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Εμφανίζει τις διαθέσιμες επιλογές φίλτρων.
    """
    filter_options_df = registries.get("filter_options")

    if filter_options_df is None or filter_options_df.empty:
        st.info("Δεν βρέθηκε διαθέσιμο filter options registry.")
        return

    st.subheader("Streamlit filter options")

    filter_group_values = (
        filter_options_df["filter_group"]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
        if "filter_group" in filter_options_df.columns
        else []
    )

    selected_filter_group = st.selectbox(
        "Επίλεξε ομάδα φίλτρου",
        options=filter_group_values,
    )

    filtered_df = filter_options_df.loc[
        filter_options_df["filter_group"].astype(str) == selected_filter_group
    ].copy()

    preview_columns = select_existing_columns(
        filtered_df,
        [
            "filter_group",
            "option_order",
            "option_value",
            "option_label_el",
            "section_ids_supported",
            "is_default_option",
        ],
    )

    st.dataframe(
        filtered_df[preview_columns],
        use_container_width=True,
        hide_index=True,
    )


# ------------------------------------------------------------
# 5. Streamlit app
# ------------------------------------------------------------

st.set_page_config(
    page_title="Car Market Analysis Attica Dashboard",
    page_icon="🏎️",
    layout="wide",
)

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown(
    """
    Το παρόν prototype αποτελεί το πρώτο λειτουργικό βήμα του dashboard layer.
    Σε αυτό το στάδιο δεν αναπαράγουμε την ανάλυση των notebooks.
    Ελέγχουμε ότι η εφαρμογή μπορεί να καταναλώσει καθαρά τα exported registries
    του Notebook 7 από τον φάκελο `data/processed/`.
    """
)

with st.sidebar:
    st.header("Project paths")
    st.write("Project root:")
    st.code(str(PROJECT_ROOT), language="text")

    st.write("Processed data:")
    st.code(str(PROCESSED_DIR), language="text")

    st.divider()
    st.write("Issue:")
    st.code("#16 Streamlit Dashboard Prototype", language="text")

registries, registry_inventory_df = load_notebook7_registries()

render_registry_health(registry_inventory_df)

tab_inputs, tab_sections, tab_bundles, tab_components, tab_filters = st.tabs(
    [
        "Έλεγχος inputs",
        "Sections",
        "Section bundles",
        "Cards & charts",
        "Filters",
    ]
)

with tab_inputs:
    st.subheader("Notebook 7 registry inventory")

    st.dataframe(
        registry_inventory_df,
        use_container_width=True,
        hide_index=True,
    )

with tab_sections:
    render_sections_preview(registries)

with tab_bundles:
    render_bundles_preview(registries)

with tab_components:
    render_cards_and_charts_preview(registries)

with tab_filters:
    render_filter_options_preview(registries)