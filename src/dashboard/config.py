# src/dashboard/config.py
# ============================================================
# Configuration layer για το Streamlit dashboard prototype
# Car Market Analysis Attica – Issue #16
# ============================================================

from __future__ import annotations


# ------------------------------------------------------------
# 1. Βασικά στοιχεία εφαρμογής
# ------------------------------------------------------------

APP_TITLE = "Car Market Analysis Attica"
APP_SUBTITLE = (
    "Πρώτο Streamlit dashboard prototype με κατανάλωση "
    "των Notebook 7 registries"
)

APP_PAGE_TITLE = "Car Market Analysis Attica Dashboard"
APP_PAGE_ICON = "🏎️"
APP_LAYOUT = "wide"

ISSUE_LABEL = "#16 Streamlit Dashboard Prototype"


# ------------------------------------------------------------
# 2. Notebook 7 registry inputs
# ------------------------------------------------------------

NOTEBOOK7_REGISTRY_FILES = {
    "sections": "notebook7_dashboard_sections_registry.csv",
    "cards": "notebook7_dashboard_cards_registry.csv",
    "charts": "notebook7_dashboard_charts_registry.csv",
    "section_components": "notebook7_section_component_registry.csv",
    "section_bundles": "notebook7_streamlit_section_bundles.csv",
    "filter_options": "notebook7_dashboard_filter_options_registry.csv",
    "asset_inventory": "notebook7_integration_asset_inventory.csv",
}


# ------------------------------------------------------------
# 3. Ελάχιστες αναμενόμενες στήλες ανά registry
# ------------------------------------------------------------

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