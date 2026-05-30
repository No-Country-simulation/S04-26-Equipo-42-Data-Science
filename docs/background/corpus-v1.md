> 📌 **Documentación inicial** — Este documento refleja el diseño o propuesta original del proyecto y puede no coincidir con la implementación final. Consultá `docs/data/data-dictionary.md` para la documentación vigente del dataset.

# **Documentación del Dataset: ConversaAI Corpus v1.0**

## **1. Resumen Ejecutivo**

Este dataset contiene **10,000 registros sintéticos** diseñados para
simular interacciones bilingües (Español/Portugués) en canales de
soporte al cliente. La estructura está optimizada para alimentar el
**Dashboard de ConversaAI**, permitiendo la visualización de métricas de
frustración, riesgo de abandono (churn) y análisis regional.

- **Formato:** CSV

- **Codificación:** UTF-8-sig (Compatible con Excel y Python)

- **Metodología:** Generación basada en agentes con escalada de
  frustración lineal.

## **2. Diccionario de Datos (Schema)**

  -------------------------------------------------------------------------------
  **Columna**         **Tipo de  **Descripción**                **Ejemplo**
                      Dato**                                    
  ------------------- ---------- ------------------------------ -----------------
  session_id          String     Identificador único de la      SESS-45210
                                 sesión de chat.                

  usuario             String     Handle del usuario             \@soyKitty_ai
                                 (anonimizado/sintético).       

  fecha               DateTime   Marca temporal del mensaje     2026-05-01
                                 (YYYY-MM-DD HH:MM:SS).         09:15:00

  region              Enum       Mercado de origen del usuario  BRAZIL
                                 (LATAM, BRAZIL, EUROPE).       

  intencion           String     Categoría temática del         logistica_envio
                                 problema detectado.            

  nivel_frustracion   Integer    Grado de insatisfacción (0 =   2
                                 Bajo, 1 = Medio, 2 = Alto).    

  texto_espanol       String     Cuerpo del mensaje en español. \"¡Es un robo!\"

  texto_portugues     String     Traducción/Equivalente         \"Isto é um
                                 semántico en portugués.        roubo!\"

  es_churn_risk       Boolean    Flag que indica riesgo         1
                      (0/1)      inminente de abandono del      
                                 cliente.                       
  -------------------------------------------------------------------------------

## **3. Lógica de Negocio y Métricas**

### **A. Escala de Frustración**

Para que el Dashboard funcione correctamente, se ha implementado una
lógica de **trayectoria de usuario**:

1.  **Nivel 0 (Neutral):** Consultas informativas o reportes iniciales.

2.  **Nivel 1 (Frustrado):** Reclamos por falta de respuesta o
    repetición del problema.

3.  **Nivel 2 (Crítico):** Lenguaje agresivo, uso de mayúsculas o
    amenazas de cancelación.

### **B. Cálculo de Churn Risk**

El campo es_churn_risk se activa automáticamente cuando el
nivel_frustracion llega a **2**. Esta métrica es fundamental para el KPI
de **\"Alerta de Clientes en Riesgo\"** definido en los requerimientos
del Dashboard.

## **4. Distribución Estadística (Balance de Carga)**

El dataset ha sido generado siguiendo una distribución controlada para
asegurar la utilidad en el entrenamiento de modelos de Machine Learning:

- **Distribución por Nivel:**

  - Nivel 0: 33.3%

  - Nivel 1: 33.3%

  - Nivel 2: 33.3%

- **Balance Regional:** Aleatorio equitativo entre LATAM, BRAZIL y
  EUROPE.

- **Consistencia Bilingüe:** 100% de los registros cuentan con su par
  traducido para validación de modelos cross-lingual.

## **5. Instrucciones de Uso para el Equipo**

1.  **Analistas de Datos:** Utilizar la columna region y fecha para
    crear series de tiempo sobre la evolución del sentimiento por
    mercado.

2.  **Ingenieros de IA:** El campo nivel_frustracion debe utilizarse
    como *Label* (etiqueta) para el entrenamiento de clasificadores de
    texto.

3.  **Visualizadores (Dashboard):** Filtrar por es_churn_risk = 1 para
    poblar el componente de \"Casos de Atención Prioritaria\".
