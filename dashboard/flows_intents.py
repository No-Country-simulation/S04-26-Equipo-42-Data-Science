"""
ConversaAI Dashboard — Tab 2: Flows & Intents.

Per-flow comparison tables, frustration by flow, churn/resolution by intent.
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard.config import COLORS, FRUST_LABELS, SYNTHETIC_NOTE


def render(filtered_df) -> None:
    """Render the Flows & Intents tab."""
    st.markdown(SYNTHETIC_NOTE)

    # Summary table
    st.subheader("Comparativa por flujo")
    summary = (
        filtered_df.groupby("flow_name")
        .agg(
            sesiones=("session_id", "count"),
            churn_rate=("any_churn", "mean"),
            resolucion=("any_resolved", "mean"),
            frust_prom=("max_frustracion", "mean"),
            turnos_prom=("num_turns", "mean"),
        )
        .round(3)
        .reset_index()
    )
    summary.columns = [
        "Flujo",
        "Sesiones",
        "Churn Rate",
        "Resolucion",
        "Frust Prom",
        "Turnos Prom",
    ]
    summary["Churn Rate"] = summary["Churn Rate"].apply(lambda x: f"{x:.1%}")
    summary["Resolucion"] = summary["Resolucion"].apply(lambda x: f"{x:.1%}")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # Frustration by flow (stacked bar)
        frust_by_flow = (
            filtered_df.groupby(["flow_name", "max_frustracion"])
            .size()
            .reset_index(name="count")
        )
        frust_by_flow["frust_label"] = frust_by_flow["max_frustracion"].map(
            FRUST_LABELS
        )
        fig = px.bar(
            frust_by_flow,
            x="flow_name",
            y="count",
            color="frust_label",
            title="Frustracion por Flujo",
            color_discrete_sequence=COLORS["frust"],
            barmode="stack",
            text_auto=True,
        )
        fig.update_layout(xaxis_title="", yaxis_title="Sesiones")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Churn rate by intent
        churn_by_intent = (
            filtered_df.groupby("intencion")["any_churn"]
            .mean()
            .reset_index()
        )
        churn_by_intent.columns = ["intencion", "churn_rate"]
        fig = px.bar(
            churn_by_intent,
            x="intencion",
            y="churn_rate",
            title="Churn Rate por Intencion",
            color="intencion",
            color_discrete_sequence=COLORS["flow"],
            text_auto=True,
        )
        fig.update_traces(texttemplate="%{y:.0%}", textposition="outside")
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Churn rate",
            yaxis=dict(tickformat=".0%"),
        )
        st.plotly_chart(fig, use_container_width=True)

    col_left2, col_right2 = st.columns(2)

    with col_left2:
        # Resolution rate by flow
        res_by_flow = (
            filtered_df.groupby("flow_name")["any_resolved"]
            .mean()
            .reset_index()
        )
        res_by_flow.columns = ["flow", "resolved_rate"]
        fig = px.bar(
            res_by_flow,
            x="flow",
            y="resolved_rate",
            title="Tasa de Resolucion por Flujo",
            color="flow",
            color_discrete_sequence=list(px.colors.qualitative.Set2),
            text_auto=True,
        )
        fig.update_traces(texttemplate="%{y:.0%}", textposition="outside")
        fig.update_layout(
            showlegend=False, xaxis_title="", yaxis=dict(tickformat=".0%")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        # Outcome by intent
        outcome_intent = (
            filtered_df.groupby(["intencion", "outcome"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            outcome_intent,
            x="intencion",
            y="count",
            color="outcome",
            title="Outcome por Intencion",
            color_discrete_map=COLORS,
            barmode="stack",
            text_auto=True,
        )
        fig.update_layout(xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
