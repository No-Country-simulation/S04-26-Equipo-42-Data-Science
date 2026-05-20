# Sprint Plan — ConversaAI

Basado en el roadmap CRISP-DM definido en `docs/ml-charter.md`.

---

## Sprint 1: Data Exploration and Baselines

### Objectives
- Understand the dataset structure, distributions, and label quality
- Build heuristic baselines for all three modeling tasks

### Tasks
- Full EDA: distributions, correlations, session patterns, text statistics
- Validate label coherence (nivel_frustracion, intencion, es_churn_risk, resolved)
- Implement keyword-based frustration baseline
- Implement rule-based churn risk baseline
- Implement random/naive intent baseline for comparison
- Document findings and update data-dictionary if needed

### Notebook
- `notebooks/01-eda.ipynb`

---

## Sprint 2: Sentiment and Frustration Model

### Objectives
- Train a supervised model for nivel_frustracion (ordinal, 3 classes)
- Compare against heuristic baseline from Sprint 1

### Tasks
- Feature engineering from texto_clean (TF-IDF, embeddings)
- Feature engineering from context (turn_number, flow_name, agente)
- Train and evaluate ordinal classification models
- Evaluate with F1-weighted, confusion matrix, per-class metrics
- Error analysis: review misclassified examples
- Export model pipeline for reuse

### Notebook
- `notebooks/02-sentiment-model.ipynb`

---

## Sprint 3: Intent Detection and Churn Prediction

### Objectives
- Train a supervised intent classifier (multiclass, 4 classes)
- Train a churn risk model (binary, imbalanced)
- Evaluate both against baselines from Sprint 1

### Tasks
- Train and evaluate intent classifier (F1-macro)
- Feature engineering for session-level churn prediction
- Train and evaluate churn risk model (AUC-PR)
- Handle class imbalance with weighted loss and/or oversampling
- Error analysis per class for both models
- Export both model pipelines

### Notebooks
- `notebooks/03-intent-model.ipynb`
- `notebooks/04-churn-model.ipynb`

---

## Sprint 4: Pattern Analysis and Dashboard

### Objectives
- Aggregate outputs from all models into actionable insights
- Build an interactive dashboard for the product team

### Tasks
- Cross-analysis: frustration x intent x resolution x churn
- Identify top unresolved intents per flow
- Identify escalation and abandonment patterns
- Build Streamlit dashboard with filters (flow, intent, date, agent)
- Document actionable recommendations
- Prepare final project report

### Outputs
- `notebooks/05-pattern-analysis.ipynb`
- `dashboard/` (Streamlit app)
- `docs/final-report.md`
