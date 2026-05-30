> 📌 **Documentación inicial** — Este documento refleja el diseño o propuesta original del proyecto y puede no coincidir con la implementación final. Consultá los documentos en `docs/data/`, `docs/models/` y `dashboard/` para la documentación vigente.

# Problema

Build a sentiment and intent analysis system on the corpus of support conversations to identify when users become frustrated, which intentions are not being resolved, and what patterns predict escalation or abandonment.

## Descripción

ConversaAI processes over 2 million messages per month. Currently, resolution rates are measured, but emotional tone and whether user intent is being accurately captured are not understood. This makes it difficult to improve workflows because there is no clear data on where they are failing.

## Expectations

Text processing pipeline for conversations in Spanish and Portuguese. Sentiment classification model with evaluation metrics. Intent detection model. Insights dashboard with top unresolved intentions and moments of greatest frustration. Report with actionable recommendations for conversational workflows.

### Users

ConversaAI product team that designs and improves conversational workflows. Data analyst who processes the corpus monthly.

### Flows

Analyst loads the month's conversation corpus → the pipeline cleans and processes the texts → the models classify each message by sentiment and intent → the system aggregates the results → the dashboard displays the most relevant patterns → the product team identifies the flows with the most frustration → prioritizes improvements for the next sprint.
