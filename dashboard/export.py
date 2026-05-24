"""
ConversaAI Dashboard — Tab 6: Export.

Download filtered CSV, metrics JSON, and executive summary markdown.
"""

from __future__ import annotations

import json

import streamlit as st

from dashboard.config import SYNTHETIC_NOTE


def render(filtered_df, metrics: dict) -> None:
    """Render the Export tab."""
    st.markdown(SYNTHETIC_NOTE)

    st.subheader("Exportar datos filtrados")

    col_left, col_right = st.columns(2)

    with col_left:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV (datos filtrados)",
            data=csv,
            file_name="conversaai_sesiones_filtradas.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_right:
        metrics_json = json.dumps(metrics, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Descargar metrics.json",
            data=metrics_json,
            file_name="pattern_metrics.json",
            mime="application/json",
            use_container_width=True,
        )

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.metric("Sesiones en filtro actual", f"{len(filtered_df):,}")
        st.metric(
            "Churn rate (filtro)",
            f"{(filtered_df['any_churn'] == 1).mean():.1%}",
        )

    with col_right:
        st.metric(
            "Resolucion (filtro)",
            f"{(filtered_df['any_resolved'] == 1).mean():.1%}",
        )
        st.metric(
            "Frustracion prom. (filtro)",
            f"{filtered_df['max_frustracion'].mean():.2f}",
        )

    st.divider()

    # Resumen markdown
    st.subheader("Resumen ejecutivo")
    summary_lines = [
        "# Resumen ConversaAI",
        "",
        f"**Periodo:** {filtered_df['fecha'].min().date()} a {filtered_df['fecha'].max().date()}",
        f"**Sesiones analizadas:** {len(filtered_df):,}",
        f"**Agentes unicos:** {filtered_df['usuario'].nunique():,}",
        f"**Churn rate:** {(filtered_df['any_churn'] == 1).mean():.1%}",
        f"**Resolucion:** {(filtered_df['any_resolved'] == 1).mean():.1%}",
        f"**Frustracion promedio:** {filtered_df['max_frustracion'].mean():.2f}",
        f"**Turnos promedio por sesion:** {filtered_df['num_turns'].mean():.1f}",
        "",
        "*Datos sinteticos — los valores reflejan reglas de construccion, no comportamiento real*",
    ]
    summary_md = "\n".join(summary_lines)
    st.download_button(
        label="📄 Descargar resumen (.md)",
        data=summary_md,
        file_name="resumen_conversaai.md",
        mime="text/markdown",
        use_container_width=True,
    )
