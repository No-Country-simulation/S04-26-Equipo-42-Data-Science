"""
ConversaAI Dashboard — Tab 1: Overview.

High-level KPIs, outcome distribution, and frustration breakdown.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, FRUST_LABELS


def render(filtered_df: pd.DataFrame, metrics: dict) -> None:
    """Render the Overview tab."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sesiones", f"{len(filtered_df):,}")
    with col2:
        churn_rate = (filtered_df["any_churn"] == 1).mean()
        st.metric("Churn Rate", f"{churn_rate:.1%}")
    with col3:
        resolved_rate = (filtered_df["any_resolved"] == 1).mean()
        st.metric("Resolucion", f"{resolved_rate:.1%}")
    with col4:
        avg_frust = filtered_df["max_frustracion"].mean()
        st.metric("Frustracion Prom.", f"{avg_frust:.2f}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        # Outcome distribution (doughnut)
        outcome_counts = filtered_df["outcome"].value_counts().reset_index()
        outcome_counts.columns = ["outcome", "count"]
        fig = px.pie(
            outcome_counts,
            values="count",
            names="outcome",
            title="Distribucion de Outcomes",
            color="outcome",
            color_discrete_map=COLORS,
            hole=0.4,
        )
        fig.update_traces(textinfo="label+percent", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Frustration distribution (bar)
        frust_counts = (
            filtered_df["max_frustracion"]
            .value_counts()
            .sort_index()
            .reset_index()
        )
        frust_counts.columns = ["nivel", "count"]
        frust_counts["label"] = frust_counts["nivel"].map(FRUST_LABELS)
        fig = px.bar(
            frust_counts,
            x="label",
            y="count",
            title="Distribucion de Frustracion Maxima",
            color="label",
            color_discrete_sequence=COLORS["frust"],
            text_auto=True,
        )
        fig.update_layout(showlegend=False, xaxis_title="Nivel de frustracion")
        st.plotly_chart(fig, use_container_width=True)

    # Global metrics from JSON
    st.divider()
    with st.expander("Metricas globales (pattern_metrics.json)"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Turnos totales", f"{metrics['total_turns']:,}")
            st.metric("Prom. turnos/sesion", metrics["avg_turns_per_session"])
        with col_b:
            st.metric(
                "Frustracion global (turno)", metrics["overall_frustration_mean"]
            )
            st.metric(
                "Resolucion global (turno)",
                f"{metrics['overall_resolved_rate']:.1%}",
            )
        with col_c:
            st.metric("Churn global (turno)", f"{metrics['overall_churn_rate']:.1%}")
            st.metric("Sesiones activas", metrics["sessions_active"])
