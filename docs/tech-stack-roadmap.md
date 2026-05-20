# Tech Stack Roadmap — ConversaAI

**Version:** 1.0
**Fecha:** Mayo 2026
**Metodologia:** CRISP-DM
**Branch:** `ml/sentiment`

---

## Filosofia

Este documento describe la evolucion del stack tecnologico del proyecto en fases.
Preferimos entregar una V1 funcional con herramientas simples a perder tiempo configurando infraestructura que todavia no necesitamos.
Cada fase se habilita cuando la anterior demuestra que el proyecto lo merece.

---

## Fase 1: MVP rapido (actual)

> Objetivo: tener modelos funcionando, metricas de referencia, y un dashboard usable
> en el menor tiempo posible. Aprender el dominio y validar que los enfoques elegidos funcionan.

### Stack V1

| Categoria | Herramienta | Instalado | Justificacion |
|-----------|-------------|-----------|---------------|
| **Package manager** | uv | Si | Ya decidido, no se negocia |
| **Data manipulation** | pandas, numpy | Pendiente | Estandar de industria |
| **Feature extraction (texto)** | scikit-learn (TfidfVectorizer) | Pendiente | Rapido, interpretable, suficiente para baseline |
| **Modelos tabulares** | scikit-learn (LogisticRegression, RandomForest) | Pendiente | Cubren del baseline al modelo competitivo |
| **Datos desbalanceados** | `class_weight='balanced'` (nativo sklearn) | No requiere instalacion | Sin dependencias extra |
| **Evaluacion** | scikit-learn metrics, confusion matrix, classification_report | Pendiente | Todo lo necesario para reportar resultados |
| **Visualizacion EDA** | matplotlib + seaborn | Pendiente | Estandar para analisis exploratorio |
| **Dashboard** | Streamlit + plotly | Pendiente | Rapido de prototipar, equipo de producto lo usa sin ayuda |
| **Serializacion modelos** | joblib | Pendiente | Estandar para scikit-learn |
| **Experiment tracking** | Tabla CSV en `reports/experiments.csv` | Ninguna | Suficiente para ~10-15 experimentos. Registro manual pero estructurado |
| **Testing** | Ninguno (notebooks first) | — | No se testean notebooks. Se evalua en V2 si se modulariza |

### Comandos de instalacion V1

```bash
uv add pandas numpy scikit-learn matplotlib seaborn plotly streamlit joblib
```

### Entregables V1

- Notebooks: `01-eda.ipynb`, `02-sentiment-model.ipynb`, `03-intent-model.ipynb`, `04-churn-model.ipynb`
- Dashboard: `dashboard/` con Streamlit
- Reporte de experimentos: `reports/experiments.csv`
- Modelos serializados: `models/` con pipelines en joblib

---

## Fase 2: Profesionalizacion (proxima iteracion)

> Objetivo: incorporar herramientas de la industria sin sobreingenieria.
> Se activa CUANDO la V1 esta funcionando y el proyecto justifica la inversion.

### Stack V2

| Categoria | Herramienta | Cambio respecto a V1 |
|-----------|-------------|----------------------|
| **Experiment tracking** | MLflow (open source, local) | Reemplaza tabla CSV. UI web para comparar experimentos, log de parametros, metricas y artifacts |
| **Feature extraction avanzada** | sentence-transformers (`all-MiniLM-L6-v2`) | Agrega embeddings semanticos como alternativa a TF-IDF |
| **Modelos boosting** | XGBoost o LightGBM | Agrega modelo estado del arte para datos tabulares |
| **Datos desbalanceados** | imbalanced-learn (SMOTE) | Agrega oversampling sintetico si class_weight no alcanza |
| **Estructura de codigo** | Modularizacion en `src/sentiment_analysis/` | Mover logica reutilizable de notebooks a modulos Python |
| **Testing** | pytest | Tests para modulos de features y prediccion (no para modelos) |
| **Configuracion** | YAML o archivo de config | Parametros centralizados, no hardcodeados en notebooks |

### Instalacion adicional V2

```bash
uv add mlflow sentence-transformers xgboost imbalanced-learn pytest
```

### Entregables V2

- MLflow UI local con historial de experimentos
- Notebook `05-experiments.ipynb` con comparacion de resultados via MLflow
- Modulos Python en `src/sentiment_analysis/features.py`, `models.py`, `tracking.py`
- Tests unitarios para modulos principales
- Dashboard mejorado con filtros avanzados

---

## Fase 3: Automatizacion (vision a futuro)

> Objetivo: explorar AutoML y herramientas cloud si el proyecto escala.
> No planificado — solo documentado como referencia para decisiones futuras.

| Herramienta | Que resuelve | Consideraciones |
|-------------|--------------|-----------------|
| **AutoGluon** / **auto-sklearn** | Automatiza seleccion de modelo + hiperparametros | Util cuando ya entendemos el problema manualmente. No reemplaza el aprendizaje |
| **MLflow + servidor remoto** | Tracking compartido en equipo | Solo si el equipo crece o los experimentos superan ~50 |
| **Azure ML / Vertex AI** | Plataforma completa cloud | Proyecto deberia estar en produccion para justificar el costo |
| **DVC** | Versionado de datasets y modelos | Solo si los datasets crecen mas alla de lo que Git puede manejar |

---

## Notas importantes

1. **No saltarse fases**: pasar directamente a V2 o V3 sin entender los datos ni los modelos manualmente es ineficiente. AutoML sin entender que hace da resultados pero no ensena.
2. **Cada fase se evalua**: antes de pasar a la siguiente, revisar si realmente se necesita. No instalar herramientas por instalar.
3. **Compatibilidad hacia atras**: V2 no rompe V1. Todo lo que funcione en V1 sigue funcionando. Las mejoras son aditivas, no sustitutivas.
4. **El objetivo final es aprender y entregar valor**: no tener el stack mas sofisticado del mundo.
