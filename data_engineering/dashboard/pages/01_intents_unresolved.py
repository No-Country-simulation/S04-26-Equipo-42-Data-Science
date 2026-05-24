import streamlit as st
import pandas as pd
import plotly.express as px
from app import load_data

st.set_page_config(page_title="Intenciones No Resueltas", layout="wide")
st.title("🎯 Intenciones No Resueltas")

df = load_data()

# Filtrar solo no resueltas
unresolved = df[df['resolved'] == 0]

# Top intenciones no resueltas
col1, col2 = st.columns(2)

with col1:
    intent_counts = unresolved['intencion'].value_counts().reset_index()
    intent_counts.columns = ['intencion', 'count']
    fig = px.bar(intent_counts, x='intencion', y='count', 
                title="Top Intenciones No Resueltas",
                color='count', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Intenciones no resueltas por flow
    intent_flow = unresolved.groupby(['flow_name', 'intencion']).size().reset_index(name='count')
    fig = px.bar(intent_flow, x='flow_name', y='count', color='intencion',
                title="Intenciones No Resueltas por Flow", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# Tabla detallada
st.subheader("📋 Detalle de Intenciones No Resueltas")
unresolved_summary = unresolved.groupby(['flow_name', 'intencion']).agg(
    total_mensajes=('texto_clean', 'count'),
    frustracion_promedio=('nivel_frustracion', 'mean'),
    churn_rate=('es_churn_risk', 'mean')
).reset_index()
st.dataframe(unresolved_summary, use_container_width=True)