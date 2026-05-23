import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import json

# Configuración de página
st.set_page_config(
    page_title="ConversaAI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ConversaAI - Análisis de Conversaciones de Soporte")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_parquet("../data/processed/data_processed.parquet")
    return df

@st.cache_resource
def load_model():
    model = joblib.load("../models/frustration_model.pkl")
    return model

df = load_data()

# ==================== KPIs Globales ====================
st.header("📈 KPIs Globales")
col1, col2, col3, col4, col5 = st.columns(5)

total_sesiones = df['session_id'].nunique()
tasa_churn = (df[df['turn_number']==df.groupby('session_id')['turn_number'].transform('max')]['es_churn_risk'].mean() * 100)
tasa_resolucion = (df[df['turn_number']==df.groupby('session_id')['turn_number'].transform('max')]['resolved'].mean() * 100)
frustracion_alta_pct = (df['nivel_frustracion'] == 2).mean() * 100
total_mensajes = len(df)

col1.metric("Sesiones", f"{total_sesiones:,}")
col2.metric("Tasa de Churn", f"{tasa_churn:.1f}%")
col3.metric("Tasa de Resolución", f"{tasa_resolucion:.1f}%")
col4.metric("Frustración Alta", f"{frustracion_alta_pct:.1f}%")
col5.metric("Total Mensajes", f"{total_mensajes:,}")

st.markdown("---")

# ==================== Filtros ====================
st.sidebar.header("Filtros")
flows = st.sidebar.multiselect(
    "Flows",
    options=df['flow_name'].unique(),
    default=df['flow_name'].unique()
)
fechas = pd.to_datetime(df['fecha'])
min_date = fechas.min()
max_date = fechas.max()
date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Aplicar filtros
df_filtered = df[df['flow_name'].isin(flows)]
if len(date_range) == 2:
    mask = (pd.to_datetime(df_filtered['fecha']) >= pd.to_datetime(date_range[0])) & \
        (pd.to_datetime(df_filtered['fecha']) <= pd.to_datetime(date_range[1]))
    df_filtered = df_filtered[mask]

st.sidebar.markdown("---")
st.sidebar.info("Dashboard basado en datos sintéticos. Pipeline listo para datos reales.")

# ==================== Gráfico 1: Distribución por Flow ====================
st.header("📊 Distribución por Flow")

col1, col2 = st.columns(2)

with col1:
    flow_counts = df_filtered['flow_name'].value_counts().reset_index()
    flow_counts.columns = ['flow_name', 'count']
    fig = px.pie(flow_counts, values='count', names='flow_name', title="Mensajes por Flow")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    frust_by_flow = df_filtered.groupby('flow_name')['nivel_frustracion'].mean().sort_values().reset_index()
    fig = px.bar(frust_by_flow, x='flow_name', y='nivel_frustracion', 
                title="Frustración Promedio por Flow", color='nivel_frustracion')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== Gráfico 2: Frustración por Turno ====================
st.header("📉 Patrón de Frustración por Turno")

frust_by_turn = df_filtered.groupby('turn_number')['nivel_frustracion'].agg(['mean', 'count']).reset_index()
fig = px.line(frust_by_turn, x='turn_number', y='mean', 
              markers=True, title="Frustración Promedio por Turno",
              labels={'mean': 'Frustración promedio', 'turn_number': 'Número de turno'})
fig.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Umbral medio")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== Gráfico 3: Intención vs Flow ====================
st.header("🎯 Relación Intención vs Flow")

intent_flow = df_filtered.groupby(['flow_name', 'intencion']).size().reset_index(name='count')
fig = px.sunburst(intent_flow, path=['flow_name', 'intencion'], values='count',
                title="Mapeo Flow → Intención")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== Gráfico 4: Churn y Resolución ====================
st.header("⚠️ Churn y Resolución")

# Datos a nivel sesión (último turno)
last_turn = df_filtered.loc[df_filtered.groupby('session_id')['turn_number'].idxmax()]
churn_by_flow = last_turn.groupby('flow_name')['es_churn_risk'].mean().reset_index()
resolved_by_flow = last_turn.groupby('flow_name')['resolved'].mean().reset_index()

fig = make_subplots(rows=1, cols=2, subplot_titles=("Tasa de Churn por Flow", "Tasa de Resolución por Flow"))

fig.add_trace(go.Bar(x=churn_by_flow['flow_name'], y=churn_by_flow['es_churn_risk'], 
                    name="Churn", marker_color='crimson'), row=1, col=1)
fig.add_trace(go.Bar(x=resolved_by_flow['flow_name'], y=resolved_by_flow['resolved'], 
                    name="Resolución", marker_color='forestgreen'), row=1, col=2)

fig.update_layout(showlegend=False, height=500)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== Gráfico 5: Distribución de Frustración ====================
st.header("😤 Distribución de Frustración")

frust_dist = df_filtered['nivel_frustracion'].value_counts().sort_index().reset_index()
frust_dist.columns = ['nivel_frustracion', 'count']
frust_dist['label'] = frust_dist['nivel_frustracion'].map({0: 'Baja', 1: 'Media', 2: 'Alta'})

fig = px.bar(frust_dist, x='label', y='count', 
            title="Distribución de Niveles de Frustración",
            color='label', color_discrete_map={'Baja': 'green', 'Media': 'orange', 'Alta': 'red'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== Pie de página ====================
st.caption("Dashboard desarrollado para ConversaAI - Hackathon Mayo 2026")