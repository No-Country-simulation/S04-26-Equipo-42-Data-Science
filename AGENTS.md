# ConversaAI -- Sentiment & Intent Analysis

Python 3.12 project managed with **uv** (not pip/conda). CRISP-DM methodology.
Notebook-driven: `src/sentiment_analysis/` is empty (`__init__.py` only).
Dashboard at `dashboard/` is planned but not yet implemented.

## Quick start

```bash
uv sync                           # install all dependencies
uv add <package>                  # add a new dependency
uv run python script.py           # run with project venv
uv run jupyter lab                # launch notebooks
```

Dependencies: `scikit-learn>=1.8.0`, `pandas>=3.0`, `numpy>=2.4`, `matplotlib`, `seaborn`, `plotly`.
No build/typecheck/lint/test infrastructure configured.

## Key paths

- `data/processed/data_preprocessed.csv` -- symlink to the 20K-row dataset
  (actual source: `data_engineering/data/processed/data_preprocessed.csv`)
- `data_engineering/` -- separate DE sub-project, **do not modify**
- `notebooks/` -- Jupyter notebooks, numbered sequentially (`01-eda.ipynb`, `02-sentiment-model.ipynb`, ...)
- `docs/data-dictionary.md` -- reference for all 15 columns, types, targets
- `docs/ml-charter.md` -- ML project scope, metrics, risks, roadmap
- `reports/` -- Markdown reports with inline images from `reports/figures/`
- `models/` -- exported pipelines via joblib (`.pkl`) + metadata (`.json`)
- `.agents/skills/` -- installed agent skills (do not modify directly)

## Dataset essentials

- 20,001 rows, 15 cols, **zero nulls**, text already preprocessed (`texto_clean`)
- Four labeled targets available for supervised learning:
  - `nivel_frustracion` (0/1/2 -- ordinal, imbalanced)
  - `intencion` (4 classes -- balanced)
  - `es_churn_risk` (0/1 -- imbalanced, 12%)
  - `resolved` (0/1 -- imbalanced, 22%)
- `nivel_frustracion==2` and `es_churn_risk==1` share identical count (2,364)
- `flow_name` maps 1:1 to `intencion`

## Git conventions

- **Branch:** work on `ml/sentiment`, protect `main`
- **Commits:** conventional commits in **English** (`feat:`, `docs:`, `chore:`, etc.), **atomic**
- **Authorization:** show staged changes to the user BEFORE committing. Do not commit without explicit approval.
- No `--force` push, no push to `main`

## Workflow

1. Read docs (`data-dictionary.md`, `ml-charter.md`, relevant reports) before writing code
2. Show every staged change to the user for approval
3. Commit atomic changes with English conventional messages
4. Documentation drives the work, not the other way around
