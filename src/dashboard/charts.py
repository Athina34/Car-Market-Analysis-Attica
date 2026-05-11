# src/dashboard/charts.py
# ============================================================
# Chart rendering layer για το Streamlit dashboard
# Car Market Analysis Attica – Issue #18
# ============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# 1. Registry schema configuration
# ------------------------------------------------------------

REQUIRED_CHART_COLUMNS = [
    "chart_id",
    "section_id",
    "chart_type",
    "chart_title_el",
]

ORDER_COLUMN_CANDIDATES = [
    "chart_order",
    "component_order",
    "order",
    "display_order",
]

PLOT_ASSET_COLUMN_CANDIDATES = [
    "plot_file_name",
    "plot_file_path",
    "plot_asset_key",
    "plot_file",
    "file_name",
    "asset_file_name",
]

SOURCE_TABLE_COLUMN_CANDIDATES = [
    "data_file_name",
    "data_table_key",
    "source_table",
    "table_key",
]

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

SUPPORTED_NATIVE_CHART_TYPES = {
    "horizontal_bar",
    "stacked_horizontal_bar",
}


# ------------------------------------------------------------
# 2. Internal utility helpers
# ------------------------------------------------------------

def _is_missing(value: Any) -> bool:
    """
    Επιστρέφει True για κενές / missing scalar τιμές.
    """
    if value is None:
        return True

    if isinstance(value, (pd.Series, pd.DataFrame, list, tuple, set, dict)):
        return False

    try:
        return bool(pd.isna(value)) or str(value).strip() == ""
    except (TypeError, ValueError):
        return str(value).strip() == ""


def _safe_text(value: Any, fallback: str = "—") -> str:
    """
    Ασφαλής μετατροπή τιμής σε string.
    """
    if _is_missing(value):
        return fallback

    return str(value).strip()


def _first_existing_column(
    df: pd.DataFrame,
    candidate_columns: list[str],
) -> str | None:
    """
    Επιστρέφει την πρώτη διαθέσιμη στήλη από λίστα υποψηφίων.
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
    Επιστρέφει required στήλες που λείπουν από DataFrame.
    """
    return [column for column in required_columns if column not in df.columns]


def _candidate_image_paths(
    raw_value: str,
    plots_dir: Path,
) -> list[Path]:
    """
    Δημιουργεί πιθανά paths για plot asset.

    Χρησιμοποιείται μόνο ως fallback όταν δεν μπορεί να γίνει native rendering.
    """
    raw_path = Path(raw_value)
    candidate_paths: list[Path] = []

    if raw_path.is_absolute():
        candidate_paths.append(raw_path)

    if raw_path.suffix.lower() in IMAGE_EXTENSIONS:
        candidate_paths.append(plots_dir / raw_path.name)
    else:
        for extension in IMAGE_EXTENSIONS:
            candidate_paths.append(plots_dir / f"{raw_value}{extension}")

    return candidate_paths


def _candidate_table_paths(
    raw_value: str,
    processed_dir: Path,
) -> list[Path]:
    """
    Δημιουργεί πιθανά paths για source CSV table.
    """
    raw_path = Path(raw_value)
    candidate_paths: list[Path] = []

    if raw_path.is_absolute():
        candidate_paths.append(raw_path)

    if raw_path.suffix.lower() == ".csv":
        candidate_paths.append(processed_dir / raw_path.name)
    else:
        candidate_paths.append(processed_dir / f"{raw_value}.csv")

    return candidate_paths


def _to_numeric_series(series: pd.Series) -> pd.Series:
    """
    Μετατρέπει μια στήλη σε numeric με ασφαλές fallback.
    """
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def _format_percent(value: float) -> str:
    """
    Μορφοποιεί ποσοστό με 2 δεκαδικά, χωρίς περιττό μηδενικό στο τέλος.
    """
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _build_bar_label(
    percent_value: float,
    count_value: float | None = None,
) -> str:
    """
    Δημιουργεί label τύπου: 25.04% (2,077 αγγελίες).
    """
    percent_text = _format_percent(percent_value)

    if count_value is None:
        return f"{percent_text}%"

    return f"{percent_text}% ({count_value:,.0f} αγγελίες)"


def _render_matplotlib_figure(fig: Any) -> None:
    """
    Κάνει render Matplotlib figure στο Streamlit με fallback για παλαιότερο API.
    """
    try:
        st.pyplot(fig, clear_figure=True, width="content")
    except TypeError:
        st.pyplot(fig, clear_figure=True)
    finally:
        plt.close(fig)


# ------------------------------------------------------------
# 3. Public data preparation helpers
# ------------------------------------------------------------

def prepare_charts(
    charts_df: pd.DataFrame,
    section_id: str | None = None,
) -> pd.DataFrame:
    """
    Φιλτράρει και ταξινομεί τα charts που ανήκουν σε ένα dashboard section.
    """
    if charts_df is None or charts_df.empty:
        return pd.DataFrame()

    df = charts_df.copy()

    if section_id is not None and "section_id" in df.columns:
        df = df.loc[
            df["section_id"].astype("string").str.strip()
            == str(section_id).strip()
        ]

    order_column = _first_existing_column(df, ORDER_COLUMN_CANDIDATES)

    sort_columns = [
        column
        for column in ["section_id", order_column, "chart_id"]
        if column is not None and column in df.columns
    ]

    if sort_columns:
        df = df.sort_values(sort_columns, na_position="last")

    return df.reset_index(drop=True)


def find_plot_asset_path(
    chart_row: pd.Series,
    plots_dir: Path,
) -> Path | None:
    """
    Προσπαθεί να βρει plot asset μέσα στο plots/.

    Χρησιμοποιείται ως fallback, όχι ως primary rendering path.
    """
    for column in PLOT_ASSET_COLUMN_CANDIDATES:
        if column not in chart_row.index or _is_missing(chart_row.get(column)):
            continue

        plot_value = _safe_text(chart_row.get(column), fallback="")

        for candidate_path in _candidate_image_paths(plot_value, plots_dir):
            if candidate_path.exists():
                return candidate_path

    return None


def find_source_table_path(
    chart_row: pd.Series,
    processed_dir: Path,
) -> Path | None:
    """
    Προσπαθεί να βρει source table μέσα στο data/processed/.
    """
    for column in SOURCE_TABLE_COLUMN_CANDIDATES:
        if column not in chart_row.index or _is_missing(chart_row.get(column)):
            continue

        table_value = _safe_text(chart_row.get(column), fallback="")

        for candidate_path in _candidate_table_paths(table_value, processed_dir):
            if candidate_path.exists():
                return candidate_path

    return None


# ------------------------------------------------------------
# 4. Native chart builders
# ------------------------------------------------------------

def build_horizontal_bar_figure(
    chart_row: pd.Series,
    source_df: pd.DataFrame,
) -> Any:
    """
    Φτιάχνει horizontal bar chart από source table.

    Η κρίσιμη αλλαγή είναι ότι τα labels μπαίνουν πάντα μέσα στο axes frame:
    - δίνουμε αρκετό xlim,
    - τοποθετούμε τα labels κοντά στο δεξί όριο,
    - χρησιμοποιούμε ha='right'.
    """
    title = _safe_text(chart_row.get("chart_title_el"), fallback="Chart")
    x_field = _safe_text(chart_row.get("x_field"), fallback="share_pct")
    y_field = _safe_text(chart_row.get("y_field"), fallback="price_segment")
    value_field = _safe_text(chart_row.get("value_field"), fallback="")

    required_fields = [x_field, y_field]
    missing_fields = [field for field in required_fields if field not in source_df.columns]
    if missing_fields:
        raise ValueError(f"Missing fields for horizontal bar chart: {missing_fields}")

    df = source_df.copy()
    df[x_field] = _to_numeric_series(df[x_field])

    if value_field and value_field in df.columns:
        df[value_field] = _to_numeric_series(df[value_field])
    else:
        value_field = ""

    df = df.sort_values(x_field, ascending=True).reset_index(drop=True)

    y_values = df[y_field].astype(str).tolist()
    x_values = df[x_field].astype(float).tolist()

    max_x = max(x_values) if x_values else 0.0
    x_limit = max(max_x + 12.0, max_x * 1.45, 10.0)
    label_x = x_limit * 0.985

    fig_height = max(3.8, 0.65 * len(df) + 1.6)
    fig, ax = plt.subplots(figsize=(8.6, fig_height), dpi=130)

    ax.barh(y_values, x_values)

    for index, row in df.iterrows():
        percent_value = float(row[x_field])
        count_value = float(row[value_field]) if value_field else None
        label = _build_bar_label(percent_value, count_value)

        # Το label δεν μπαίνει πλέον στο x + offset, γιατί αυτό το έβγαζε
        # εκτός πλαισίου. Το καρφώνουμε μέσα στο δεξί όριο του axes.
        ax.text(
            label_x,
            index,
            label,
            va="center",
            ha="right",
            fontsize=9,
            clip_on=True,
        )

    ax.set_xlim(0, x_limit)
    ax.set_xlabel("Ποσοστό συμμετοχής στην αγορά (%)")
    ax.set_ylabel("Price segment")
    ax.set_title(title, pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    fig.tight_layout()

    return fig


def build_stacked_horizontal_bar_figure(
    chart_row: pd.Series,
    source_df: pd.DataFrame,
) -> Any:
    """
    Φτιάχνει stacked horizontal bar chart από source table.

    Τα labels μπαίνουν μέσα στα segments μόνο όταν υπάρχει αρκετός χώρος.
    Έτσι δεν βγαίνουν εκτός πλαισίου.
    """
    title = _safe_text(chart_row.get("chart_title_el"), fallback="Chart")
    x_field = _safe_text(chart_row.get("x_field"), fallback="share_pct")
    y_field = _safe_text(chart_row.get("y_field"), fallback="price_segment")
    category_field = _safe_text(chart_row.get("category_field"), fallback="")

    required_fields = [x_field, y_field, category_field]
    missing_fields = [field for field in required_fields if field not in source_df.columns]
    if missing_fields:
        raise ValueError(
            f"Missing fields for stacked horizontal bar chart: {missing_fields}"
        )

    df = source_df.copy()
    df[x_field] = _to_numeric_series(df[x_field])

    pivot_df = (
        df.pivot_table(
            index=y_field,
            columns=category_field,
            values=x_field,
            aggfunc="sum",
            fill_value=0.0,
        )
        .sort_index()
    )

    fig_height = max(4.2, 0.7 * len(pivot_df) + 1.8)
    fig, ax = plt.subplots(figsize=(9.0, fig_height), dpi=130)

    left_values = [0.0] * len(pivot_df)
    y_labels = pivot_df.index.astype(str).tolist()

    for category in pivot_df.columns:
        widths = pivot_df[category].astype(float).tolist()
        bars = ax.barh(y_labels, widths, left=left_values, label=str(category))

        for bar, width, left_value in zip(bars, widths, left_values):
            if width >= 6.0:
                ax.text(
                    left_value + width / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{_format_percent(width)}%",
                    va="center",
                    ha="center",
                    fontsize=8,
                    clip_on=True,
                )

        left_values = [
            left_value + width
            for left_value, width in zip(left_values, widths)
        ]

    ax.set_xlim(0, 100)
    ax.set_xlabel("Ποσοστό συμμετοχής στην αγορά (%)")
    ax.set_ylabel("Price segment")
    ax.set_title(title, pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
        frameon=False,
        fontsize=8,
    )

    fig.tight_layout()

    return fig


def build_native_chart_figure(
    chart_row: pd.Series,
    source_df: pd.DataFrame,
) -> Any:
    """
    Επιλέγει native chart builder βάσει chart_type.
    """
    chart_type = _safe_text(chart_row.get("chart_type"), fallback="")

    if chart_type == "horizontal_bar":
        return build_horizontal_bar_figure(
            chart_row=chart_row,
            source_df=source_df,
        )

    if chart_type == "stacked_horizontal_bar":
        return build_stacked_horizontal_bar_figure(
            chart_row=chart_row,
            source_df=source_df,
        )

    raise ValueError(f"Unsupported native chart type: {chart_type}")


# ------------------------------------------------------------
# 5. Streamlit rendering helpers
# ------------------------------------------------------------

def render_single_chart(
    chart_row: pd.Series,
    processed_dir: Path,
    plots_dir: Path,
    show_metadata: bool = False,
) -> None:
    """
    Κάνει render ένα chart block σε compact dashboard card.

    Προτεραιότητα:
    1. Native Matplotlib rendering από source table, για σωστό layout.
    2. Fallback σε PNG asset, αν λείπει ή αποτύχει το source table.
    3. Fallback preview table, αν υπάρχει μόνο source table.
    """
    chart_id = _safe_text(chart_row.get("chart_id"), fallback="unknown_chart")
    chart_title = _safe_text(chart_row.get("chart_title_el"), fallback=chart_id)
    chart_type = _safe_text(chart_row.get("chart_type"), fallback="unknown")

    source_table_path = find_source_table_path(
        chart_row=chart_row,
        processed_dir=processed_dir,
    )

    plot_asset_path = find_plot_asset_path(
        chart_row=chart_row,
        plots_dir=plots_dir,
    )

    with st.container(border=True):
        st.markdown(f"#### {chart_title}")

        if show_metadata:
            st.caption(f"Τύπος γραφήματος: `{chart_type}`")

        rendered_native_chart = False

        if (
            source_table_path is not None
            and chart_type in SUPPORTED_NATIVE_CHART_TYPES
        ):
            try:
                source_df = pd.read_csv(source_table_path, encoding="utf-8-sig")
                fig = build_native_chart_figure(
                    chart_row=chart_row,
                    source_df=source_df,
                )
                _render_matplotlib_figure(fig)
                rendered_native_chart = True
            except Exception as exc:
                st.warning(
                    "Δεν έγινε native rendering του chart. "
                    f"Θα χρησιμοποιηθεί fallback. Λεπτομέρειες: {exc}"
                )

        if not rendered_native_chart:
            if plot_asset_path is not None:
                st.image(
                    str(plot_asset_path),
                    width=760,
                )
            elif source_table_path is not None:
                st.info(
                    "Δεν βρέθηκε plot asset για αυτό το chart. "
                    "Εμφανίζεται fallback preview από το source table."
                )

                try:
                    source_df = pd.read_csv(source_table_path, encoding="utf-8-sig")
                    st.dataframe(
                        source_df,
                        width="stretch",
                        hide_index=True,
                    )
                except Exception as exc:
                    st.warning(f"Το source table βρέθηκε αλλά δεν διαβάστηκε: {exc}")
            else:
                st.warning(
                    "Δεν βρέθηκε ούτε plot asset ούτε source table για αυτό το chart. "
                    f"Chart ID: `{chart_id}`"
                )

        if show_metadata:
            with st.expander(f"Chart metadata: {chart_id}"):
                metadata_df = pd.DataFrame([chart_row])
                st.dataframe(
                    metadata_df,
                    width="stretch",
                    hide_index=True,
                )


def render_section_charts(
    registries: dict[str, pd.DataFrame],
    section_id: str,
    processed_dir: Path,
    plots_dir: Path,
    show_metadata: bool = False,
) -> None:
    """
    Κάνει render όλα τα charts ενός dashboard section.
    """
    charts_df = registries.get("charts")

    if charts_df is None or charts_df.empty:
        st.info("Δεν φορτώθηκε διαθέσιμο charts registry.")
        return

    missing_columns = _missing_columns(charts_df, REQUIRED_CHART_COLUMNS)
    if missing_columns:
        st.warning(
            "Το charts registry δεν έχει την ελάχιστη αναμενόμενη δομή. "
            f"Λείπουν στήλες: {', '.join(missing_columns)}"
        )
        return

    section_charts = prepare_charts(
        charts_df=charts_df,
        section_id=section_id,
    )

    if section_charts.empty:
        st.info(f"Δεν βρέθηκαν charts για το section `{section_id}`.")
        return

    st.caption(f"Charts found for this section: {len(section_charts)}")

    for _, chart_row in section_charts.iterrows():
        render_single_chart(
            chart_row=chart_row,
            processed_dir=processed_dir,
            plots_dir=plots_dir,
            show_metadata=show_metadata,
        )