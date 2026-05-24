"""
ConversaAI — Sentiment & Intent Analysis Dashboard

Dashboard interactivo con Streamlit + Plotly para explorar los patrones
de frustracion, intencion, churn y resolucion en sesiones de soporte.

Fuente: reports/session_aggregated.csv + reports/pattern_metrics.json
Ejecutar: streamlit run dashboard/app.py
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "reports" / "session_aggregated.csv"
METRICS_PATH = BASE_DIR / "reports" / "pattern_metrics.json"

SYNTHETIC_NOTE = (
    "**Nota:** Este dataset es sintetico/determinista. "
    "Los patrones mostrados reflejan reglas de construccion, "
    "no comportamiento real de usuarios. Con datos reales, "
    "las correlaciones seran mas debiles y variables."
)

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["max_frustracion"] = df["max_frustracion"].astype(int)

    with open(METRICS_PATH) as f:
        metrics = json.load(f)

    return df, metrics


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
COLORS = {
    "Resuelto": "#2ecc71",
    "Churn": "#e74c3c",
    "Activo": "#f39c12",
    "flow": list(px.colors.qualitative.Set2[:4]),
    "frust": ["#27ae60", "#f1c40f", "#e74c3c"],
}
FRUST_LABELS = {0: "Baja (0)", 1: "Media (1)", 2: "Alta (2)"}

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ConversaAI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
def render_sidebar(df):
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/chatbot.png", width=60)
        st.title("ConversaAI")
        st.caption("Sentiment & Intent Analysis")

        st.divider()
        st.subheader("Filtros")

        selected_flows = st.multiselect(
            "Flujo de soporte",
            options=sorted(df["flow_name"].unique()),
            default=sorted(df["flow_name"].unique()),
        )

        selected_intents = st.multiselect(
            "Intencion",
            options=sorted(df["intencion"].unique()),
            default=sorted(df["intencion"].unique()),
        )

        frust_levels = st.slider(
            "Frustracion maxima minima",
            min_value=0,
            max_value=2,
            value=(0, 2),
        )

        date_min = df["fecha"].min().date()
        date_max = df["fecha"].max().date()
        date_range = st.date_input(
            "Rango de fechas",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max,
        )

        st.divider()
        st.caption(SYNTHETIC_NOTE)

    # Apply filters
    mask = pd.Series(True, index=df.index)
    if selected_flows:
        mask &= df["flow_name"].isin(selected_flows)
    if selected_intents:
        mask &= df["intencion"].isin(selected_intents)
    mask &= df["max_frustracion"].between(frust_levels[0], frust_levels[1])
    if len(date_range) == 2:
        mask &= df["fecha"].between(
            pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        )

    return df[mask].copy()


# ---------------------------------------------------------------------------
# TAB 1 — Overview
# ---------------------------------------------------------------------------
def render_overview(filtered_df, metrics):
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
            st.metric("Frustracion global (turno)", metrics["overall_frustration_mean"])
            st.metric("Resolucion global (turno)", f"{metrics['overall_resolved_rate']:.1%}")
        with col_c:
            st.metric("Churn global (turno)", f"{metrics['overall_churn_rate']:.1%}")
            st.metric("Sesiones activas", metrics["sessions_active"])


# ---------------------------------------------------------------------------
# TAB 2 — Flows & Intents
# ---------------------------------------------------------------------------
def render_flows_intents(filtered_df):
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
        fig.update_layout(showlegend=False, xaxis_title="", yaxis=dict(tickformat=".0%"))
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


# ---------------------------------------------------------------------------
# TAB 3 — Agents
# ---------------------------------------------------------------------------
def render_agents(filtered_df):
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


# ---------------------------------------------------------------------------
# TAB 4 — Temporal Trends
# ---------------------------------------------------------------------------
def render_trends(filtered_df):
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


# ---------------------------------------------------------------------------
# TAB 5 — Correlation Matrix
# ---------------------------------------------------------------------------
def render_correlation(filtered_df):
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


# ---------------------------------------------------------------------------
# TAB 6 — Export
# ---------------------------------------------------------------------------
def render_export(filtered_df, metrics):
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    df, metrics = load_data()
    filtered_df = render_sidebar(df)

    tabs = st.tabs(
        [
            "📊 Overview",
            "🔄 Flujos & Intents",
            "👤 Agentes",
            "📈 Tendencias",
            "🔗 Correlaciones",
            "📥 Exportar",
        ]
    )

    with tabs[0]:
        render_overview(filtered_df, metrics)

    with tabs[1]:
        render_flows_intents(filtered_df)

    with tabs[2]:
        render_agents(filtered_df)

    with tabs[3]:
        render_trends(filtered_df)

    with tabs[4]:
        render_correlation(filtered_df)

    with tabs[5]:
        render_export(filtered_df, metrics)


if __name__ == "__main__":
    main()
