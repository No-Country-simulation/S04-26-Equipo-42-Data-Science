# ConversaAI -- Sentiment & Intent Analysis

Python 3.12 project managed with **uv** (not pip/conda). CRISP-DM methodology.

## Quick start

```bash
uv sync                           # install all dependencies
uv add <package>                  # add a new dependency
uv run python script.py           # run with project venv
uv run jupyter lab                # launch notebooks
```

## Key paths

- `data/processed/data_preprocessed.csv` -- symlink to the 20K-row dataset
  (actual source: `data_engineering/data/processed/data_preprocessed.csv`)
- `src/sentiment_analysis/` -- Python package
- `notebooks/` -- Jupyter notebooks for EDA and modeling
- `docs/data-dictionary.md` -- reference for all 15 columns, types, targets
- `docs/ml-charter.md` -- ML project scope, metrics, risks, roadmap
- `data_engineering/` -- DE work, do not modify

## Dataset essentials

- 20,001 rows, 15 cols, **zero nulls**, text already preprocessed (`texto_clean`)
- Four labeled targets available for supervised learning:
  - `nivel_frustracion` (0/1/2 -- ordinal, imbalanced)
  - `intencion` (4 classes -- balanced)
  - `es_churn_risk` (0/1 -- imbalanced, 12%)
  - `resolved` (0/1 -- imbalanced, 22%)
- `nivel_frustracion==2` and `es_churn_risk==1` share identical count (2,364) -- likely correlated
- `flow_name` maps 1:1 to `intencion`

## Git conventions

- **Branch:** work on `ml/sentiment`, protect `main`
- **Commits:** conventional commits (`feat:`, `docs:`, `chore:`, etc.), atomic
- **Authorization:** show staged changes to the user BEFORE committing. Do not commit without explicit approval.
- No `--force` push, no push to `main`

## Documentation style

- No emojis in docs or commit messages
- Professional, clear, no AI-generated tone
- Prefer Spanish for project docs

## Project skills installed (`.agents/skills/`)

- `exploratory-data-analysis` -- for EDA phase
- `nlp-natural-language-processing` -- text processing, transformers, spaCy
- `scikit-learn-best-practices` -- modeling workflow, pipelines, evaluation
- `ml-pipeline-workflow` -- end-to-end ML pipeline orchestration
- `Sentiment Analysis` -- sentiment classification approaches

## User workflow preference

- Every staged change must be reviewed by the user before committing
- Documentation (data dictionary, ML charter, reports) drives the work, not the other way around
