## **PLANIFICACIÓN DE ACTIVIDADES**

##  Estrategia General (2 semanas)

| Fase | Días | Responsables | Entregable clave |
| :---- | :---- | :---- | :---- |
| 1\. Data Understanding & Preparation | 1–3 | DE \+ DS | Corpus limpio, etiquetas aproximadas (pseudo-labeling) |
| 2\. Sentiment Analysis (MVP) | 4–6 | DS1 | Modelo de sentimiento (negativo/neutral/positivo) \+ frustración |
| 3\. Intent Detection (MVP) | 5–7 | DS2 | Clasificador de intenciones (5–10 categorías) o zero-shot |
| 4\. Pattern Analysis (Escalamiento/Abandono) | 7–9 | MLE \+ DS | Reglas \+ modelo ligero (ej. Random Forest sobre features) |
| 5\. Dashboard & Report | 9–11 | MLE \+ DE | Panel interactivo (Streamlit / Power BI) y recomendaciones |
| 6\. Integración & Presentación | 11–14 | Todo el equipo | Pipeline reproducible \+ presentación ejecutiva |

---

## 

## 🧠 Decisiones Técnicas Clave (Evitando trampas comunes)

### 1\. **Procesamiento de texto (Español/Portugués)**

- Usar `spaCy` con modelos `es_core_news_md` y `pt_core_news_md` o `nltk`.  
- Normalización ligera: minúsculas, eliminar caracteres especiales, expandir contracciones comunes.  
- **No hacer stemming agresivo** – el contexto emocional se pierde.  
- Manejar emojis ↔ texto (ej. `😠` → `enojado`).

### 2\. **Sentiment & Frustration** (sin etiquetas previas)

- **Opción más rápida**: `pysentimiento` (modelos preentrenados para ES/PT, incluye emociones básicas). Da neg/neu/pos \+ emociones como enojo.  
- **Frustración específica**: regla heurística sobre sentimiento negativo sostenido \+ palabras clave (`"no funciona"`, `"siempre igual"`, `"inútil"`) \+ cambios de tono (mayúsculas, signos).  
- **Métrica útil**: *Negative Sentiment Rate por conversación* y su evolución.

### 3\. **Intent Detection** (sin etiquetas)

- No da tiempo a entrenar clasificador supervisado.  
- **Zero-shot con modelos multilingües**: `BART-zero-shot` o `xlm-roberta-large-xnli` (definir 5–10 intents de negocio: *cancelación, facturación, error técnico, consulta, pago, cambio datos, etc.*).  
- Alternativa más simple: **clustering \+ asignación manual de nombres** (ej. BERTopic, K-Means con embeddings de `all-MiniLM-L6-v2`). El equipo de producto puede validar nombres.

### 4\. **Escalamiento / Abandono** (patrones predictivos)

- Anotar como *abandono* conversaciones donde el usuario no responde después de X turnos.  
- *Escalamiento* si hay derivación a humano o mención de “hablar con supervisor”.  
- Construir features: longitud, turnos, sentimiento promedio, cambio de sentimiento, intents no resueltos, tiempo entre respuestas.  
- Modelo simple: **Random Forest** con shap para interpretar patrones.

### 5\. **Dashboard** (para equipo de producto)

- Métricas clave: intenciones no resueltas por workflow, frustración por intent, tasas de abandono/escalamiento por semana.  
- Usar **Streamlit** (rápido de montar) con filtros por fecha, idioma, intent.  
- Visualización de ejemplo: *“Top 3 intents con mayor frustración”* \+ ejemplos de frases reales (anonymizadas).

---

## 👥 División de Roles (Ejemplo concreto)

| Rol | Tareas específicas |
| :---- | :---- |
| **Data Engineer** | – Conectar a fuente de datos (CSV, API, DB).  – Limpieza inicial y unificación de campos (conversación por fila, timestamp, turnos). – Guardar corpus procesado en formato parquet. – Automatizar pipeline diario (opcional, pero útil para demo). |
| **DS1 (Sentiment)** | – Implementar `pysentimiento` sobre corpus.  – Calcular frustración por heurística (negativo \+ keywords). – Generar métricas de sentimiento por conversación/turno. – Validar con ejemplos (spot-check). |
| **DS2 (Intent)** | – Usar zero-shot o clustering para asignar intents.  – Mapear a categorías de negocio (validar con equipo de producto en 1 reunión). – Identificar intents no resueltos (según fin de conversación). |
| **MLE** | – Construir features para escalamiento/abandono.  – Entrenar Random Forest y seleccionar top features. – Montar Streamlit dashboard integrando salidas de DS1+DS2. – Empaquetar todo en un notebook ejecutable \+ script. |

**Nota**: Todos trabajan sobre el mismo repositorio (Git) y hacen code reviews ligeros. Reunión diaria de 15 min.

## ⚠️ Riesgos y Mitigaciones (para el hackathon)

| Riesgo | Mitigación |
| :---- | :---- |
| Datos desbalanceados o sin etiquetas | Usar modelos preentrenados y heurísticas; el valor está en patrones, no en precisión absoluta. |
| Lenguaje informal / mezcla ES/PT | Mantener modelos multilingües; si falla mucho, traducir automáticamente (Google Translate API) solo para sentimiento – pero ojo con coste. |
| Falta de definición de intenciones | Definir 5 intents con el cliente el día 1\. Usar frases reales para afinar prompts del zero-shot. |
| Dashboard poco útil | Enfocar en **3 preguntas que el producto quiere responder** (ej. “¿qué intent causa más abandono?”). Iterar rápido. |

---

## 📈 KPIs Reales para la Presentación (No solo F1)

- **Cobertura**: % de conversaciones donde se detectó sentimiento e intent.  
- **Insights accionables**: Ejemplos concretos (ej. *“Cancelaciones con frustración tienen 70% de abandono”*).  
- **Simplicidad**: ¿Puede el equipo de producto usar el dashboard sin ayuda técnica?  
- **Tiempo de ejecución** del pipeline completo (\< 30 min sobre 2M mensajes – si es mucho, muestrear).

---

## 🚀 Plan de Arranque (Día 1\)

1. **Reunión de 1 hora** con el equipo (y stakeholders si es posible) para alinear intents y definición de frustración/abandono.  
2. **Crear repositorio** con estructura:  
     
   /data/raw, processed  
     
   /notebooks/ 01\_EDA, 02\_sentiment, 03\_intent, 04\_patterns  
     
   /src/ preprocessing, sentiment, intent, features, dashboard  
     
   README.md, requirements.txt  
     
3. **Explorar una muestra** de 5k conversaciones para entender jerga, longitud, idioma predominante.  
4. **Implementar baseline** de sentimiento con `pysentimiento` – debería funcionar en horas.

---

## 💎 Recomendación Final

**No intenten entrenar modelos desde cero** – es una trampa común en hackathones. Usen lo que ya funciona (`pysentimiento`, zero-shot, embeddings multilingües). Concéntrense en **conectar sentimiento \+ intent \+ resultado** (escalamiento/abandono) para mostrar patrones que el negocio no ve hoy. El dashboard debe tener **filtros y ejemplos textuales** para que el analista pueda profundizar.

Si al tercer día el pipeline de procesamiento no está funcionando, **reduzcan alcance**: solo sentimiento \+ frustración \+ reglas simples de intents (keywords) ya dará valor.

¿Necesitas que profundice en alguna de estas áreas, o que redacte el plan de trabajo para asignar tareas por día?  
