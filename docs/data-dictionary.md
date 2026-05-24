# Data Dictionary — ConversaAI

**Version:** 1.0  
**Fuente:** `data_engineering/data/processed/data_preprocessed.csv`  
**Filas:** 20,001 | **Columnas:** 15 | **Valores nulos:** 0

---

## Columnas

### Identificadores y Metadatos

| Columna | Tipo | Descripcion | Dominio | Uso en modelo |
|---------|------|-------------|---------|---------------|
| `session_id` | string | Identificador unico de la conversacion | `SESS-XXXXXX` (6,648 sesiones unicas) | Agrupacion, feature engineering |
| `turn_number` | entero | Numero de turno dentro de la sesion | 1, 2, 3 | Feature (secuencia) |
| `usuario` | string | Usuario/agente que atiende | `@usuario` (~300 usuarios) | Feature (rendimiento por agente) |
| `fecha` | datetime | Timestamp del mensaje | 2025-11-08 a 2026-05-07 | Feature temporal |

### Texto

| Columna | Tipo | Descripcion | Dominio | Uso en modelo |
|---------|------|-------------|---------|---------------|
| `texto_espanol` | string | Texto original en espanol | Texto libre | Input principal (modelo ES) |
| `texto_portugues` | string | Traduccion al portugues | Texto libre | Input alternativo (modelo PT) |
| `texto_original` | string | Texto original (sin identificar idioma) | Texto libre | Deprecated? |
| `texto_clean` | string | Texto normalizado: minusculas, sin acentos ni puntuacion | Texto limpio | Input del modelo NLP |
| `texto_vacio` | booleano | Flag de texto vacio tras limpieza | `True` / `False` | Control de calidad |

### Negocio y Clasificacion

| Columna | Tipo | Descripcion | Dominio | Uso en modelo |
|---------|------|-------------|---------|---------------|
| `flow_name` | categorico | Flujo de soporte al que pertenece | `Acceso y Seguridad`, `Gestion de Cuenta`, `Soporte Tecnico y Despacho`, `Facturacion y Cobros` | Feature, segmentacion |
| `intencion` | categorico | Intencion del usuario en el turno | `error_login`, `cambio_plan`, `logistica_envio`, `problema_pago` | **TARGET** (clasificacion multiclase) |
| `nivel_frustracion` | entero | Nivel de frustracion del usuario | 0 (baja), 1 (media), 2 (alta) | **TARGET** (clasificacion ordinal) |
| `es_churn_risk` | booleano | Riesgo de abandono/churn | 0 / 1 | **TARGET** (clasificacion binaria) |
| `resolved` | booleano | Indica si el problema fue resuelto | 0 / 1 | **TARGET** (clasificacion binaria), outcome |
| `idioma` | categorico | Idioma detectado del texto | `es` (100% de los casos) | Segmentacion |

---

## Estadisticas Clave

| Metrica | Valor |
|---------|-------|
| Sesiones unicas | 6,648 |
| Turnos promedio por sesion | ~3 |
| Distribucion frustracion | 0: 10,970 (54.8%) / 1: 6,667 (33.3%) / 2: 2,364 (11.8%) |
| Distribucion intencion | balanceada (~5,000 cada una) |
| Tasa de resolucion (resolved=1) | 21.5% |
| Tasa de churn (es_churn_risk=1) | 11.8% |
| Idioma predominante | Espanol (100%) |
| Rango temporal | Nov 2025 - May 2026 (~6 meses) |

---

## Relaciones y Dependencias

- Cada `session_id` tiene 1 a 3 `turn_number`
- `nivel_frustracion=2` y `es_churn_risk=1` tienen exactamente la misma cantidad de registros (2,364) — probablemente indica que frustracion alta = churn risk
- `flow_name` mapea 1:1 con `intencion`:
  - `Acceso y Seguridad` → `error_login`
  - `Gestion de Cuenta` → `cambio_plan`
  - `Soporte Técnico y Despacho` → `logistica_envio`
  - `Facturación y Cobros` → `problema_pago`

---

## Notas

- Dataset sintetico / preprocesado — sin nulos, sin valores fuera de rango
- `texto_vacio` es `False` en todos los registros (texto limpiado correctamente)
- La columna `texto_clean` ya esta normalizada (minusculas, sin acentos, sin puntuacion)
