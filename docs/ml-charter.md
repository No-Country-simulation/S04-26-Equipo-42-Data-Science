# ML Charter — ConversaAI: Sentiment & Intent Analysis

**Version:** 1.0  
**Metodologia:** CRISP-DM  
**Branch:** `ml/sentiment`  
**Fecha:** Mayo 2026

---

## 1. Business Understanding

### Problema de negocio

ConversaAI procesa mas de 2 millones de mensajes al mes en conversaciones de soporte. Actualmente se miden tasas de resolucion, pero **no se entiende el tono emocional ni si la intencion del usuario se esta capturando correctamente**. Esto dificulta mejorar los flujos de trabajo porque no hay datos claros sobre donde estan fallando.

### Objetivos de negocio

1. Identificar **cuando los usuarios se frustran** y en que flujos
2. Detectar **que intenciones no se estan resolviendo**
3. Predecir **patrones de escalamiento o abandono**
4. Proveer un **dashboard de insights** accionables para el equipo de producto

### Criterios de exito (business KPIs)

- Reducir el tiempo de identificacion de flujos problematicos (actualmente no medido → tener metrica baseline)
- Proveer al menos 3 insights accionables por sprint (ej. "las cancelaciones con frustracion tienen 70% de abandono")
- Dashboard usable por equipo de producto sin asistencia tecnica

---

## 2. Data Understanding

### Datos disponibles

- **Dataset:** `data/processed/data_preprocessed.csv` — 20,001 filas, 15 columnas
- **Origen:** Corpus de conversaciones de soporte sintetico (Data Engineering previamente realizada)
- **Calidad:** Sin valores nulos, sin valores fuera de rango, texto pre-normalizado

### Targets disponibles (supervised learning)

| Target              | Tipo                     | Clases                    | Balance       | Posible approach                     |
| ------------------- | ------------------------ | ------------------------- | ------------- | ------------------------------------ |
| `nivel_frustracion` | Clasificacion ordinal    | 0 (55%), 1 (33%), 2 (12%) | Desbalanceado | Clasificador ordinal, F1-weighted    |
| `intencion`         | Clasificacion multiclase | 4 clases (~25% c/u)       | Balanceado    | Clasificador flat, Accuracy/F1-macro |
| `es_churn_risk`     | Clasificacion binaria    | 0 (88%), 1 (12%)          | Desbalanceado | Balanced classes, AUC-PR             |
| `resolved`          | Clasificacion binaria    | 0 (78%), 1 (22%)          | Desbalanceado | Outcome feature, no target principal |

---

## 3. ML Task Definition

### Tarea 1: Clasificacion de frustracion

- **Target:** `nivel_frustracion` (0/1/2)
- **Input:** `texto_clean` + features contextuales (turn_number, flow_name, agente)
- **Tipo:** Clasificacion ordinal (o multiclase con perdida ordinal)
- **Metrica principal:** F1-weighted (macro si las clases chicas son importantes)
- **Metricas secundarias:** AUC-ROC one-vs-rest, matriz de confusion
- **Baseline heuristico:** Regla de keywords de frustracion

### Tarea 2: Deteccion de intencion

- **Target:** `intencion` (4 clases)
- **Input:** `texto_clean` + `flow_name`
- **Tipo:** Clasificacion multiclase
- **Metrica principal:** F1-macro
- **Baseline:** Zero-shot con modelos multilingues vs enfoque supervisado (evaluamos cual rinde mejor)

### Tarea 3: Prediccion de churn / abandono

- **Target:** `es_churn_risk` (0/1)
- **Input:** Features agregadas por sesion (frustracion promedio, resolved rate, duracion, cantidad de turnos)
- **Tipo:** Clasificacion binaria con desbalanceo
- **Metrica principal:** AUC-PR (preferred para desbalanceo) o F1
- **Baseline:** Reglas heuristicas (frustracion sostenida + no resuelto)

### Tarea 4: Analisis de patrones (post-modelos)

- **Objetivo:** Identificar correlaciones entre frustracion, intencion, y resultado
- **No es un modelo per se** — es agregacion de los outputs de T1+T2+T3
- **Output:** Dashboard con metricas agregadas por flujo, intent, agente, periodo

---

## 4. Approach Tecnico

### Pipeline propuesto

```
Business Understanding [OK - docs/conversa-ai.md]
        |
Data Understanding [OK - data_engineering + este charter]
        |
Data Preparation [OK - DE completo]
        |
Modeling [Sprint actual]
  ├── T1: Frustracion (supervisado)
  ├── T2: Intencion (supervisado)
  └── T3: Churn (feature engineering + modelo tabular)
        |
Evaluation [Metricas sobre test hold-out]
        |
Deployment [Dashboard + reporte]
```

### Stack tecnologico

| Componente             | Herramienta                                   | Skill asociado       |
| ---------------------- | --------------------------------------------- | -------------------- |
| Preprocesamiento texto | spaCy, expresiones regulares                  | NLP                  |
| Feature engineering    | pandas, scikit-learn                          | scikit-learn         |
| Clasificacion texto    | scikit-learn (TF-IDF + lineal) / transformers | scikit-learn, NLP    |
| Clasificacion tabular  | scikit-learn (Random Forest, XGBoost)         | scikit-learn         |
| Evaluacion             | scikit-learn metrics, confusion matrix        | scikit-learn         |
| Experiment tracking    | (TBD: WandB / MLflow)                         | —                    |
| Dashboard              | Streamlit                                     | (futuro)             |
| Orquestacion           | Notebooks estructurados + pipeline            | ml-pipeline-workflow |

### Relacion con la planificacion de actividades

El documento `Planificacion de Actividades.md` plantea una estrategia solida para el proyecto, con recomendaciones tecnicas valiosas como el uso de `pysentimiento` para analisis de sentimiento y zero-shot para deteccion de intenciones. Esas recomendaciones estan pensadas para un escenario donde no hay datos etiquetados.

Al revisar el dataset, descubrimos que si existen labels para frustracion, intencion, churn y resolucion. Esto amplia nuestras opciones: podemos mantener `pysentimiento` como baseline de comparacion y al mismo tiempo entrenar modelos supervisados que probablemente den mejor precision. Ambas aproximaciones son complementarias.

---

## 5. Success Metrics & Evaluation

### Por tarea

| Tarea       | Metrica principal | Baseline heuristico     | Objetivo minimo |
| ----------- | ----------------- | ----------------------- | --------------- |
| Frustracion | F1-weighted       | 0.55 (keyword rules)    | >0.70           |
| Intencion   | F1-macro          | 0.25 (random)           | >0.85           |
| Churn       | AUC-PR            | 0.30 (simple heuristic) | >0.50           |

### Estrategia de validacion

- **Split:** Train (70%), Validation (15%), Test (15%) — estratificado por target
- **Cross-validation:** 5-fold estratificada (StratifiedKFold)
- **Test hold-out:** Una sola evaluacion al final
- **Error analysis:** Matriz de confusion + ejemplos mal clasificados por clase

---

## 6. Non-Goals (Scope Explicito)

- NO entrenar modelos desde cero (usaremos modelos pre-entrenados + fine-tuning si es necesario)
- NO implementar pipeline de produccion en tiempo real
- NO desplegar a produccion — el entregable es un dashboard + reporte
- NO hacer traduccion automatica (el dataset ya tiene ES y PT)
- NO cubrir mas de 4 intenciones (las que ya existen en datos)

---

## 7. Riesgos y Mitigaciones

| Riesgo                                                             | Probabilidad | Impacto | Mitigacion                                                                                  |
| ------------------------------------------------------------------ | ------------ | ------- | ------------------------------------------------------------------------------------------- |
| Labels de frustracion son heuristicas/sinteticas, no reales        | Media        | Alto    | Validar con spot-check manual; si no correlacionan, pivotar a pysentimiento                 |
| Dataset es 100% sintetico (no representa datos reales)             | Alta         | Alto    | Documentar como limitacion; el pipeline debe funcionar con datos reales cambiando la fuente |
| Desbalanceo en frustracion clase 2 (12%) y churn (12%)             | Alta         | Medio   | Usar weighted loss, class weights, oversampling (SMOTE)                                     |
| texto_clean perdio informacion util al eliminar acentos/mayusculas | Media        | Bajo    | Evaluar usando texto_original como alternativa                                              |
| Sesiones de solo 3 turnos limitan analisis temporal                | Alta         | Bajo    | Features de secuencia corta; considerar bigramas de intencion                               |

---

## 8. Roadmap CRISP-DM

| Fase                   | Estado          | Entregable                                      |
| ---------------------- | --------------- | ----------------------------------------------- |
| Business Understanding | Completado      | `docs/conversa-ai.md`, `docs/ml-charter.md`     |
| Data Understanding     | Completado      | `docs/data-dictionary.md`, EDA notebook         |
| Data Preparation       | Completado (DE) | Dataset preprocesado                            |
| Modeling               | Pendiente       | Notebooks: 02-sentiment, 03-intent, 04-patterns |
| Evaluation             | Pendiente       | Reporte de metricas, matriz de confusion        |
| Deployment             | Pendiente       | Dashboard Streamlit, reporte ejecutivo          |

---

## 9. Entregables

1. **Modelos:** Pipeline de clasificacion de frustracion, intencion, y churn
2. **Dashboard:** Visualizaciones de insights por flujo, intent, frustracion
3. **Reporte:** Recomendaciones accionables para el equipo de producto
4. **Notebooks:** Reproducibles con analisis paso a paso
5. **Codigo:** Modulos en `src/sentiment_analysis/` reutilizables
