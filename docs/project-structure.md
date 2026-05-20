# Project Structure — ConversaAI

Estructura detallada del proyecto de analisis de sentimiento e intencion,
organizado bajo metodologia CRISP-DM.

```
.
├── README.md                          # Presentacion del proyecto
├── AGENTS.md                          # Convenciones para sesiones con AI
│
├── pyproject.toml                     # Configuracion del proyecto (uv + Hatchling)
├── .python-version                    # Version de Python pinneada (3.12)
├── uv.lock                            # Lock file de dependencias
├── skills-lock.json                   # Lock file de skills instaladas
│
├── .gitignore
├── .hintrc
│
├── data/
│   └── processed/
│       └── data_preprocessed.csv      # Symlink al dataset (NO mover)
│
├── data_engineering/                  # Sub-proyecto de Data Engineering
│   ├── notebooks/                     #   Notebooks de ingesta y preprocesamiento
│   ├── data/processed/                #   Dataset fuente (no modificar)
│   └── reports/quality/               #   Reportes de calidad de datos
│
├── docs/                              # Documentacion del proyecto
│   ├── conversa-ai.md                 #   Guideline del proyecto
│   ├── data-dictionary.md             #   Diccionario de datos (15 columnas)
│   ├── ml-charter.md                  #   Charter del proyecto ML (CRISP-DM)
│   ├── project-structure.md           #   Este archivo
│   ├── sprint-plan.md                 #   Plan de trabajo por sprints
│   ├── tech-stack-roadmap.md          #   Roadmap tecnologico V1-V3
│   └── Planificacion de Actividades.md#   Propuesta original (referencia)
│
├── models/                            # Pipelines exportados
│   ├── frustration_model.pkl          #   Modelo de frustracion (joblib)
│   └── frustration_metadata.json      #   Metadatos del modelo
│
├── notebooks/                         # Notebooks numerados por orden CRISP-DM
│   ├── 01-eda.ipynb                   #   Analisis exploratorio de datos
│   ├── 02-sentiment-model.ipynb       #   Clasificacion de frustracion
│   ├── 03-intent-model.ipynb          #   Deteccion de intencion (pendiente)
│   ├── 04-churn-model.ipynb           #   Prediccion de churn (pendiente)
│   └── 05-pattern-analysis.ipynb      #   Analisis cruzado de patrones (pendiente)
│
├── reports/                           # Reportes con hallazgos
│   ├── eda-report.md                  #   Hallazgos del EDA
│   ├── sentiment-model-report.md      #   Evaluacion del modelo de frustracion
│   └── figures/                       #   Graficos y visualizaciones (PNG)
│       ├── baseline_deterministico.png
│       ├── correlation_matrix.png
│       ├── frustracion_distribution.png
│       ├── rf_feature_importance.png
│       └── ... (22 figuras en total)
│
├── src/
│   └── sentiment_analysis/            # Modulos reutilizables
│       └── __init__.py                #   (paquete, contenido proximamente)
│
└── .agents/                           # Skills instaladas (no modificar manualmente)
    ├── exploratory-data-analysis/
    ├── ml-pipeline-workflow/
    ├── nlp-natural-language-processing/
    ├── scikit-learn-best-practices/
    └── sentiment-analysis/
```

## Convenciones

### Metodologia

El proyecto sigue **CRISP-DM** (Cross-Industry Standard Process for Data Mining):

| Fase | Estado |
|------|--------|
| Business Understanding | Completado |
| Data Understanding | Completado |
| Data Preparation | Completado (Data Engineering) |
| Modeling | Parcial (frustracion listo, intent/churn pendientes) |
| Evaluation | Pendiente |
| Deployment | Pendiente (dashboard + reporte final) |

### Ramas

- `main` — version estable, protegida
- `ml/sentiment` — desarrollo activo del pipeline ML
- Commits en ingles, formato conventional commits

### Dependencias

Gestionadas exclusivamente con `uv`:

```bash
uv sync                           # instalar todo
uv add <paquete>                  # agregar dependencia
uv run python <script>            # ejecutar con el venv del proyecto
uv run jupyter lab                # lanzar notebooks
```

### Dataset

- Origen: `data_engineering/data/processed/data_preprocessed.csv`
- Acceso via symlink: `data/processed/data_preprocessed.csv`
- 20,001 filas, 15 columnas, cero nulos
- Naturaleza: sintetico/determinista (ver `reports/eda-report.md`)
- Los modelos supervisados son un ejercicio metodologico; el valor del proyecto
  esta en el pipeline, las visualizaciones y la arquitectura.

### Targets

| Target | Tipo | Clases |
|--------|------|--------|
| `nivel_frustracion` | Ordinal | 0 (55%), 1 (33%), 2 (12%) |
| `intencion` | Multiclase | 4 clases (~25% c/u) |
| `es_churn_risk` | Binario | 0 (88%), 1 (12%) |
| `resolved` | Binario | 0 (78%), 1 (22%) |

### Skills instaladas

El proyecto utiliza skills de AI para asistencia en tareas especificas.
Ver `.atl/skill-registry.md` para el listado completo.
