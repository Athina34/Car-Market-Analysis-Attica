# ============================================================
# Custom UI styling for the Streamlit dashboard
# Car Market Analysis Attica
# ============================================================

from __future__ import annotations

import streamlit as st


def apply_custom_theme() -> None:
    """
    Applies a balanced semi-dark executive dashboard theme.

    Design direction:
    - muted blue-gray background
    - dark navy sidebar
    - soft light cards
    - burgundy accent used only for hierarchy
    - subtle hover states for a more interactive feel
    """
    st.markdown(
        """
        <style>
        /* ====================================================
           1. Base application background
        ==================================================== */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top right, rgba(89, 28, 46, 0.11), transparent 30%),
                linear-gradient(180deg, #dbe3ed 0%, #cfd8e4 100%);
            color: #172033;
        }

        .stApp {
            background:
                linear-gradient(180deg, #dbe3ed 0%, #cfd8e4 100%);
        }

        .block-container {
            padding-top: 2.1rem;
            padding-bottom: 3.2rem;
            max-width: 1360px;
        }

        header[data-testid="stHeader"] {
            background: rgba(13, 20, 33, 0.98);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* ====================================================
           2. Typography
        ==================================================== */

        h1, h2, h3, h4 {
            color: #111827 !important;
            letter-spacing: -0.025em;
        }

        p {
            color: #334155;
            line-height: 1.72;
        }

        .section-note {
            color: #334155;
            font-size: 1rem;
            line-height: 1.75;
            max-width: 1120px;
            margin: 0.9rem 0 1.35rem 0;
        }

        /* ====================================================
           3. Sidebar
        ==================================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #172033 0%, #0f172a 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 5px 0 28px rgba(15, 23, 42, 0.20);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #f8fafc !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #cbd5e1 !important;
        }

        section[data-testid="stSidebar"] code {
            color: #e2e8f0 !important;
            background: rgba(255, 255, 255, 0.075) !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] pre {
            background: rgba(255, 255, 255, 0.065) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.13);
        }

        /* ====================================================
           4. Hero section
        ==================================================== */

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2.45rem 2.65rem;
            border-radius: 24px;
            background:
                linear-gradient(135deg, #1e293b 0%, #111827 62%, #2b1722 100%);
            border: 1px solid rgba(255, 255, 255, 0.11);
            box-shadow:
                0 24px 60px rgba(15, 23, 42, 0.30),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            margin-bottom: 1.45rem;
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease;
        }

        .hero-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow:
                0 30px 70px rgba(15, 23, 42, 0.34),
                inset 0 1px 0 rgba(255, 255, 255, 0.08);
        }

        .hero-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 7px;
            height: 100%;
            background: linear-gradient(180deg, #991b1b 0%, #7f1d1d 100%);
        }

        .hero-card::after {
            content: "";
            position: absolute;
            right: -130px;
            top: -130px;
            width: 360px;
            height: 360px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.075), transparent 66%);
            pointer-events: none;
        }

        .hero-kicker {
            color: #fca5a5;
            font-size: 0.78rem;
            font-weight: 760;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.78rem;
        }

        .hero-title {
            color: #ffffff;
            font-size: 2.95rem;
            font-weight: 820;
            line-height: 1.04;
            letter-spacing: -0.035em;
            margin-bottom: 0.95rem;
        }

        .hero-subtitle {
            color: #dbe4ef;
            font-size: 1.04rem;
            line-height: 1.76;
            max-width: 1000px;
        }

        .hero-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1.35rem;
        }

        .hero-badge {
            padding: 0.44rem 0.86rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #f8fafc;
            font-size: 0.82rem;
            font-weight: 640;
            transition:
                transform 160ms ease,
                background 160ms ease,
                border-color 160ms ease;
        }

        .hero-badge:hover {
            transform: translateY(-1px);
            background: rgba(255, 255, 255, 0.13);
            border-color: rgba(255, 255, 255, 0.22);
        }

        /* ====================================================
           5. Metric cards
        ==================================================== */

        div[data-testid="stMetric"] {
            background:
                linear-gradient(180deg, #f3f6fa 0%, #e8eef5 100%);
            border: 1px solid rgba(71, 85, 105, 0.20);
            border-radius: 18px;
            padding: 1.22rem 1.35rem;
            box-shadow:
                0 15px 32px rgba(15, 23, 42, 0.11),
                inset 0 1px 0 rgba(255, 255, 255, 0.78);
            transition:
                transform 160ms ease,
                box-shadow 160ms ease,
                border-color 160ms ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: rgba(127, 29, 29, 0.28);
            box-shadow:
                0 20px 40px rgba(15, 23, 42, 0.14),
                inset 0 1px 0 rgba(255, 255, 255, 0.82);
        }

        div[data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 680;
        }

        div[data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 840;
            letter-spacing: -0.03em;
        }

        /* ====================================================
           6. Alerts
        ==================================================== */

        [data-testid="stSuccess"] {
            background: #d9efe5;
            border: 1px solid #9dd1b6;
            border-radius: 15px;
            color: #14532d;
            box-shadow: 0 10px 24px rgba(20, 83, 45, 0.07);
        }

        [data-testid="stSuccess"] p {
            color: #14532d !important;
        }

        [data-testid="stWarning"] {
            background: #f8ecd0;
            border: 1px solid #e0bf6c;
            border-radius: 15px;
            color: #78350f;
        }

        [data-testid="stInfo"] {
            background: #d7e4f4;
            border: 1px solid #9fb9da;
            border-radius: 15px;
            color: #1e3a8a;
        }

        /* ====================================================
           7. Tabs
        ==================================================== */

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid rgba(71, 85, 105, 0.30);
            margin-bottom: 1.1rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 44px;
            padding-left: 0.2rem;
            padding-right: 0.2rem;
            margin-right: 1rem;
            background: transparent;
            color: #475569;
            font-weight: 680;
            transition: color 140ms ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #111827;
        }

        .stTabs [aria-selected="true"] {
            color: #7f1d1d !important;
            border-bottom-color: #7f1d1d !important;
        }

        /* ====================================================
           8. Dataframes / tables
        ==================================================== */

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(30, 41, 59, 0.20);
            background: #111827;
            box-shadow: 0 18px 38px rgba(15, 23, 42, 0.16);
        }

        /* ====================================================
           9. Expanders
        ==================================================== */

        details {
            border-radius: 16px !important;
            border: 1px solid rgba(71, 85, 105, 0.24) !important;
            background: rgba(243, 246, 250, 0.92) !important;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.075);
            margin-bottom: 0.85rem;
            transition:
                transform 150ms ease,
                box-shadow 150ms ease,
                border-color 150ms ease;
        }

        details:hover {
            transform: translateY(-1px);
            border-color: rgba(127, 29, 29, 0.24) !important;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.10);
        }

        details summary {
            color: #111827 !important;
            font-weight: 720;
        }

        /* ====================================================
           10. Selectbox / inputs
        ==================================================== */

        div[data-baseweb="select"] > div {
            background: #f3f6fa !important;
            border: 1px solid rgba(71, 85, 105, 0.35) !important;
            border-radius: 13px !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        }

        div[data-baseweb="select"] > div:hover {
            border-color: rgba(127, 29, 29, 0.36) !important;
        }

        div[data-baseweb="select"] span {
            color: #111827 !important;
        }

        /* ====================================================
           11. Code blocks
        ==================================================== */

        code {
            color: #065f46 !important;
            background: #d9efe5 !important;
            border-radius: 7px !important;
            padding: 0.12rem 0.34rem !important;
        }

        pre {
            background: rgba(15, 23, 42, 0.07) !important;
            border: 1px solid rgba(71, 85, 105, 0.25) !important;
            border-radius: 12px !important;
        }

        /* ====================================================
           12. General refinements
        ==================================================== */

        hr {
            border-color: rgba(71, 85, 105, 0.30);
        }

        a {
            color: #7f1d1d;
        }

        ::selection {
            background: rgba(127, 29, 29, 0.20);
        }

        /* ====================================================
           13. Responsive behavior
        ==================================================== */

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1.4rem;
            }

            .hero-card {
                padding: 1.8rem 1.5rem;
                border-radius: 18px;
            }

            .hero-title {
                font-size: 2.15rem;
            }

            .hero-subtitle {
                font-size: 0.98rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """
    Renders the main dashboard hero section.
    """
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">Market Intelligence Dashboard</div>
            <div class="hero-title">Car Market Analysis Attica</div>
            <div class="hero-subtitle">
                Interactive overview of the used car market in Attica, based on
                the processed outputs of the analytical workflow. The dashboard
                brings together key indicators, price segments, charts and filters
                in a clean presentation environment.
            </div>
            <div class="hero-badge-row">
                <span class="hero-badge">Market KPIs</span>
                <span class="hero-badge">Price Segments</span>
                <span class="hero-badge">Charts & Filters</span>
                <span class="hero-badge">Thesis Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )