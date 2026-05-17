# Data Engineering Pipeline - Conversa AI

## 📌 Descripción

**Rol:** Data Engineer**Entregables:**

- Notebooks ETL (`ingest.ipynb`, `preprocess.ipynb`)
- Dataset procesado (`data_processed.parquet`)
- Reporte de calidad (quality_report_xxxxx)

## 🗂️ Estructura del repositorio

```


data_engineering/
│
├── data/
│   ├── raw/
│   │   └── ejemplo_v2_final.csv          # (o corpus_v2_final.csv, según tu archivo real)
│   ├── interim/
│   │   └── data_limpia.parquet
│   └── processed/
│       └── data_processed.parquet
├── notebooks/
│   ├── ingest.ipynb
│   └── preprocess.ipynb
├── reports/
│   └── quality/
│       └── quality_report_20260512.html   # (o .md)
├── .gitignore
└── README.md

```

## 📊 Datos de origen

El proyecto se ha desarrollado utilizando **datos sintéticos** generados para simular conversaciones de soporte. La decisión de emplear datos sintéticos responde a:

* **Disponibilidad inmediata:** Permite construir y validar el pipeline sin esperar la liberación de datos reales (sujetos a privacidad o aprobaciones).
* **Estructura controlada:** Los datos sintéticos incluyen las mismas columnas y tipos que los reales (`session_id`, `turn_number`, `flow_name`, `intencion`, `nivel_frustracion`, textos en español/portugués, etc.).
* **Reproducibilidad:** Cualquier miembro del equipo puede ejecutar el pipeline con los datos de ejemplo y obtener los mismos resultados.

### 🧪 Dataset sintético de ejemplo

* **Archivo:** `ejemplo_v2_final.csv` (incluido en `data/raw/`)
* **Tamaño:** 20.001 filas (6 sesiones completas de 3 turnos cada una)
* **Columnas principales:**
  * `session_id`, `turn_number`, `flow_name`
  * `texto_espanol`, `texto_portugues`
  * `intencion`, `nivel_frustracion` (0-2)
  * `es_churn_risk`, `resolved`
* **Limitaciones conocidas:**
  * Solo 3 turnos por sesión (en datos reales puede haber más).
  * No contiene columna de escalamiento explícita (se definirá con el equipo de producto).
  * El texto es corto y sin ruido extremo (emojis, errores tipográficos graves).

### 📈 Proyección a datos reales

El pipeline se ha diseñado para ser **independiente del volumen** y funcionará con los datos reales (2.000 o hasta 2 millones de mensajes) con mínimos ajustes:

* La detección automática de encoding y separador soporta CSVs reales.
* Las validaciones de calidad (nulos, rangos) alertarán sobre datos atípicos.
* La limpieza de texto (minúsculas, acentos, puntuación) es robusta frente a emojis, mayúsculas y errores comunes.

> **Nota:** Si los datos reales incluyeran nuevas columnas (ej. `agente_intervino`, `tiempo_respuesta`), los notebooks pueden actualizarse fácilmente para aprovecharlas.

---

## Descripción Notebooks

### Notebook ingest.ipynb

Este notebook:

* Detecta automáticamente encoding y separador del CSV.
* Valida que las columnas obligatorias existan y que nivel_frustracion esté en [0,2].
* Convierte la columna fecha a datetime.
* Guarda un DataFrame limpio intermedio (por defecto como Parquet, si no funciona usa CSV).

Al ejecutarlo se generarán:

* data_limpia.parquet (o .csv) – datos con tipos correctos y sin errores básicos.
* quality_report.html – resumen de calidad (nulos, duplicados, etc.).

### 📒Notebook preprocess.ipynb

Este notebook:

* Toma el archivo generado por ingest.ipynb.
* Detecta el idioma de cada mensaje (es/pt) según qué columna de texto no esté vacía.
* Normaliza el texto: minúsculas, eliminación de acentos y puntuación, espacios redundantes.
* Crea una columna texto_clean lista para NLP.
* Guarda el dataset final como data_processed.parquet (y opcionalmente CSV).

---

## 📊 Formato del dataset final (`data_processed.parquet`)

| Columna                       | Tipo     | Descripción                                                  |
| ----------------------------- | -------- | ------------------------------------------------------------- |
| `session_id`                | string   | Identificador único de la conversación                      |
| `turn_number`               | int      | Número de turno dentro de la sesión (1..N)                  |
| `flow_name`                 | string   | Nombre del flujo conversacional (ej. "Acceso y Seguridad")    |
| `fecha`                     | datetime | Fecha y hora del mensaje                                      |
| `intencion`                 | string   | Intención del usuario (target para modelos)                  |
| `nivel_frustracion`         | int      | 0 = baja, 1 = media, 2 = alta (target secundario)             |
| `resolved`                  | int      | 1 = problema resuelto, 0 = no resuelto                        |
| `es_churn_risk`             | int      | 1 = riesgo de abandono, 0 = normal                            |
| `idioma`                    | string   | `es` (español) o `pt` (portugués)                       |
| `texto_clean`               | string   | Texto normalizado (sin acentos, sin puntuación, minúsculas) |
| `texto_original` (opcional) | string   | Texto original del idioma detectado                           |

> **Nota:** Si el equipo lo requiere, se pueden añadir columnas derivadas como `longitud_texto`, `turno_maximo_por_sesion`, etc. con una pequeña modificación en `preprocess.ipynb`.

## ⚠️ Suposiciones y limitaciones

- **Escalamiento:** Los datos originales no tienen una columna explícita de "escalamiento". Se puede derivar como `(turn_number >= 4) & (resolved == 0)` si el equipo lo acuerda.
- **Abandono:** Se asume que `es_churn_risk == 1` indica que el usuario abandonó la conversación.
- **Idioma:** Si ambos textos (español y portugués) están presentes, se prioriza el español por defecto. En datos reales solo debería venir uno.
- **Turno máximo:** En los datos sintéticos cada sesión tenía exactamente 3 turnos; en los reales puede haber más. El pipeline acepta cualquier entero positivo.

## 📈 Reporte de calidad

El notebook `ingest.ipynb` produce un archivo `quality_report.html` que incluye:

- Número de filas iniciales y finales
- Nulos por columna
- Duplicados por fila completa y por clave (`session_id` + `turn_number`)
- Distribución de `nivel_frustracion`
- Valores fuera de rango (corregidos automáticamente)

## 🤝 Integración con otros equipos

- **Data Science:** El archivo `data_processed.parquet` es el punto de partida para entrenar modelos de sentimiento e intención. Si necesitan más features (longitud, etc.), abrid un issue en el repositorio.
- **Frontend/Backend:** Si requieren agregados (p.ej., top intenciones no resueltas, frustración media por flow), se puede crear un notebook adicional que lea el Parquet y genere endpoints simulados o CSVs de métricas.

## 📝 Notas para el equipo de Data Science171

- El texto ya viene limpio y en minúsculas sin acentos. Pueden usarlo directamente en vectores (TF‑IDF, embeddings).
- La columna `intencion` es el target para clasificación de intenciones.
- `nivel_frustracion` puede usarse como target para regresión/clasificación de frustración o como feature.
- `resolved` puede predecirse como indicador de resolución.

## 🧹 Mantenimiento y mejoras futuras

- Si el volumen crece (>10k filas), se recomienda migrar a Parquet siempre y usar `pyarrow`.
- Si se incorporan nuevas columnas (por ejemplo `agente_intervino`, `tiempo_respuesta`), actualizar los notebooks fácilmente.
- Para automatización, los notebooks pueden convertirse a scripts `.py` y programarse con `cron` o Airflow.

## ✒️ Autor

Data Engineer – Hackathon Conversa AI
[Marely Cárcamo Quisto] – [17/05/2026]

---

**Última actualización:** Mayo 2026

```

```
