"""
ConversaAI Dashboard — Sidebar filter controls.

Renders the sidebar with flow, intent, frustration level,
and date range filters. Returns a filtered DataFrame.
"""

from __future__ import annotations

import streamlit as st

from dashboard.config import SYNTHETIC_NOTE


def render_sidebar(df):
    """Render sidebar filters and return a filtered DataFrame."""
    # ------------------------------------------------------------------
    # Header: logo, title, subtitle
    # ------------------------------------------------------------------
    st.sidebar.image(
        "https://img.icons8.com/fluency/96/chatbot.png", width=60
    )
    st.sidebar.title("ConversaAI")
    st.sidebar.caption("Sentiment & Intent Analysis")

    st.sidebar.divider()
    st.sidebar.subheader("Filtros")

    # ------------------------------------------------------------------
    # Flow filter
    # ------------------------------------------------------------------
    flows = sorted(df["flow_name"].dropna().unique())
    selected_flows = st.sidebar.multiselect(
        "Flujo",
        options=flows,
        default=flows,
    )

    # ------------------------------------------------------------------
    # Intent filter
    # ------------------------------------------------------------------
    intents = sorted(df["intencion"].dropna().unique())
    selected_intents = st.sidebar.multiselect(
        "Intencion",
        options=intents,
        default=intents,
    )

    # ------------------------------------------------------------------
    # Frustration range slider
    # ------------------------------------------------------------------
    frust_range = st.sidebar.slider(
        "Rango de frustracion",
        min_value=0,
        max_value=2,
        value=(0, 2),
        step=1,
    )

    # ------------------------------------------------------------------
    # Date range
    # ------------------------------------------------------------------
    min_date = df["fecha"].min().date()
    max_date = df["fecha"].max().date()
    date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # ------------------------------------------------------------------
    # Apply filters
    # ------------------------------------------------------------------
    mask = df["flow_name"].isin(selected_flows)
    mask &= df["intencion"].isin(selected_intents)
    mask &= df["max_frustracion"].between(frust_range[0], frust_range[1])

    if len(date_range) == 2:
        start, end = date_range
        mask &= df["fecha"].dt.date >= start
        mask &= df["fecha"].dt.date <= end

    st.sidebar.divider()
    st.sidebar.metric(
        "Sesiones filtradas",
        f"{mask.sum():,} / {len(df):,}",
    )

    st.sidebar.divider()
    st.sidebar.caption(SYNTHETIC_NOTE)

    return df[mask].copy()
