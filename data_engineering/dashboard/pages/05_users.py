"""
Análisis por Usuario/Agente
Muestra los usuarios más activos y sus métricas de frustración
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from app import load_data

st.set_page_config(page_title="Análisis por Usuario", layout="wide")
st.title("👥 Análisis por Usuario/Agente")

df = load_data()

# ==================== MÉTRICAS GENERALES ====================
st.header("📊 Estadísticas de Usuarios")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Usuarios únicos", df['usuario'].nunique())

with col2:
    # Usuario más activo
    top_user = df['usuario'].value_counts().idxmax()
    top_user_msgs = df['usuario'].value_counts().max()
    st.metric("Usuario más activo", top_user, f"{top_user_msgs} mensajes")

with col3:
    # Frustración promedio por usuario
    avg_frust = df.groupby('usuario')['nivel_frustracion'].mean().mean()
    st.metric("Frustración promedio global", f"{avg_frust:.2f}")

st.markdown("---")

# ==================== TOP USUARIOS MÁS ACTIVOS ====================
st.subheader("📈 Top 15 Usuarios Más Activos")

user_activity = df.groupby('usuario').agg(
    total_mensajes=('texto_clean', 'count'),
    frustracion_promedio=('nivel_frustracion', 'mean'),
    tasa_churn=('es_churn_risk', 'mean'),
    tasa_resolucion=('resolved', 'mean')
).reset_index()

user_activity = user_activity.sort_values('total_mensajes', ascending=False).head(15)

fig = px.bar(user_activity, x='usuario', y='total_mensajes',
             title="Top 15 Usuarios por Cantidad de Mensajes",
             color='frustracion_promedio', color_continuous_scale='Reds',
             labels={'usuario': 'Usuario', 'total_mensajes': 'Mensajes'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== TOP USUARIOS MÁS FRUSTRADOS ====================
st.subheader("😤 Top 15 Usuarios con Mayor Frustración Promedio")

# Filtrar usuarios con al menos 5 mensajes para evitar ruido
user_frustration = df.groupby('usuario').agg(
    total_mensajes=('texto_clean', 'count'),
    frustracion_promedio=('nivel_frustracion', 'mean')
).reset_index()
user_frustration = user_frustration[user_frustration['total_mensajes'] >= 5]
user_frustration = user_frustration.sort_values('frustracion_promedio', ascending=False).head(15)

fig = px.bar(user_frustration, x='usuario', y='frustracion_promedio',
             title="Top 15 Usuarios con Mayor Frustración Promedio (mín. 5 mensajes)",
             color='frustracion_promedio', color_continuous_scale='Reds',
             labels={'usuario': 'Usuario', 'frustracion_promedio': 'Frustración promedio'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== TABLA COMPLETA ====================
st.subheader("📋 Tabla de Métricas por Usuario")

# Mostrar tabla con opción de búsqueda
search = st.text_input("🔍 Buscar usuario", placeholder="Escribe parte del nombre...")

user_metrics = df.groupby('usuario').agg(
    mensajes=('texto_clean', 'count'),
    frustracion_promedio=('nivel_frustracion', 'mean'),
    frustracion_alta=('nivel_frustracion', lambda x: (x == 2).mean() * 100),
    churn_rate=('es_churn_risk', 'mean'),
    resolucion_rate=('resolved', 'mean')
).reset_index()

user_metrics.columns = ['usuario', 'mensajes', 'frustracion_promedio', 'frustracion_alta_%', 'churn_rate', 'resolucion_rate']

# Redondear
user_metrics['frustracion_promedio'] = user_metrics['frustracion_promedio'].round(2)
user_metrics['frustracion_alta_%'] = user_metrics['frustracion_alta_%'].round(1)
user_metrics['churn_rate'] = (user_metrics['churn_rate'] * 100).round(1)
user_metrics['resolucion_rate'] = (user_metrics['resolucion_rate'] * 100).round(1)

# Filtrar por búsqueda
if search:
    user_metrics = user_metrics[user_metrics['usuario'].str.contains(search, case=False)]

st.dataframe(user_metrics, use_container_width=True)

# ==================== DESCARGA ====================
csv = user_metrics.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar métricas de usuarios (CSV)",
    data=csv,
    file_name="user_metrics.csv",
    mime="text/csv"
)