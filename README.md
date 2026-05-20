# ConversaAI — Sentiment & Intent Analysis

Sentiment and intent analysis on customer support conversations for ConversaAI.
The project follows the **CRISP-DM** methodology to build an ML pipeline that
classifies user frustration levels, detects the intent behind each message, and
identifies churn patterns.

It uses a labeled dataset of 20,000 support conversations with four targets:
frustration (3 levels), intent (4 classes), churn risk, and resolution status.
The focus is on generating actionable insights for the product team through an
interactive dashboard.

---

## Quick start

```bash
uv sync
uv run jupyter lab
```

---

## Project structure

```
data/       — preprocessed dataset (20K conversations)
docs/       — project documentation
models/     — exported pipelines (.pkl)
notebooks/  — numbered notebooks by CRISP-DM phase
reports/    — findings and figures
src/        — reusable modules
```

> For a detailed reference, see [`docs/project-structure.md`](docs/project-structure.md).

---

## Stack

`Python 3.12` · `scikit-learn` · `pandas` · `matplotlib` · `seaborn` · `plotly`

Managed with [uv](https://docs.astral.sh/uv/).

---

## Documentation

- [`docs/data-dictionary.md`](docs/data-dictionary.md) — column and target definitions
- [`docs/ml-charter.md`](docs/ml-charter.md) — project scope, metrics, risks
- [`docs/sprint-plan.md`](docs/sprint-plan.md) — sprint-based work plan
- [`docs/tech-stack-roadmap.md`](docs/tech-stack-roadmap.md) — V1 to V3 evolution

---

## License

Academic project — No Country.
