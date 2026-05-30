> 📌 **Documentación inicial** — Este documento refleja el diseño o propuesta original del proyecto y puede no coincidir con la implementación final. Consultá `docs/data/data-dictionary.md` para la documentación vigente del dataset.

# **Informe de Especificación: Corpus V2 (ConversaAI)**

## **1. Resumen de la Entrega**

El **Corpus V2** es un dataset sintético bilingüe de **10,000
registros** diseñado para la detección de frustración y riesgo de
abandono (churn). Esta versión ha sido auditada para cerrar los \"gaps\"
de información detectados entre el modelo de IA y la visualización final
en el Dashboard.

- **Volumen:** 20,002 registros (3,334 sesiones de 3 mensajes cada una).

- **Alcance Temporal:** 6 meses de datos históricos (distribución
  aleatoria).

- **Regiones:** LATAM (Español) y BRAZIL (Portugués).

## **2. Resolución de Gaps Críticos (Post-Auditoría)**

Se han integrado metadatos de trazabilidad que permiten el
funcionamiento de los componentes de Figma:

  ---------------------------------------------------------------------------
  **Campo Nuevo**   **Relevancia para el        **Relevancia para IA
                    Dashboard**                 Engineer**
  ----------------- --------------------------- -----------------------------
  **flow_name**     Alimenta el ranking de      Contextualiza la intención en
                    flujos críticos.            un proceso de negocio.

  **turn_number**   Habilita el timeline de     Permite análisis de series
                    sentimiento por paso.       temporales por sesión.

  **resolved**      Calcula la tasa de          Etiqueta de éxito/fracaso de
                    resolución (KPI del 64%).   la interacción.

  **fecha (6        Permite visualizar          Provee diversidad temporal al
  meses)**          tendencias y                dataset.
                    estacionalidad.             
  ---------------------------------------------------------------------------

## 

## 

## 

## **3. Estructura de Datos (Data Schema)**

  ----------------------------------------------------------------------------
  **Columna**         **Descripción**                       **Ejemplo**
  ------------------- ------------------------------------- ------------------
  session_id          Identificador único de la             SESS-123456
                      conversación.                         

  turn_number         Posición del mensaje (1, 2 o 3).      1

  flow_name           Categoría superior (ej. Facturación). Facturación y
                                                            Cobros

  usuario             Handle anonimizado del cliente.       \@soyMarely99

  fecha               Marca temporal (Rango de 180 días).   2026-02-15
                                                            14:30:00

  intencion           Clasificación temática del mensaje.   problema_pago

  nivel_frustracion   Escala de sentimiento (0=Bajo,        2
                      1=Medio, 2=Alto).                     

  texto_espanol       Input para entrenamiento (Modelo      \"¡Esto es un
                      BETO).                                robo!\"

  texto_portugues     Input para entrenamiento (Modelo      \"Isto é um
                      BERTimbau).                           roubo!\"

  es_churn_risk       Alerta automática si                  1
                      nivel_frustracion = 2.                

  resolved            Indica si el caso se cerró            0
                      satisfactoriamente.                   
  ----------------------------------------------------------------------------

## 

## **4. Notas para el Equipo de IA**

- **Calidad de Etiquetas:** El campo nivel_frustracion puede utilizarse
  directamente como *Ground Truth* para el entrenamiento del
  clasificador de sentimiento.

- **Consistencia Bilingüe:** Cada entrada cuenta con su par bilingüe,
  ideal para pruebas de modelos *cross-lingual*.

- **Balance:** El dataset mantiene una proporción controlada de casos de
  éxito vs. frustración para evitar sesgos en el dashboard.

## **5. Validación de KPIs**

Para asegurar la integridad del dashboard, se han verificado los
siguientes indicadores en este dataset:

1.  **Tasa de Resolución:** \~64% (Consistente con el prototipo).

2.  **Riesgo de Abandono:** Identificado mediante la flag es_churn_risk.

3.  **Mapeo de Flujos:** 100% de las intenciones están vinculadas a un
    flow_name.
