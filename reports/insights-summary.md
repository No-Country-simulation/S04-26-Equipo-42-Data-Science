# Insights Summary — ConversaAI

**Version:** 1.0
**Fecha:** Mayo 2026
**Fuente:** Analisis cruzado de los reportes de EDA, sentiment, intent, churn y pattern-analysis

> **Nota importante:** Todos los hallazgos se basan en un dataset sintetico
> deterministico (20,001 registros, 6.648 sesiones). Los patrones descritos
> reflejan reglas de construccion del corpus, no comportamiento real de
> usuarios. El valor del proyecto reside en el pipeline validado y en los
> tipos de analisis que seran accionables cuando se procesen conversaciones
> reales.

---

## Resumen

El proyecto entrega un pipeline CRISP-DM completo para analisis de
sentimiento e intencion en conversaciones de soporte. Se entrenaron,
validaron y exportaron tres modelos supervisados (frustracion, intencion,
churn). Un dashboard interactivo con seis vistas permite monitoreo en
tiempo real.

**Hallazgo central:** El dataset sintetico sigue reglas deterministicas
donde el nivel de frustracion determina completamente el resultado de cada
sesion. Esto implica que las metricas actuales de los modelos (100% de
precision) son artificialmente perfectas. El pipeline, la arquitectura y
el dashboard estan listos para produccion, pero los modelos requeriran
reentrenamiento con datos reales antes de su despliegue.

---

## Hallazgos Principales

### 1. La Frustracion es la Senal Mas Importante

El nivel de frustracion (`nivel_frustracion`) determina completamente
tanto el churn como la resolucion:

| Nivel de Frustracion | Tasa de Resolucion | Tasa de Churn | Interpretacion |
|---------------------|-------------------|---------------|----------------|
| Baja (0) | ~36% | 0% | Puede resolverse, pero no esta garantizado |
| Media (1) | 0% | 0% | Nunca se resuelve, pero no genera abandono |
| Alta (2) | 0% | 100% | Siempre lleva al abandono |

**Implicacion:** En produccion, monitorear la frustracion en tiempo real
permite intervenir antes de que un usuario alcance el nivel 2. El sistema
actual detecta churn despues de que ocurre. La oportunidad real esta en
prevenirlo.

### 2. La Intencion esta Determinada por el Flujo de Soporte

Cada `flow_name` mapea 1:1 con una `intencion`:

| Flow | Intencion |
|------|-----------|
| Acceso y Seguridad | error_login |
| Gestion de Cuenta | cambio_plan |
| Soporte Tecnico y Despacho | logistica_envio |
| Facturacion y Cobros | problema_pago |

**Implicacion:** En produccion, el equipo puede encaminar conversaciones
segun el `flow_name` y saber que categoria de intencion esperar. Si los
datos reales muestran discrepancias (por ejemplo, errores de login
reportados en el flujo de facturacion), eso seniala un problema de
experiencia de usuario que vale la pena investigar.

### 3. Todos los Flujos se Comportan de forma Identica (en Datos Sinteticos)

Los cuatro flujos presentan metricas practicamente identicas:

| Flow | Frustracion Promedio | Tasa de Churn | Tasa de Resolucion | Turnos Promedio |
|------|---------------------|---------------|-------------------|-----------------|
| Acceso y Seguridad | 1.34 | 33.8% | 66.3% | 3.0 |
| Facturacion y Cobros | 1.37 | 37.4% | 62.7% | 3.0 |
| Gestion de Cuenta | 1.35 | 35.3% | 64.9% | 3.0 |
| Soporte Tecnico | 1.36 | 35.6% | 64.6% | 3.0 |

**Implicacion:** Con datos reales, aparecera variacion entre flujos. El
dashboard ya esta configurado para detectar que flujos rinden por debajo
del promedio. Durante la migracion, prestar atencion a flujos con:

- Frustracion superior al promedio (posibles problemas de diseno del flujo)
- Resolucion inferior al promedio (oportunidades de capacitacion de agentes)
- Churn superior al promedio (intervencion urgente)

### 4. El Resultado de la Sesion esta Determinado por la Frustracion Maxima

El analisis a nivel sesion revela una regla exacta:

> `frustracion_maxima = 1 -> sesion resuelta (100%)`
> `frustracion_maxima = 2 -> sesion con churn (100%)`

No existen sesiones "activas" (sin resolver y sin churn). Esto es un
artefacto de los datos sinteticos. En escenarios reales, el equipo debe
esperar una proporcion significativa de sesiones sin resultado definido
que requieran seguimiento.

### 5. Los Modelos de Solo Texto Alcanzan Precision Perfecta en Intencion y Churn

Los modelos supervisados que usan unicamente `texto_clean`
(TF-IDF + RandomForest) alcanzan 100% de precision sin features
contextuales como `flow_name` o `turn_number`:

| Modelo | Features | Precision | Tamano |
|--------|----------|-----------|--------|
| Frustracion | texto + contexto (92 dims) | 100% | 588 KB |
| Intencion | solo texto (89 dims) | 100% | 456 KB |
| Churn | solo texto (89 dims) | 100% | 301 KB |

**Implicacion:** El enfoque de solo texto para intencion y churn es
prometedor para produccion porque elimina la dependencia de metadatos
auxiliares. Sin embargo, la precision caera con datos reales. Se
recomienda establecer una linea de base con reglas heuristicas y mejorar
de forma iterativa.

---

## Capacidades del Dashboard

El dashboard de Streamlit (6 pestanas) esta operativo y conectado al
pipeline de datos:

| Pestana | Proposito | Metricas Clave |
|---------|-----------|----------------|
| Overview | KPIS globales | Sesiones, tasa de churn, tasa de resolucion, frustracion promedio |
| Flujos e Intenciones | Desglose por flujo | Frustracion por flujo, churn y resolucion por intencion |
| Agentes | Agregacion por agente | Volumen, tasa de churn, tasa de resolucion por agente |
| Tendencias | Monitoreo temporal | Evolucion mensual de frustracion, churn y resolucion |
| Correlaciones | Analisis cruzado | Matriz de correlacion, graficos de dispersion |
| Exportar | Descarga de datos | Exportacion a CSV, JSON y markdown |

Todas las pestanas respetan los filtros de flujo, intencion, nivel de
frustracion y rango de fechas.

---

## Recomendaciones para la Migracion a Datos Reales

| Prioridad | Accion | Motivo |
|-----------|--------|--------|
| P1 | Reentrenar los tres modelos con datos reales | Los modelos actuales estan sobreajustados a reglas deterministicas; las metricas caeran significativamente |
| P1 | Establecer metricas de base con reglas heuristicas (turn_number, flow_name) | Las heuristicas son interpretables, economicas y sirven como referencia para medir mejora del ML |
| P2 | Comparar rendimiento de solo texto vs texto + contexto | En datos reales, las features contextuales pueden agregar senal; en datos sinteticos no fue necesario |
| P2 | Monitorear la variacion entre flujos cuando lleguen datos reales | Los flujos homogeneos son un artefacto sintetico; la variacion real es esperable y valiosa |
| P3 | Implementar alertas de escalada de frustracion | La funcionalidad de mayor impacto: detectar transiciones de nivel 1 a nivel 2 de frustracion de forma temprana |
| P3 | Evaluar embeddings (sentence-transformers) vs TF-IDF | TF-IDF funciono porque el vocabulario era perfectamente discriminativo; los datos reales pueden requerir comprension semantica |

---

## Que Monitorear en Produccion

Una vez operando con datos reales, hacer seguimiento semanal de estas
metricas:

1. Distribucion de frustracion por flujo: identificar que flujos son
   sistematicamente mas frustrantes.
2. Tasa de churn por intencion: determinar que intenciones tienen mayor
   probabilidad de terminar en abandono.
3. Tasas de resolucion por agente: detectar agentes que resuelven
   consistentemente vs. aquellos que escalan.
4. Tendencias temporales: identificar patrones semanales, mensuales o
   estacionales en la frustracion.
5. Deriva del modelo: verificar si los puntajes de confianza de las
   predicciones se degradan con el tiempo.

---

## Limitaciones

| Limitacion | Impacto | Mitigacion |
|------------|---------|------------|
| Dataset 100% sintetico | Todas las metricas son artificialmente perfectas | Documentar claramente; el entregable es el pipeline, no las metricas |
| Sin patrones temporales | No es posible validar analisis de tendencias | Las vistas de tendencias del dashboard estan listas; los datos reales proveeran la primera senal significativa |
| Sin datos bilinguees | Modelos en portugues no probados | Los modelos usan solo `texto_clean`; la capacidad bilingue requiere datos adicionales |
| Flujos homogeneos | La comparacion entre flujos no es significativa | La variacion con datos reales validara si las vistas por flujo del dashboard son utiles |
