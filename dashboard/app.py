"""
ConversaAI — Sentiment & Intent Analysis Dashboard

Entry point for the Streamlit dashboard. Imports and orchestrates
all tab modules.

Run:  streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Ensure project root is on sys.path so 'dashboard.' prefix imports resolve
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Local modules (dashboard. prefix required for Pylance static analysis)
from dashboard.data import load_metrics, load_session_data
from dashboard.sidebar import render_sidebar
from dashboard import overview, flows_intents, agents, trends, correlation, export

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
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    df = load_session_data()
    metrics = load_metrics()
    filtered_df = render_sidebar(df)

    tabs = st.tabs([
        "📊 Overview",
        "🔄 Flujos & Intents",
        "👤 Agentes",
        "📈 Tendencias",
        "🔗 Correlaciones",
        "📥 Exportar",
    ])

    with tabs[0]:
        overview.render(filtered_df, metrics)
    with tabs[1]:
        flows_intents.render(filtered_df)
    with tabs[2]:
        agents.render(filtered_df)
    with tabs[3]:
        trends.render(filtered_df)
    with tabs[4]:
        correlation.render(filtered_df)
    with tabs[5]:
        export.render(filtered_df, metrics)


if __name__ == "__main__":
    main()
