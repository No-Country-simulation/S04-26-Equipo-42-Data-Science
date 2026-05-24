"""
ConversaAI Dashboard — Tab 4: Temporal Trends.

Monthly frustration, churn, resolution, and per-flow trends.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.config import SYNTHETIC_NOTE


def render(filtered_df) -> None:
    """Render the Temporal Trends tab."""
    st.markdown(SYNTHETIC_NOTE)

    # Ensure we treat months as ordered categories
    filtered_df = filtered_df.copy()
    filtered_df["month"] = pd.Categorical(
        filtered_df["month"],
        categories=sorted(filtered_df["month"].unique()),
        ordered=True,
    )

    # Monthly aggregation
    monthly = (
        filtered_df.groupby("month")
        .agg(
            sesiones=("session_id", "count"),
            frust_prom=("max_frustracion", "mean"),
            resolucion=("any_resolved", "mean"),
            churn=("any_churn", "mean"),
        )
        .round(3)
        .reset_index()
    )
    monthly["month_str"] = monthly["month"].astype(str)

    col_left, col_right = st.columns(2)

    with col_left:
        fig = px.line(
            monthly,
            x="month_str",
            y="frust_prom",
            title="Frustracion Promedio por Mes",
            markers=True,
            labels={"month_str": "Mes", "frust_prom": "Frustracion prom."},
        )
        fig.update_traces(line_color="#e74c3c", line_width=3)
        fig.update_layout(yaxis_range=[0, 2])
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Churn & resolution over time
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=monthly["month_str"],
                y=monthly["churn"],
                mode="lines+markers",
                name="Churn rate",
                line=dict(color="#e74c3c", width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=monthly["month_str"],
                y=monthly["resolucion"],
                mode="lines+markers",
                name="Resolucion",
                line=dict(color="#2ecc71", width=3),
            )
        )
        fig.update_layout(
            title="Churn y Resolucion por Mes",
            xaxis_title="Mes",
            yaxis_title="Tasa",
            yaxis=dict(tickformat=".0%"),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Frustration by flow over time
    frust_by_flow_month = (
        filtered_df.groupby(["month", "flow_name"])["max_frustracion"]
        .mean()
        .round(3)
        .reset_index()
    )
    frust_by_flow_month["month_str"] = frust_by_flow_month["month"].astype(str)

    fig = px.line(
        frust_by_flow_month,
        x="month_str",
        y="max_frustracion",
        color="flow_name",
        title="Frustracion por Flujo a lo Largo del Tiempo",
        markers=True,
        color_discrete_sequence=list(px.colors.qualitative.Set2),
        labels={
            "month_str": "Mes",
            "max_frustracion": "Frustracion prom.",
            "flow_name": "Flujo",
        },
    )
    fig.update_layout(yaxis_range=[0, 2])
    st.plotly_chart(fig, use_container_width=True)
