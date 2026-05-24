"""
ConversaAI Dashboard — Tab 5: Correlation Matrix.

Cross-correlation heatmap with strip plots for key variable pairs.
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard.config import SYNTHETIC_NOTE


def render(filtered_df) -> None:
    """Render the Correlation Matrix tab."""
    st.markdown(SYNTHETIC_NOTE)

    corr_vars = ["max_frustracion", "any_resolved", "any_churn", "num_turns"]
    corr_labels = {
        "max_frustracion": "Frustracion",
        "any_resolved": "Resuelto",
        "any_churn": "Churn",
        "num_turns": "Turnos",
    }

    corr_matrix = filtered_df[corr_vars].corr().round(3)
    corr_matrix = corr_matrix.rename(index=corr_labels, columns=corr_labels)

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Matriz de Correlacion Cruzada (Nivel Sesion)",
        labels={"color": "Correlacion"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        # Scatter: frustration vs resolution
        jitter = filtered_df.sample(min(1000, len(filtered_df)), random_state=42)
        fig = px.strip(
            jitter,
            x="max_frustracion",
            y="any_resolved",
            title="Frustracion vs Resolucion (strip plot, n=1000)",
            labels={
                "max_frustracion": "Frustracion maxima",
                "any_resolved": "Resuelto (0/1)",
            },
            color="max_frustracion",
        )
        fig.update_layout(coloraxis=dict(colorscale="RdYlGn_r"))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Scatter: frustration vs churn
        fig = px.strip(
            jitter,
            x="max_frustracion",
            y="any_churn",
            title="Frustracion vs Churn (strip plot, n=1000)",
            labels={
                "max_frustracion": "Frustracion maxima",
                "any_churn": "Churn (0/1)",
            },
            color="max_frustracion",
        )
        fig.update_layout(coloraxis=dict(colorscale="RdYlGn_r"))
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**Interpretacion:** Frustracion-Churn = 1.000 y Frustracion-Resolucion = -0.997 "
        "confirman la naturaleza determinista del dataset. "
        "Con datos reales, estas correlaciones serian notablemente mas debiles."
    )
