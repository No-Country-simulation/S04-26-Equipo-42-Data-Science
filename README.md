# ConversaAI — Sentiment & Intent Analysis

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue?logo=python)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red?logo=streamlit)](https://streamlit.io/)
[![uv](https://img.shields.io/badge/uv-package%20manager-green)](https://docs.astral.sh/uv/)
[![CRISP--DM](https://img.shields.io/badge/methodology-CRISP--DM-lightgrey)](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)

ML-powered analysis of customer support conversations for **ConversaAI**.
The project follows **CRISP-DM** methodology to classify user frustration,
detect intent, identify churn patterns, and surface insights through an
interactive dashboard.

---

## Status

All four supervised models are built, evaluated, and exported. The interactive
dashboard is live and ready for stakeholder review.

| Phase | Notebook | Status |
|-------|----------|--------|
| Business Understanding | — | ✅ Charter, scope, sprint plan |
| Data Understanding | [`01-eda.ipynb`](notebooks/01-eda.ipynb) | ✅ |
| Data Preparation | (handled upstream by DE team) | ✅ |
| Modeling — Frustration | [`02-sentiment-model.ipynb`](notebooks/02-sentiment-model.ipynb) | ✅ |
| Modeling — Intent | [`03-intent-model.ipynb`](notebooks/03-intent-model.ipynb) | ✅ |
| Modeling — Churn | [`04-churn-model.ipynb`](notebooks/04-churn-model.ipynb) | ✅ |
| Evaluation | [`05-pattern-analysis.ipynb`](notebooks/05-pattern-analysis.ipynb) | ✅ |
| Deployment | Dashboard | ✅ |

---

## Quick start

```bash
# Install dependencies
uv sync

# Launch notebooks
uv run jupyter lab

# Launch dashboard
uv run streamlit run dashboard/app.py
```

> Requires Python 3.12+. Package manager: [uv](https://docs.astral.sh/uv/).

---

## Project structure

```
├── data/                          # Preprocessed dataset (20K conversations)
├── data_engineering/              # DE sub-project — do not modify
├── dashboard/                     # Streamlit application (modular)
│   ├── app.py                     # Entry point (orchestrator)
│   ├── config.py                  # Constants, colors, paths
│   ├── data.py                    # Cached data loading
│   ├── sidebar.py                 # Filter controls
│   ├── overview.py                # Tab: high-level KPIs
│   ├── flows_intents.py           # Tab: per-flow / per-intent breakdown
│   ├── agents.py                  # Tab: agent performance
│   ├── trends.py                  # Tab: temporal trends
│   ├── correlation.py             # Tab: correlation matrix
│   └── export.py                  # Tab: CSV / JSON / markdown export
├── docs/                          # Project documentation
│   ├── data-dictionary.md         # Column and target definitions
│   ├── ml-charter.md              # Scope, metrics, risks
│   ├── sprint-plan.md             # Sprint-based work plan
│   └── tech-stack-roadmap.md      # V1–V3 evolution
├── models/                        # Exported pipelines (.pkl + .json)
│   ├── frustration_model.pkl
│   ├── intent_model.pkl
│   └── churn_model.pkl
├── notebooks/                     # CRISP-DM notebooks (numbered)
│   ├── 01-eda.ipynb
│   ├── 02-sentiment-model.ipynb
│   ├── 03-intent-model.ipynb
│   ├── 04-churn-model.ipynb
│   └── 05-pattern-analysis.ipynb
├── reports/                       # Reports with inline figures
│   ├── eda-report.md
│   ├── sentiment-model-report.md
│   ├── intent-model-report.md
│   ├── churn-model-report.md
│   └── pattern-analysis-report.md
├── src/                           # Reusable modules (future)
│   └── sentiment_analysis/
├── pyproject.toml                 # Project metadata + dependencies
└── README.md
```

---

## Models

All models were trained on **synthetic/deterministic data** (20,001 rows, 0 nulls).
Performance reflects dataset construction rules, not real-world behavior.

| Target | Type | Classes | Balanced | Key Metric | Notes |
|--------|------|---------|----------|------------|-------|
| **Frustration** (`nivel_frustracion`) | Ordinal classification | 3 (0/1/2) | ❌ Imbalanced | 100% accuracy | Perfect separation by `turn_number` |
| **Intent** (`intencion`) | Multiclass | 4 | ✅ Balanced | 100% accuracy | 1:1 mapping with `flow_name` |
| **Churn** (`es_churn_risk`) | Binary | 2 | ❌ 12% pos | 1.00 PR-AUC | 100% correlated with `nivel_frustracion==2` |
| **Resolution** (`resolved`) | Binary | 2 | ❌ 22% pos | — | Exported for dashboard use |

> Model reports with detailed evaluation figures are in [`reports/`](reports/).

---

## Dashboard

The interactive dashboard provides six views into the data:

| Tab | What it shows |
|-----|---------------|
| 📊 **Overview** | KPIs (sessions, churn, resolution, frustration), outcome distribution, global metrics |
| 🔄 **Flows & Intents** | Per-flow comparison, frustration by flow, churn/resolution by intent |
| 👤 **Agents** | Agent-level aggregation, scatter plot, churn/resolution leaderboards, search |
| 📈 **Temporal Trends** | Monthly frustration, churn, and resolution trends; per-flow time series |
| 🔗 **Correlations** | Cross-correlation heatmap, strip plots for key variable pairs |
| 📥 **Export** | Download filtered CSV, metrics JSON, or executive summary markdown |

All tabs respect sidebar filters (flow, intent, frustration range, date range).

```bash
uv run streamlit run dashboard/app.py
```

---

## Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.12 |
| **ML / Data** | scikit-learn 1.8, pandas 3.0, numpy 2.4 |
| **Visualization** | matplotlib, seaborn, plotly |
| **Dashboard** | Streamlit 1.57, Plotly |
| **Notebooks** | Jupyter Lab |
| **Package mgmt** | [uv](https://docs.astral.sh/uv/) |
| **Methodology** | CRISP-DM |

---

## Documentation

- [`docs/data-dictionary.md`](docs/data-dictionary.md) — All 15 columns, types, and targets
- [`docs/ml-charter.md`](docs/ml-charter.md) — Project scope, success criteria, risks, roadmap
- [`docs/sprint-plan.md`](docs/sprint-plan.md) — Sprint-based work plan and deliverables
- [`docs/tech-stack-roadmap.md`](docs/tech-stack-roadmap.md) — V1 to V3 architecture evolution

---

## License

Academic project — No Country.
