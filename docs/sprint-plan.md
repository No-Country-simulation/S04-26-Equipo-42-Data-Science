# Sprint Plan — ConversaAI

Basado en el roadmap CRISP-DM definido en `docs/ml-charter.md`.
Actualizado tras EDA (Mayo 2026) con hallazgos sobre la naturaleza determinista del dataset.

---

## Nota sobre el dataset

El analisis exploratorio (notebook 01-eda) revelo que el dataset presenta patrones deterministicos:

- `nivel_frustracion` sigue una regla exacta por `turn_number`: turno 1 = 0, turno 2 = 1, turno 3 = 0 o 2 segun `resolved`
- `es_churn_risk` tiene correlacion del 100% con `nivel_frustracion == 2`
- `intencion` mapea 1:1 con `flow_name`
- La longitud del texto es uniforme (15-33 caracteres), sugerente de datos sinteticos

Esto es consistente con la documentacion existente (`docs/data-dictionary.md`) que indica que el dataset es sintetico.

**Implicacion:** Las metricas de clasificacion supervisada seran artificialmente altas. El valor del proyecto reside en el pipeline de procesamiento, las visualizaciones y la arquitectura, que son 100% transferibles a datos reales. Los modelos supervisados se incluyen como ejercicio metodologico y para demostrar el flujo completo de CRISP-DM.

---

## Sprint 1: Data Exploration and Baselines

:white_check_mark: COMPLETADO

### Objectives
- Understand the dataset structure, distributions, and label quality
- Build heuristic baselines for all three modeling tasks

### Tasks completed
- Full EDA: distributions, correlations, session patterns, text statistics
- Validate label coherence (nivel_frustracion, intencion, es_churn_risk, resolved)
- Identify deterministic rules underlying each target
- Document findings in `reports/eda-report.md`

### Notebook
- `notebooks/01-eda.ipynb` :white_check_mark:
- `reports/eda-report.md` :white_check_mark:

---

## Sprint 2: Supervised Models (Methodological Exercise)

:white_check_mark: COMPLETADO

### Objectives
- Train supervised models for all three tasks following standard ML workflows ✅
- Compare against deterministic baselines discovered in EDA ✅
- Document the full modeling pipeline for reuse with real data ✅

### Tasks completed

#### Frustration model
- Feature engineering from `texto_clean` (TF-IDF unigrams + bigrams) :white_check_mark:
- Feature engineering from context (turn_number, flow_name, agente) :white_check_mark:
- Train and evaluate RandomForest classifier :white_check_mark:
- Compare against deterministic baseline :white_check_mark:
- Error analysis: 0 misclassified cases (100% accuracy) :white_check_mark:
- Export model pipeline: `models/frustration_model.pkl` (588 KB) + metadata :white_check_mark:
- **Result:** F1-weighted **1.0000** (vs baseline 0.55 objective)

#### Intent model
- Train RandomForest with TF-IDF features (texto_clean) :white_check_mark:
- Compare against flow_name lookup baseline (100% accurate) :white_check_mark:
- Document that intent is fully determined by flow_name :white_check_mark:
- Export model pipeline: `models/intent_model.pkl` (456 KB) + metadata :white_check_mark:
- **Result:** F1-macro **1.0000** (vs baseline 0.25 objective)

#### Churn model
- Train RandomForest with TF-IDF features (texto_clean — text-only) :white_check_mark:
- Compare against frustracion==2 rule (100% accurate, same 2,364 records) :white_check_mark:
- Document that churn = frustracion alta sin resolucion :white_check_mark:
- Export model pipeline: `models/churn_model.pkl` (301 KB) + metadata :white_check_mark:
- **Result:** AUC-PR **1.0000** (vs baseline 0.30 objective)

### Deliverables completed
- `notebooks/02-sentiment-model.ipynb` :white_check_mark:
- `notebooks/03-intent-model.ipynb` :white_check_mark:
- `notebooks/04-churn-model.ipynb` :white_check_mark:
- `reports/sentiment-model-report.md` with figures :white_check_mark:
- `reports/intent-model-report.md` with figures :white_check_mark:
- `reports/churn-model-report.md` with figures :white_check_mark:
- Model artifacts in `models/` directory :white_check_mark:

---

## Sprint 3: Pattern Analysis and Dashboard

### Objectives
- Aggregate outputs across all targets into actionable insights
- Build an interactive dashboard for the product team
- Generate the real value of the project: visualizations and patterns

### Tasks

#### Cross-analysis
- Frustration distribution by flow, intent, agent, time period
- Resolution rates by intent and frustration level
- Churn patterns: which combinations of intent + frustration lead to abandonment
- Temporal trends: how frustration evolves over the 6-month window
- Session-level analysis: complete conversation outcomes

#### Dashboard (Streamlit)
- Main KPIs: volume, resolution rate, churn rate, avg frustration
- Filters: flow, intent, date range, agent
- Interactive charts (plotly):
  - Frustration distribution by flow and intent
  - Resolution rates with drill-down
  - Churn risk heatmap
  - Temporal evolution of all metrics
  - Top unresolved intents per flow
- Data export: allow downloading filtered views as CSV

#### Documentation
- Document each insight with concrete examples
- Note which findings are dataset-specific and which would generalize to real data
- Provide recommendations for what to monitor with real data

### Deliverables
- `notebooks/05-pattern-analysis.ipynb`
- `dashboard/app.py` (Streamlit application)
- `reports/insights-summary.md` with actionable recommendations

---

## Sprint 4: Final Report and Presentation

### Objectives
- Consolidate all findings into an executive report
- Prepare presentation materials
- Document limitations and roadmap for real data deployment

### Tasks
- Write executive summary of findings
- Document architecture and pipeline design decisions
- Include honest assessment of synthetic data limitations
- Outline migration path to real data (what changes, what stays)
- Prepare presentation slides or notebook-based demo

### Deliverables
- `docs/final-report.md`
- `reports/presentation.md` or slide deck
- Demo-ready Streamlit dashboard

---

## Resumen de cambios respecto a la version anterior

| Aspecto | Version anterior | Version ajustada |
|---------|-----------------|-----------------|
| Enfoque de modelado | Entrenar modelos supervisados como objetivo principal | Modelos como ejercicio metodologico; el valor esta en el pipeline y dashboard |
| Sprint 2 | Solo frustracion | Los 3 modelos en un sprint (son rapidos por ser deterministicos) |
| Sprint 3 | Intent + Churn | Ahora es Pattern Analysis + Dashboard (expandido) |
| Sprint 4 | Pattern Analysis + Dashboard | Ahora es Final Report + Presentacion |
| Dataset | Tratado como datos reales | Explicitamente documentado como sintetico con implicaciones claras |
| Metricas | F1, AUC-PR como objetivo | Comparacion contra baseline deterministico como referencia |
