# streamlit_app.py
# ============================================================
# Streamlit Dashboard Prototype / Rendering Layer
# Car Market Analysis Attica
# Consume Notebook 7 Registries
# ============================================================

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.dashboard.config import (
    APP_LAYOUT,
    APP_PAGE_ICON,
    APP_PAGE_TITLE,
    NOTEBOOK7_REGISTRY_FILES,
)
from src.dashboard.data_loader import (
    find_project_root,
    get_processed_dir,
    load_notebook7_registries,
    select_existing_columns,
)
from src.dashboard.kpi_cards import render_section_kpi_cards
from src.dashboard.styles import apply_custom_theme, render_hero


# ------------------------------------------------------------
# 1. Cached registry loading
# ------------------------------------------------------------

def build_registry_fingerprint(processed_dir: Path) -> tuple[tuple[str, int], ...]:
    """
    Builds a lightweight fingerprint for the Notebook 7 registry files.

    The fingerprint is based on file modification timestamps so Streamlit
    refreshes the cache when a registry file changes.
    """
    fingerprint_records = []

    for file_name in NOTEBOOK7_REGISTRY_FILES.values():
        file_path = processed_dir / file_name
        file_mtime_ns = file_path.stat().st_mtime_ns if file_path.exists() else -1
        fingerprint_records.append((file_name, file_mtime_ns))

    return tuple(fingerprint_records)


@st.cache_data(show_spinner="Loading Notebook 7 registries...")
def load_cached_notebook7_registries(
    processed_dir_str: str,
    registry_fingerprint: tuple[tuple[str, int], ...],
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Cached wrapper around the reusable registry loading layer.
    """
    _ = registry_fingerprint
    processed_dir = Path(processed_dir_str)

    return load_notebook7_registries(processed_dir)


# ------------------------------------------------------------
# 2. UI helper functions
# ------------------------------------------------------------

def render_registry_health(inventory_df: pd.DataFrame) -> None:
    """
    Renders the main registry validation status.
    """
    all_files_exist = bool(inventory_df["file_exists"].all())
    all_files_read = bool(inventory_df["can_read"].all())
    no_missing_columns = bool((inventory_df["missing_columns"] == "").all())

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Registry files",
        f"{inventory_df['file_exists'].sum()} / {len(inventory_df)}",
    )
    col2.metric(
        "Readable files",
        f"{inventory_df['can_read'].sum()} / {len(inventory_df)}",
    )
    col3.metric(
        "Column checks",
        "OK" if no_missing_columns else "Review",
    )

    if all_files_exist and all_files_read and no_missing_columns:
        st.success("All core Notebook 7 registries were loaded successfully.")
    else:
        st.warning(
            "One or more registries require attention. "
            "Review the validation table before continuing."
        )


def render_registry_inventory(inventory_df: pd.DataFrame) -> None:
    """
    Renders the registry inventory table.
    """
    st.subheader("Registry inventory")
    st.caption(
        "Validation summary for the CSV registries exported by Notebook 7."
    )

    st.dataframe(
        inventory_df,
        width="stretch",
        hide_index=True,
    )


def render_sections_preview(
    registries: dict[str, pd.DataFrame],
    show_metadata: bool,
) -> None:
    """
    Renders a preview of dashboard sections.
    """
    sections_df = registries.get("sections")

    if sections_df is None or sections_df.empty:
        st.info("No sections registry is available.")
        return

    sort_columns = select_existing_columns(sections_df, ["section_order", "section_id"])
    if sort_columns:
        sections_df = sections_df.sort_values(sort_columns)

    st.subheader("Dashboard sections")
    st.caption(
        "High-level structure of the dashboard views prepared by Notebook 7."
    )

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
        width="stretch",
        hide_index=True,
    )

    st.markdown("### Section details")

    for _, row in sections_df.iterrows():
        section_order = row.get("section_order", "")
        section_id = row.get("section_id", "unknown_section")
        section_title = row.get("section_title_el", section_id)
        section_description = row.get(
            "section_description_el",
            "No section description is available.",
        )

        with st.expander(f"{section_order}. {section_id}"):
            st.markdown(f"**Registry title:** {section_title}")
            st.write(section_description)

            if show_metadata:
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
                        width="stretch",
                        hide_index=True,
                    )


def render_bundles_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Renders the Streamlit-ready section bundles registry.
    """
    bundles_df = registries.get("section_bundles")

    if bundles_df is None or bundles_df.empty:
        st.info("No section bundles registry is available.")
        return

    st.subheader("Section bundles")
    st.caption(
        "Streamlit-ready mapping between dashboard sections, "
        "KPI cards, charts and source assets."
    )

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
        width="stretch",
        hide_index=True,
    )


def render_cards_and_charts_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Renders a summary of KPI cards and chart registries.
    """
    cards_df = registries.get("cards")
    charts_df = registries.get("charts")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("KPI cards")

        if cards_df is None or cards_df.empty:
            st.info("No KPI cards registry is available.")
        else:
            st.metric("Total KPI cards", len(cards_df))

            card_columns = select_existing_columns(
                cards_df,
                [
                    "card_order",
                    "card_id",
                    "section_id",
                    "card_scope",
                    "price_segment",
                    "kpi_label_el",
                    "display_value",
                    "source_table",
                ],
            )

            st.dataframe(
                cards_df[card_columns].head(30),
                width="stretch",
                hide_index=True,
            )

    with col2:
        st.subheader("Charts")

        if charts_df is None or charts_df.empty:
            st.info("No charts registry is available.")
        else:
            st.metric("Total charts", len(charts_df))

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
                width="stretch",
                hide_index=True,
            )


def render_dashboard_kpi_rendering_layer(
    registries: dict[str, pd.DataFrame],
) -> None:
    """
    Renders the first real dashboard layer for Issue #18.

    Σε αυτό το πρώτο increment δεν αφαιρούμε τα validation previews.
    Προσθέτουμε πραγματικό KPI rendering layer που καταναλώνει
    το Notebook 7 cards registry και εμφανίζει Streamlit metric cards.
    """
    sections_df = registries.get("sections")
    cards_df = registries.get("cards")

    if sections_df is None or sections_df.empty:
        st.info("No sections registry is available for dashboard rendering.")
        return

    if cards_df is None or cards_df.empty:
        st.info("No KPI cards registry is available for dashboard rendering.")
        return

    if "section_id" not in sections_df.columns:
        st.warning("The sections registry does not contain `section_id`.")
        return

    sort_columns = select_existing_columns(sections_df, ["section_order", "section_id"])
    if sort_columns:
        sections_df = sections_df.sort_values(sort_columns).reset_index(drop=True)

    section_options = sections_df["section_id"].astype(str).tolist()

    if not section_options:
        st.info("No dashboard sections were found.")
        return

    st.subheader("Dashboard rendering layer")
    st.caption(
        "Issue #18 first rendering increment: Notebook 7 KPI card registry "
        "mapped to Streamlit metric components."
    )

    selected_section_id = st.selectbox(
        "Select dashboard section",
        options=section_options,
        key="dashboard_render_section_id",
    )

    selected_section = sections_df.loc[
        sections_df["section_id"].astype(str) == selected_section_id
    ].iloc[0]

    section_title = selected_section.get("section_title_el", selected_section_id)
    section_description = selected_section.get("section_description_el", "")

    st.markdown(f"### {section_title}")

    if pd.notna(section_description) and str(section_description).strip():
        st.markdown(
            f"""
            <div class="section-note">
            {section_description}
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_cards_df = cards_df.loc[
        cards_df["section_id"].astype(str) == selected_section_id
    ].copy()

    st.caption(f"KPI cards found for this section: {len(section_cards_df)}")

    render_section_kpi_cards(
        registries=registries,
        section_id=selected_section_id,
        cards_per_row=4,
    )

    with st.expander("KPI registry rows used for this section"):
        preview_columns = select_existing_columns(
            section_cards_df,
            [
                "card_order",
                "card_id",
                "section_id",
                "card_scope",
                "price_segment",
                "kpi_label_el",
                "display_value",
                "value_type",
                "source_table",
            ],
        )

        if preview_columns:
            st.dataframe(
                section_cards_df[preview_columns],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No preview columns are available for this section.")


def render_filter_options_preview(registries: dict[str, pd.DataFrame]) -> None:
    """
    Renders the available dashboard filter options.
    """
    filter_options_df = registries.get("filter_options")

    if filter_options_df is None or filter_options_df.empty:
        st.info("No filter options registry is available.")
        return

    st.subheader("Filter options")
    st.caption(
        "Available filter groups and options prepared for the Streamlit dashboard."
    )

    if "filter_group" not in filter_options_df.columns:
        st.warning("The filter options registry does not contain `filter_group`.")
        return

    filter_group_values = (
        filter_options_df["filter_group"]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )

    if not filter_group_values:
        st.info("No filter groups were found.")
        return

    selected_filter_group = st.selectbox(
        "Select filter group",
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

    st.metric("Available options", len(filtered_df))

    st.dataframe(
        filtered_df[preview_columns],
        width="stretch",
        hide_index=True,
    )


# ------------------------------------------------------------
# 3. Streamlit app
# ------------------------------------------------------------

st.set_page_config(
    page_title=APP_PAGE_TITLE,
    page_icon=APP_PAGE_ICON,
    layout=APP_LAYOUT,
)

apply_custom_theme()

project_root = find_project_root(Path(__file__).resolve().parent)
processed_dir = get_processed_dir(project_root)
registry_fingerprint = build_registry_fingerprint(processed_dir)

registries, registry_inventory_df = load_cached_notebook7_registries(
    processed_dir_str=str(processed_dir),
    registry_fingerprint=registry_fingerprint,
)

render_hero()

st.markdown(
    """
    <div class="section-note">
    This prototype now extends the Notebook 7 registry validation layer into
    an initial dashboard rendering layer. KPI cards are rendered from
    <code>notebook7_dashboard_cards_registry.csv</code>, while the original
    registry validation previews remain available for technical review.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Project paths")

    st.write("Project root:")
    st.code(str(project_root), language="text")

    st.write("Processed data:")
    st.code(str(processed_dir), language="text")

    st.divider()

    st.write("Dashboard stage:")
    st.code("KPI rendering layer", language="text")

    st.divider()

    show_metadata = st.toggle(
        "Show technical metadata",
        value=True,
        help="Show source keys, plot keys and filter support flags where available.",
    )

render_registry_health(registry_inventory_df)

tab_dashboard, tab_inputs, tab_sections, tab_bundles, tab_components, tab_filters = st.tabs(
    [
        "Dashboard render",
        "Input validation",
        "Sections",
        "Section bundles",
        "Cards & charts",
        "Filters",
    ]
)

with tab_dashboard:
    render_dashboard_kpi_rendering_layer(registries)

with tab_inputs:
    render_registry_inventory(registry_inventory_df)

with tab_sections:
    render_sections_preview(
        registries=registries,
        show_metadata=show_metadata,
    )

with tab_bundles:
    render_bundles_preview(registries)

with tab_components:
    render_cards_and_charts_preview(registries)

with tab_filters:
    render_filter_options_preview(registries)