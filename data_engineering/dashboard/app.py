"""
ConversaAI - Dashboard de Análisis de Conversaciones de Soporte
Autor: Data Engineering Team
Fecha: Mayo 2026

Dashboard interactivo para visualizar:
- KPIs globales de conversaciones
- Distribución por flujo (flow)
- Patrones de frustración
- Intenciones no resueltas
- Tendencias temporales
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(
    page_title="ConversaAI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CARGA DE DATOS ====================
@st.cache_data
def load_data():
    """Carga el dataset preprocesado desde data/processed/"""
    # Construir ruta relativa desde dashboard/
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "data" / "processed" / "data_preprocessed.csv"
    print(f"Cargando datos desde: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Convertir fecha a datetime si no lo está
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
    
    return df

# Cargar datos
try:
    df = load_data()
    st.success(f"✅ Datos cargados: {len(df):,} mensajes, {df['session_id'].nunique():,} sesiones")
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
    st.info("Verifica que el archivo exista en: data/processed/data_preprocessed.csv")
    st.stop()

# ==================== FILTROS EN SIDEBAR ====================
st.sidebar.header("🔍 Filtros")

# Filtro por flows
flows = st.sidebar.multiselect(
    "Flows",
    options=df['flow_name'].unique(),
    default=df['flow_name'].unique(),
    help="Selecciona uno o más flujos conversacionales"
)

# Filtro por rango de fechas
if 'fecha' in df.columns:
    min_date = df['fecha'].min().date()
    max_date = df['fecha'].max().date()
    
    date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = []

# Filtro por nivel de frustración
frustration_levels = st.sidebar.multiselect(
    "Nivel de frustración",
    options=[0, 1, 2],
    default=[0, 1, 2],
    format_func=lambda x: {0: "Baja", 1: "Media", 2: "Alta"}[x],
    help="0 = Baja, 1 = Media, 2 = Alta"
)

# Aplicar filtros
df_filtered = df[df['flow_name'].isin(flows)]
df_filtered = df_filtered[df_filtered['nivel_frustracion'].isin(frustration_levels)]

if len(date_range) == 2 and 'fecha' in df.columns:
    mask = (df_filtered['fecha'] >= pd.to_datetime(date_range[0])) & \
        (df_filtered['fecha'] <= pd.to_datetime(date_range[1]) + pd.Timedelta(days=1))
    df_filtered = df_filtered[mask]

# Métricas después de filtros
total_mensajes_filtrados = len(df_filtered)
total_sesiones_filtradas = df_filtered['session_id'].nunique() if not df_filtered.empty else 0

# ==================== SIDEBAR - CONFIGURACIONES ====================
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configuración")

granularidad = st.sidebar.selectbox(
    "Granularidad temporal",
    ["Diario", "Semanal", "Mensual"],
    help="Nivel de detalle para los gráficos de tendencia"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "📊 **Dashboard ConversaAI**\n\n"
    "Desarrollado para NoCountry.\n\n"
    "Basado en datos sintéticos. Pipeline listo para datos reales."
)

# ==================== TÍTULO PRINCIPAL ====================
st.title("📊 ConversaAI - Análisis de Conversaciones de Soporte")
st.markdown("Dashboard interactivo para visualizar métricas de frustración, intenciones no resueltas y tendencias temporales.")
st.markdown("---")

# ==================== KPIS GLOBALES ====================
st.header("📈 KPIs Globales")

if not df_filtered.empty:
    # Calcular KPIs a nivel sesión (último turno)
    last_turn = df_filtered.loc[df_filtered.groupby('session_id')['turn_number'].idxmax()]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Sesiones", f"{total_sesiones_filtradas:,}")
    
    with col2:
        tasa_churn = (last_turn['es_churn_risk'].mean() * 100) if not last_turn.empty else 0
        st.metric("Tasa de Churn", f"{tasa_churn:.1f}%")
    
    with col3:
        tasa_resolucion = (last_turn['resolved'].mean() * 100) if not last_turn.empty else 0
        st.metric("Tasa de Resolución", f"{tasa_resolucion:.1f}%")
    
    with col4:
        frustracion_alta = (df_filtered['nivel_frustracion'] == 2).mean() * 100
        st.metric("Frustración Alta", f"{frustracion_alta:.1f}%")
    
    with col5:
        st.metric("Total Mensajes", f"{total_mensajes_filtrados:,}")
else:
    st.warning("⚠️ No hay datos con los filtros seleccionados")
    st.stop()

st.markdown("---")

# ==================== DISTRIBUCIÓN POR FLOW ====================
st.header("📊 Distribución por Flow")

if not df_filtered.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        flow_counts = df_filtered['flow_name'].value_counts().reset_index()
        flow_counts.columns = ['flow_name', 'count']
        fig = px.pie(flow_counts, values='count', names='flow_name', 
                    title="Mensajes por Flow", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        frust_by_flow = df_filtered.groupby('flow_name')['nivel_frustracion'].mean().sort_values().reset_index()
        fig = px.bar(frust_by_flow, x='flow_name', y='nivel_frustracion', 
                    title="Frustración Promedio por Flow", 
                    color='nivel_frustracion', color_continuous_scale='Reds',
                    labels={'nivel_frustracion': 'Frustración promedio'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== FRUSTRACIÓN POR TURNO ====================
st.header("📉 Patrón de Frustración por Turno")

if not df_filtered.empty:
    frust_by_turn = df_filtered.groupby('turn_number')['nivel_frustracion'].agg(['mean', 'count']).reset_index()
    fig = px.line(frust_by_turn, x='turn_number', y='mean', 
                markers=True, title="Frustración Promedio por Turno",
                labels={'mean': 'Frustración promedio', 'turn_number': 'Número de turno'})
    fig.add_hline(y=1, line_dash="dash", line_color="orange", 
                annotation_text="Umbral medio", annotation_position="top right")
    fig.update_layout(yaxis_range=[0, 2])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== INTENCIONES NO RESUELTAS ====================
st.header("🎯 Intenciones No Resueltas")

if not df_filtered.empty:
    unresolved = df_filtered[df_filtered['resolved'] == 0]
    
    if len(unresolved) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            intent_counts = unresolved['intencion'].value_counts().reset_index()
            intent_counts.columns = ['intencion', 'count']
            fig = px.bar(intent_counts, x='intencion', y='count', 
                        title="Top Intenciones No Resueltas",
                        color='count', color_continuous_scale='Reds',
                        labels={'intencion': 'Intención', 'count': 'Cantidad'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            intent_flow = unresolved.groupby(['flow_name', 'intencion']).size().reset_index(name='count')
            fig = px.bar(intent_flow, x='flow_name', y='count', color='intencion',
                        title="No Resueltas por Flow", barmode='group',
                        labels={'flow_name': 'Flow', 'count': 'Cantidad', 'intencion': 'Intención'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Métrica adicional
        st.metric("Total de mensajes no resueltos", f"{len(unresolved):,}", 
                delta=f"{len(unresolved)/len(df_filtered)*100:.1f}% del total",
                delta_color="inverse")
    else:
        st.info("✅ No hay mensajes no resueltos en el período seleccionado")

st.markdown("---")

# ==================== RELACIÓN INTENCIÓN vs FLOW ====================
st.header("🔗 Relación Intención vs Flow")

if not df_filtered.empty:
    intent_flow_all = df_filtered.groupby(['flow_name', 'intencion']).size().reset_index(name='count')
    fig = px.sunburst(intent_flow_all, path=['flow_name', 'intencion'], values='count',
                    title="Mapeo Flow → Intención",
                    color='count', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Cada flow tiene una intención predominante (relación 1:1 en datos sintéticos)")

st.markdown("---")

# ==================== CHURN Y RESOLUCIÓN POR FLOW ====================
st.header("⚠️ Churn y Resolución por Flow")

if not df_filtered.empty:
    last_turn_filtered = df_filtered.loc[df_filtered.groupby('session_id')['turn_number'].idxmax()]
    churn_by_flow = last_turn_filtered.groupby('flow_name')['es_churn_risk'].mean().reset_index()
    resolved_by_flow = last_turn_filtered.groupby('flow_name')['resolved'].mean().reset_index()
    
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=("Tasa de Churn por Flow", "Tasa de Resolución por Flow"))
    
    fig.add_trace(go.Bar(x=churn_by_flow['flow_name'], y=churn_by_flow['es_churn_risk'], 
                        name="Churn", marker_color='crimson'), row=1, col=1)
    fig.add_trace(go.Bar(x=resolved_by_flow['flow_name'], y=resolved_by_flow['resolved'], 
                        name="Resolución", marker_color='forestgreen'), row=1, col=2)
    
    fig.update_layout(showlegend=False, height=500,
                    yaxis_title="Tasa", yaxis2_title="Tasa")
    fig.update_yaxes(range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== TENDENCIAS TEMPORALES ====================
st.header("📅 Tendencias Temporales")

if not df_filtered.empty and 'fecha' in df_filtered.columns:
    df_temp = df_filtered.copy()
    
    # Aplicar granularidad
    if granularidad == "Diario":
        df_temp['periodo'] = df_temp['fecha'].dt.date
    elif granularidad == "Semanal":
        df_temp['periodo'] = df_temp['fecha'].dt.to_period('W').astype(str)
    else:
        df_temp['periodo'] = df_temp['fecha'].dt.to_period('M').astype(str)
    
    # Agregar por período
    trends = df_temp.groupby('periodo').agg(
        frustracion_promedio=('nivel_frustracion', 'mean'),
        frustracion_alta=('nivel_frustracion', lambda x: (x == 2).mean()),
        churn_rate=('es_churn_risk', 'mean'),
        resolucion_rate=('resolved', 'mean'),
        total=('session_id', 'count')
    ).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(trends, x='periodo', y='frustracion_promedio',
                    title=f"Evolución de Frustración ({granularidad})",
                    markers=True, 
                    labels={'periodo': 'Período', 'frustracion_promedio': 'Frustración promedio'})
        fig.update_layout(yaxis_range=[0, 2])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico combinado de churn y resolución
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trends['periodo'], y=trends['churn_rate'],
                                mode='lines+markers', name='Churn',
                                line=dict(color='crimson')))
        fig.add_trace(go.Scatter(x=trends['periodo'], y=trends['resolucion_rate'],
                                mode='lines+markers', name='Resolución',
                                line=dict(color='forestgreen')))
        fig.update_layout(title=f"Churn vs Resolución ({granularidad})",
                        xaxis_title="Período", yaxis_title="Tasa",
                        yaxis_range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
    
    # Volumen de mensajes
    fig = px.bar(trends, x='periodo', y='total',
                title=f"Volumen de Mensajes ({granularidad})",
                color='total', color_continuous_scale='Blues',
                labels={'periodo': 'Período', 'total': 'Cantidad de mensajes'})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==================== DISTRIBUCIÓN DE FRUSTRACIÓN ====================
st.header("😤 Distribución de Frustración")

if not df_filtered.empty:
    frust_dist = df_filtered['nivel_frustracion'].value_counts().sort_index().reset_index()
    frust_dist.columns = ['nivel_frustracion', 'count']
    frust_dist['label'] = frust_dist['nivel_frustracion'].map({0: 'Baja', 1: 'Media', 2: 'Alta'})
    frust_dist['porcentaje'] = (frust_dist['count'] / frust_dist['count'].sum() * 100).round(1)
    
    fig = px.bar(frust_dist, x='label', y='count', 
                title="Distribución de Niveles de Frustración",
                color='label', 
                color_discrete_map={'Baja': 'green', 'Media': 'orange', 'Alta': 'red'},
                text='porcentaje',
                labels={'label': 'Nivel de frustración', 'count': 'Cantidad'})
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
# ==================== BOTÓN DE DESCARGA DE VIDEO DEMO ====================
st.markdown("---")
st.subheader("📹 Demo del Dashboard")

# Ruta al video (ajústala según dónde guardes el archivo)
video_path = "videos/dashboard_demo.mp4"

# Verificar si el video existe
import os
if os.path.exists(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    
    st.download_button(
        label="📥 Descargar video demo (MP4)",
        data=video_bytes,
        file_name="conversaai_dashboard_demo.mp4",
        mime="video/mp4"
    )
    st.caption("Video de demostración del dashboard - Mayo 2026")
else:
    st.info("📹 El video demo estará disponible próximamente.")

# ==================== PIE DE PÁGINA ====================
st.markdown("---")
st.caption(
    "📊 **ConversaAI Dashboard** | Desarrollado como simulación NoCountry | "
    "Datos sintéticos - Pipeline listo para datos reales | "
    f"Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
)