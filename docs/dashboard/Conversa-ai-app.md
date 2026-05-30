# ConversaAI APP - Documentación Técnica

> 📌 **Documentación del equipo Data Engineering** — Este documento describe el dashboard desarrollado por DE en `data_engineering/dashboard/`. El dashboard principal del proyecto DS se encuentra en `dashboard/` con estructura modular. Ver `README.md` para más detalles.

**Versión:** 1.0
**Fecha:** Mayo 2026
**Autor:** Data Engineering Team
**Proyecto:** S04-26-Equipo-42-Data-Science

---

## Tabla de Contenidos

- [ConversaAI APP - Documentación Técnica](#conversaai-app---documentación-técnica)
	- [Tabla de Contenidos](#tabla-de-contenidos)
	- [1. Descripción General](#1-descripción-general)
		- [Tecnologías utilizadas](#tecnologías-utilizadas)
		- [Repositorio](#repositorio)
	- [2. Acceso al Dashboard](#2-acceso-al-dashboard)
		- [Opción A: Acceso Online (recomendado)](#opción-a-acceso-online-recomendado)
		- [Opción B: Ejecución Local](#opción-b-ejecución-local)
- [Instalar dependencias](#instalar-dependencias)
- [Ejecutar dashboard](#ejecutar-dashboard)
		- [Opción C: Lanzador desde raíz](#opción-c-lanzador-desde-raíz)
	- [3. Estructura del Proyecto](#3-estructura-del-proyecto)
	- [4. Funcionalidades](#4-funcionalidades)
		- [4.1 KPIs Globales](#41-kpis-globales)
		- [4.2 Visualizaciones](#42-visualizaciones)
		- [4.3 Páginas del Dashboard](#43-páginas-del-dashboard)
	- [5. Filtros Disponibles](#5-filtros-disponibles)
	- [6. Datos Utilizados](#6-datos-utilizados)
		- [Dataset Principal](#dataset-principal)
		- [Diccionario de Variables](#diccionario-de-variables)
		- [Distribución de Targets](#distribución-de-targets)
	- [7. Instalación Local](#7-instalación-local)
		- [Requisitos previos](#requisitos-previos)
		- [Paso a paso](#paso-a-paso)
- [1. Clonar repositorio](#1-clonar-repositorio)
- [2. Crear entorno virtual](#2-crear-entorno-virtual)
- [3. Activar entorno virtual](#3-activar-entorno-virtual)
- [En Windows:](#en-windows)
- [En Mac/Linux:](#en-maclinux)
- [4. Instalar dependencias](#4-instalar-dependencias)
- [5. Ejecutar dashboard](#5-ejecutar-dashboard)
		- [Dependencias (requirements.txt)](#dependencias-requirementstxt)
	- [8. Mantenimiento](#8-mantenimiento)
		- [Actualizar datos](#actualizar-datos)
		- [Agregar nueva página](#agregar-nueva-página)
		- [Modificar gráficos existentes](#modificar-gráficos-existentes)
	- [9. Solución de Problemas](#9-solución-de-problemas)
	- [10. Próximas Mejoras](#10-próximas-mejoras)
	- [Contacto](#contacto)

---

## 1. Descripción General

El **Dashboard de ConversaAI** es una herramienta interactiva desarrollada para visualizar y analizar conversaciones de soporte al cliente en español y portugués. Permite al equipo de producto identificar patrones de frustración, intenciones no resueltas y métricas clave de rendimiento.

### Tecnologías utilizadas

| Tecnología | Propósito                   |
| ----------- | ---------------------------- |
| Python 3.12 | Lenguaje principal           |
| Streamlit   | Framework del dashboard      |
| Plotly      | Visualizaciones interactivas |
| Pandas      | Procesamiento de datos       |

### Repositorio

[https://github.com/No-Country-simulation/S04-26-Equipo-42-Data-Science](https://github.com/No-Country-simulation/S04-26-Equipo-42-Data-Science)

---

## 2. Acceso al Dashboard

### Opción A: Acceso Online (recomendado)

**URL:** [https://conversaai-dashboard.streamlit.app](https://conversaai-dashboard.streamlit.app)

*Requisitos:* Ninguno (acceso web directo)

### Opción B: Ejecución Local

```bash
# Clonar repositorio
git clone https://github.com/No-Country-simulation/S04-26-Equipo-42-Data-Science.git```

```

# Instalar dependencias

pip install -r requirements.txt

# Ejecutar dashboard

streamlit run data_engineering/dashboard/app.py

### Opción C: Lanzador desde raíz

```bash
python app.py
```
---

## 3. Estructura del Proyecto

S04-26-Equipo-42-Data-Science/
├── app.py                              # Lanzador principal
├── requirements.txt                    # Dependencias
└─── data_engineering/
   ├── dashboard/
   │   ├── app.py                      # Dashboard principal
   │   └── pages/                      # Páginas adicionales
   │       ├── 01_intents_unresolved.py
   │       ├── 02_frustration_spikes.py
   │       ├── 03_temporal_trends.py
   │       ├── 04_workflows.py
   │       └── 05_users.py
   └── data/
      └── processed/
          └── data_preprocessed.csv   # Dataset (20,001 registros)


---
## 4. Funcionalidades

### 4.1 KPIs Globales


| KPI                 | Descripción           | Cálculo                                 |
| ------------------- | ---------------------- | ---------------------------------------- |
| Sesiones            | Conversaciones únicas | `COUNT(DISTINCT session_id)`           |
| Tasa de Churn       | Usuarios que abandonan | `AVG(es_churn_risk) * 100`             |
| Tasa de Resolución | Problemas resueltos    | `AVG(resolved) * 100`                  |
| Frustración Alta   | Mensajes nivel 2       | `(COUNT(frustracion=2) / total) * 100` |
| Total Mensajes      | Volumen de mensajes    | `COUNT(*)`                             |



### 4.2 Visualizaciones

| Visualización | Datos                  | Propósito                     |
| -------------- | ---------------------- | ------------------------------ |
| Pie chart      | Distribución por flow | Identificar flujos más usados |
| Barras         | Frustración por flow  | Comparar niveles entre flujos  |
| Línea         | Frustración por turno | Detectar patrón creciente     |
| Sunburst       | Intención vs Flow     | Validar mapeo 1:1              |
| Barras dobles  | Churn/Resolución      | Comparar desempeño por flow   |
| Tendencias     | Evolución temporal    | Detectar picos estacionales    |



### 4.3 Páginas del Dashboard

| Página                  | Archivo                      | Función                           |
| ------------------------ | ---------------------------- | ---------------------------------- |
| Overview                 | `app.py`                   | KPIs y visualizaciones principales |
| Intenciones No Resueltas | `01_intents_unresolved.py` | Top intenciones sin resolver       |
| Picos de Frustración    | `02_frustration_spikes.py` | Detección de anomalías           |
| Tendencias Temporales    | `03_temporal_trends.py`    | Evolución por período            |
| Análisis por Workflow   | `04_workflows.py`          | Comparativa de flujos              |
| Análisis por Usuario    | `05_users.py`              | Métricas por agente               |

---

## 5. Filtros Disponibles

| Filtro                | Tipo        | Valores posibles                                                                | Default       |
| --------------------- | ----------- | ------------------------------------------------------------------------------- | ------------- |
| Flows                 | Multiselect | Acceso y Seguridad, Gestión de Cuenta, Soporte Técnico, Facturación y Cobros | Todos         |
| Rango de fechas       | Date picker | Nov 2025 - May 2026                                                             | Todo el rango |
| Nivel de frustración | Multiselect | 0 (Baja), 1 (Media), 2 (Alta)                                                   | Todos         |
| Granularidad temporal | Selectbox   | Diario, Semanal, Mensual                                                        | Diario        |


---
## 6. Datos Utilizados

### Dataset Principal

| Propiedad           | Valor                                    |
| ------------------- | ---------------------------------------- |
| **Archivo**   | `data/processed/data_preprocessed.csv` |
| **Registros** | 20,001 mensajes                          |
| **Sesiones**  | 6,648 conversaciones                     |
| **Período**  | Noviembre 2025 - Mayo 2026               |
| **Idiomas**   | Español (100%)                          |



### Diccionario de Variables

| Variable              | Tipo     | Rango             | Descripción                         |
| --------------------- | -------- | ----------------- | ------------------------------------ |
| `session_id`        | string   | -                 | Identificador único de sesión      |
| `turn_number`       | int      | 1-6               | Número de turno en la conversación |
| `flow_name`         | string   | 4 valores         | Nombre del flujo conversacional      |
| `usuario`           | string   | 540 valores       | Identificador del agente/usuario     |
| `fecha`             | datetime | 2025-11 a 2026-05 | Timestamp del mensaje                |
| `intencion`         | string   | 4 valores         | Intención del usuario               |
| `nivel_frustracion` | int      | 0,1,2             | Nivel de frustración                |
| `texto_clean`       | string   | -                 | Texto normalizado para NLP           |
| `es_churn_risk`     | int      | 0,1               | Riesgo de abandono                   |
| `resolved`          | int      | 0,1               | Problema resuelto o no               |



### Distribución de Targets

| Target       | Clase 0 | Clase 1 | Clase 2 |
| ------------ | ------- | ------- | ------- |
| Frustración | 54.8%   | 33.3%   | 11.8%   |
| Churn        | 88.2%   | 11.8%   | -       |
| Resolución  | 78.5%   | 21.5%   | -       |

---

## 7. Instalación Local

### Requisitos previos

* Python 3.12 o superior
* Git
* Conexión a internet


### Paso a paso


# 1. Clonar repositorio

git clone https://github.com/No-Country-simulation/S04-26-Equipo-42-Data-Science.git
cd S04-26-Equipo-42-Data-Science

# 2. Crear entorno virtual

python -m venv .env

# 3. Activar entorno virtual

# En Windows:

.env\Scripts\activate

# En Mac/Linux:

source .env/bin/activate

# 4. Instalar dependencias

pip install -r requirements.txt

# 5. Ejecutar dashboard

streamlit run data_engineering/dashboard/app.py



### Dependencias (requirements.txt)

* streamlit>=1.35.0
* pandas>=2.2.0
* plotly>=5.24.0
* joblib>=1.4.0
* pyarrow>=15.0.0

---

## 8. Mantenimiento

### Actualizar datos

1. Reemplazar `data/processed/data_preprocessed.csv`
2. Reiniciar el servidor de Streamlit (Ctrl+C y `streamlit run app.py`)


### Agregar nueva página
Crear archivo: pages/06_nueva_pagina.py
Contenido mínimo:
   import streamlit as st
   st.title("Mi Nueva Página")

### Modificar gráficos existentes
Editar directamente en:
- data_engineering/dashboard/app.py (página principal)
- data_engineering/dashboard/pages/*.py (páginas secundarias)


---

## 9. Solución de Problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| ModuleNotFoundError | Dependencia faltante | pip install -r requirements.txt |
| El dashboard no carga | Archivo de datos no encontrado | Verificar data/processed/data_preprocessed.csv |
| Las páginas no aparecen | Carpeta pages/ incorrecta | Usar nombres numéricos: 01_*.py |
| Error de rutas | Path relativo incorrecto | Verificar estructura del proyecto |
| Dashboard lento | Demasiados datos | Filtrar por fecha o flows |
| Gráficos vacíos | Filtros muy restrictivos | Ampliar rango de selección |

---

## 10. Próximas Mejoras

| Mejora | Prioridad | Estado |
|--------|-----------|--------|
| Exportar reportes en PDF | Alta | Pendiente |
| Alertas automáticas de picos | Media | Pendiente |
| Integración con datos en tiempo real | Media | Pendiente |
| Modelos predictivos de escalamiento | Baja | Pendiente |
| Autenticación de usuarios | Baja | Pendiente |

---
## Contacto

| Rol | Nombre | GitHub |
|-----|--------|--------|
| Data Engineer | marelycarcamo | github.com/marelycarcamo |
| Data Science | luiscm17 | github.com/luiscm17 |

