import streamlit as st
import pandas as pd
import plotly.express as px
from app import load_data

st.set_page_config(page_title="Picos de Frustración", layout="wide")
st.title("📈 Picos de Frustración")

df = load_data()
df['fecha'] = pd.to_datetime(df['fecha'])

# Frustración por día
frust_daily = df.groupby(df['fecha'].dt.date).agg(
    frustracion_promedio=('nivel_frustracion', 'mean'),
    frustracion_alta=('nivel_frustracion', lambda x: (x == 2).mean() * 100),
    total_mensajes=('texto_clean', 'count')
).reset_index()

# Detectar picos (frustración > 1.5)
frust_daily['pico'] = frust_daily['frustracion_promedio'] > 1.5

col1, col2 = st.columns(2)

with col1:
    fig = px.line(frust_daily, x='fecha', y='frustracion_promedio',
                title="Evolución de Frustración Promedio",
                markers=True)
    # Marcar picos
    picos = frust_daily[frust_daily['pico']]
    fig.add_scatter(x=picos['fecha'], y=picos['frustracion_promedio'],
                    mode='markers', marker=dict(color='red', size=12),
                    name='Pico (>1.5)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(frust_daily, x='fecha', y='frustracion_alta',
                title="% de Frustración Alta por Día",
                color='frustracion_alta', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

st.info("🔔 **Picos detectados:** Días donde la frustración promedio supera 1.5 (umbral configurable)")