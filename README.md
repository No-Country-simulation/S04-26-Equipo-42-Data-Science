<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-1.8-orange?logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Streamlit-1.57-red?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/uv-package%20manager-green?logo=uv" alt="uv">
  <img src="https://img.shields.io/badge/CRISP--DM-complete-blue" alt="CRISP-DM">
</p>

<h1 align="center">ConversaAI</h1>
<p align="center"><em>Sentiment & Intent Analysis for Customer Support Conversations</em></p>

<p align="center">
  Three machine learning models analyze frustration, intent, and churn from
  support conversations. An interactive dashboard surfaces actionable insights
  for product teams.
</p>

<br>

---

## Demo

<p align="center">
  <a href="https://www.youtube.com/watch?v=5pAGcT9N79k">
    <img src="https://img.shields.io/badge/▶%20Watch%20the%20demo-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch the demo">
  </a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://conversa-ai.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Dashboard-Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Dashboard">
  </a>
</p>

---

## Overview

ConversaAI applies supervised learning to customer support conversations,
following the CRISP-DM methodology end-to-end. The project delivers:

- **Three trained models** for frustration level, intent detection, and churn
  risk, exported as reusable pipelines.
- **An interactive dashboard** with six views — overview, flows, agents, trends,
  correlations, and data export — all connected through synchronized filters.
- **Six analytical reports** documenting every phase: EDA, model evaluations,
  cross-target pattern analysis, and an executive summary.

The pipeline was validated on a synthetic dataset (20,001 conversations) and is
ready to ingest real data with minimal changes.

---

## Quick Start

```bash
uv sync                          # install dependencies
uv run streamlit run dashboard/app.py  # launch dashboard
uv run jupyter lab               # explore notebooks
```

> Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

---

## Models

| Target | Approach | Key Metric |
|--------|----------|------------|
| Frustration (`nivel_frustracion`) | RandomForest + TF-IDF + context | F1-weighted: 1.00 |
| Intent (`intencion`) | RandomForest + TF-IDF (text only) | F1-macro: 1.00 |
| Churn (`es_churn_risk`) | RandomForest + TF-IDF (text only) | AUC-PR: 1.00 |

> **Important:** These metrics reflect the deterministic nature of the synthetic
> dataset. Real data will introduce noise and require retraining.

---

## Dashboard

Six interconnected tabs, all respecting sidebar filters:

| Tab | Purpose |
|-----|---------|
| Overview | Global KPIs and outcome distribution |
| Flows & Intents | Per-flow frustration and per-intent resolution |
| Agents | Agent-level aggregation with search |
| Trends | Monthly evolution of all key metrics |
| Correlations | Cross-variable heatmap and strip plots |
| Export | Download filtered data as CSV, JSON, or markdown |

---

## Reports

| Report | Content |
|--------|---------|
| [`EDA Report`](reports/eda-report.md) | Data exploration and deterministic patterns |
| [`Frustration Model`](reports/sentiment-model-report.md) | Sentiment classification methodology |
| [`Intent Model`](reports/intent-model-report.md) | Intent detection methodology |
| [`Churn Model`](reports/churn-model-report.md) | Churn prediction methodology |
| [`Pattern Analysis`](reports/pattern-analysis-report.md) | Cross-target session-level insights |
| [`Insights Summary`](reports/insights-summary.md) | Executive summary and recommendations |

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.12 |
| ML & Data | scikit-learn 1.8, pandas 3.0, numpy 2.4 |
| Visualization | matplotlib, seaborn, plotly |
| Dashboard | Streamlit 1.57 |
| Package Manager | uv |
| Methodology | CRISP-DM |

---

## Documentation

Full documentation index at [`docs/README.md`](docs/README.md).

- [Data Dictionary](docs/data/data-dictionary.md) — Column definitions and targets
- [ML Charter](docs/models/ml-charter.md) — Scope, risks, and success criteria
- [Sprint Plan](docs/models/sprint-plan.md) — Work plan and deliverables
- [Tech Roadmap](docs/models/tech-stack-roadmap.md) — V1 to V3 architecture evolution

---

## License

Academic project — No Country.
