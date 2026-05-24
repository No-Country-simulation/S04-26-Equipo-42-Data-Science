"""
ConversaAI Dashboard — Tab 3: Agents.

Agent-level aggregation, scatter plot, churn/resolution leaderboards, table.
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard.config import SYNTHETIC_NOTE


def render(filtered_df) -> None:
    """Render the Agents tab."""
    st.markdown(SYNTHETIC_NOTE)

    # Agent-level aggregation
    agent_stats = (
        filtered_df.groupby("usuario")
        .agg(
            sesiones=("session_id", "count"),
            frust_prom=("max_frustracion", "mean"),
            resolucion=("any_resolved", "mean"),
            churn_rate=("any_churn", "mean"),
            turnos_prom=("num_turns", "mean"),
        )
        .round(3)
        .reset_index()
    )

    # Agent search
    search = st.text_input("Buscar agente por nombre", placeholder="@usuario...")
    if search:
        agent_stats = agent_stats[
            agent_stats["usuario"].str.contains(search, case=False, na=False)
        ]

    # Top 20 by volume
    top_agents = agent_stats.nlargest(20, "sesiones")

    col_left, col_right = st.columns(2)

    with col_left:
        fig = px.scatter(
            top_agents,
            x="sesiones",
            y="frust_prom",
            size="sesiones",
            color="resolucion",
            hover_name="usuario",
            hover_data={
                "sesiones": True,
                "frust_prom": ":.2f",
                "resolucion": ":.0%",
                "churn_rate": ":.0%",
            },
            title="Top 20 Agentes por Volumen — Frustracion vs Sesiones",
            labels={
                "sesiones": "Sesiones",
                "frust_prom": "Frustracion prom.",
                "resolucion": "Resolucion",
            },
        )
        fig.update_layout(coloraxis=dict(colorscale="RdYlGn_r"))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Top 10 churn rate
        top_churn = agent_stats.nlargest(10, "churn_rate")
        fig = px.bar(
            top_churn,
            x="churn_rate",
            y="usuario",
            title="Top 10 Agentes — Mayor Churn Rate",
            color="churn_rate",
            text_auto=True,
            orientation="h",
        )
        fig.update_traces(texttemplate="%{x:.0%}", textposition="outside")
        fig.update_layout(
            xaxis_title="Churn rate",
            yaxis_title="",
            xaxis=dict(tickformat=".0%"),
            coloraxis=dict(colorscale="Reds"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 resolution rate
    st.divider()
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        top_res = agent_stats.nlargest(10, "resolucion")
        fig = px.bar(
            top_res,
            x="resolucion",
            y="usuario",
            title="Top 10 Agentes — Mayor Resolucion",
            color="resolucion",
            text_auto=True,
            orientation="h",
        )
        fig.update_traces(texttemplate="%{x:.0%}", textposition="outside")
        fig.update_layout(
            xaxis_title="Resolucion",
            yaxis_title="",
            xaxis=dict(tickformat=".0%"),
            coloraxis=dict(colorscale="Greens"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        # Agents table
        st.subheader("Tabla de agentes")
        display_cols = [
            "usuario",
            "sesiones",
            "frust_prom",
            "resolucion",
            "churn_rate",
            "turnos_prom",
        ]
        display = agent_stats[display_cols].copy()
        display.columns = [
            "Agente",
            "Sesiones",
            "Frust Prom",
            "Resolucion",
            "Churn",
            "Turnos Prom",
        ]
        display["Resolucion"] = display["Resolucion"].apply(lambda x: f"{x:.0%}")
        display["Churn"] = display["Churn"].apply(lambda x: f"{x:.0%}")
        display["Frust Prom"] = display["Frust Prom"].apply(lambda x: f"{x:.2f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
