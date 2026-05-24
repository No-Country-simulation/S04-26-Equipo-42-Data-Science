import streamlit as st
import pandas as pd
import plotly.express as px
from app import load_data

st.set_page_config(page_title="Tendencias Temporales", layout="wide")
st.title("📅 Tendencias Temporales")

df = load_data()
df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.to_period('M').astype(str)
df['semana'] = df['fecha'].dt.to_period('W').astype(str)

# Selector de granularidad
granularidad = st.selectbox("Granularidad", ["Diario", "Semanal", "Mensual"])

if granularidad == "Diario":
    df['periodo'] = df['fecha'].dt.date
elif granularidad == "Semanal":
    df['periodo'] = df['semana']
else:
    df['periodo'] = df['mes']

# Métricas por período
trends = df.groupby('periodo').agg(
    frustracion_promedio=('nivel_frustracion', 'mean'),
    churn_rate=('es_churn_risk', 'mean'),
    resolucion_rate=('resolved', 'mean'),
    total=('texto_clean', 'count')
).reset_index()

col1, col2 = st.columns(2)

with col1:
    fig = px.line(trends, x='periodo', y='frustracion_promedio',
                title=f"Evolución de Frustración ({granularidad})",
                markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(trends, x='periodo', y=['churn_rate', 'resolucion_rate'],
                title=f"Churn vs Resolución ({granularidad})",
                markers=True, labels={'value': 'Tasa', 'variable': 'Métrica'})
    st.plotly_chart(fig, use_container_width=True)

# Volumen de mensajes
fig = px.bar(trends, x='periodo', y='total',
            title=f"Volumen de Mensajes ({granularidad})",
            color='total', color_continuous_scale='Blues')
st.plotly_chart(fig, use_container_width=True)