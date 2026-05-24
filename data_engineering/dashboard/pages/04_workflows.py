import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from app import load_data

st.set_page_config(page_title="Análisis por Workflow", layout="wide")
st.title("🔧 Análisis por Workflow")

df = load_data()

# Métricas por workflow (a nivel sesión)
last_turn = df.loc[df.groupby('session_id')['turn_number'].idxmax()]
workflow_metrics = last_turn.groupby('flow_name').agg(
    sesiones=('session_id', 'count'),
    tasa_churn=('es_churn_risk', 'mean'),
    tasa_resolucion=('resolved', 'mean'),
    frustracion_promedio=('nivel_frustracion', 'mean')
).reset_index()

# Convertir a porcentajes
workflow_metrics['tasa_churn_pct'] = workflow_metrics['tasa_churn'] * 100
workflow_metrics['tasa_resolucion_pct'] = workflow_metrics['tasa_resolucion'] * 100

# Gráfico comparativo
fig = make_subplots(rows=1, cols=2, subplot_titles=("Tasa de Churn", "Tasa de Resolución"))

fig.add_trace(go.Bar(x=workflow_metrics['flow_name'], y=workflow_metrics['tasa_churn_pct'],
                    name="Churn", marker_color='crimson'), row=1, col=1)
fig.add_trace(go.Bar(x=workflow_metrics['flow_name'], y=workflow_metrics['tasa_resolucion_pct'],
                    name="Resolución", marker_color='forestgreen'), row=1, col=2)

fig.update_layout(height=500, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Ranking de workflows problemáticos
st.subheader("🏆 Ranking de Workflows Problemáticos")
workflow_metrics['problema_score'] = (workflow_metrics['tasa_churn'] + 
                                    (1 - workflow_metrics['tasa_resolucion']) +
                                    workflow_metrics['frustracion_promedio']/2)
workflow_metrics = workflow_metrics.sort_values('problema_score', ascending=False)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Flow más problemático", workflow_metrics.iloc[0]['flow_name'],
            f"Score: {workflow_metrics.iloc[0]['problema_score']:.2f}")
with col2:
    st.metric("Flow con más churn", workflow_metrics.loc[workflow_metrics['tasa_churn'].idxmax(), 'flow_name'],
            f"{workflow_metrics['tasa_churn'].max()*100:.1f}%")
with col3:
    st.metric("Flow con peor resolución", workflow_metrics.loc[workflow_metrics['tasa_resolucion'].idxmin(), 'flow_name'],
            f"{workflow_metrics['tasa_resolucion'].min()*100:.1f}%")

st.dataframe(workflow_metrics, use_container_width=True)