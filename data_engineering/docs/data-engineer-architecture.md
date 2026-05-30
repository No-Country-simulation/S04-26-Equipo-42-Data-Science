```
data-engineer/

├── etl/

│ ├── ingest.py \# Lee CSV, valida, carga a DB

│ ├── preprocess.py \# Limpieza de texto (básica: minúsculas, quitar
acentos)

│ └── validate.py \# Reglas de negocio

├── inference/

│ ├── batch_predict.py \# Llama a endpoints ML y guarda resultados

│ └── client.py \# Cliente HTTP para los modelos

├── db/

│ ├── schema.sql \# DDL de tablas

│ ├── migrations/ \# Scripts de cambios (si usas alembic)

│ └── queries/ \# Vistas para KPIs

├── scripts/

│ ├── run_all.sh \# Orquesta ETL + inferencia + agregados

│ └── clean_old_data.py \# Limpieza

├── tests/

│ ├── test_etl.py \# Pruebas con el CSV sintético

│ └── test_queries.py

└── README.md \# Instrucciones para correr el pipeline
```

# Proyecto Data Engineer - Conversa AI

## Pipeline ETL + Integración con Modelos + KPIs Básicos

### 1. Setup y configuraciones

- Importar librerías (pandas, sqlalchemy, requests, etc.)

- Parámetros globales (ruta del CSV, connection string, endpoints)

### 2. Ingesta y validación inicial

- Cargar CSV (el sintético o el real)

- Validar columnas obligatorias

- Mostrar reporte de calidad (filas nulas, tipos, valores fuera de
  rango)

### 3. Limpieza y transformación

- Uniformar fechas (columna fecha a datetime)

- Asignar idioma (es o pt) según texto no nulo

- Normalizar texto básico (minúsculas, eliminar puntuación excesiva)

- Crear columna texto_clean para los modelos

### 4. Carga a base de datos (SQLite o Supabase)

- Crear tablas messages, sessions (si no existen)

- Insertar datos (usando if_exists=\'append\')

### 5. Inferencia batch (simulada o real)

- Por cada mensaje, llamar a endpoint de sentimiento e intención (si el
  modelo no está listo, usar valores dummy)

- Guardar resultados en tabla predictions

### 6. Agregados para dashboard

- Calcular KPIs:

  - Tasa de frustración promedio por flow_name

  - Top 3 intenciones no resueltas (resolved=0)

  - Distribución de sentimientos por idioma

- Generar vistas/materialized views o guardar resultados en CSV

### 7. Exportación de reporte final

- Crear archivo reporte_intenciones_no_resueltas.csv

- Mostrar gráfico simple con matplotlib o plotly

### 8. Conclusión y pasos siguientes

- Resumen de registros procesados, errores detectados, etc.

- Notas para el equipo de Frontend (cuáles tablas consultar)
