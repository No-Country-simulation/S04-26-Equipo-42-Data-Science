"""
ConversaAI Dashboard — Configuration constants.

Paths, color palette, labels, and shared text.
"""

from pathlib import Path

import plotly.express as px

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "reports" / "session_aggregated.csv"
METRICS_PATH = BASE_DIR / "reports" / "pattern_metrics.json"

# ---------------------------------------------------------------------------
# Copy / dataset notice
# ---------------------------------------------------------------------------
SYNTHETIC_NOTE = (
    "**Nota:** Este dataset es sintetico/determinista. "
    "Los patrones mostrados reflejan reglas de construccion, "
    "no comportamiento real de usuarios. Con datos reales, "
    "las correlaciones seran mas debiles y variables."
)

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
COLORS = {
    "Resuelto": "#2ecc71",
    "Churn": "#e74c3c",
    "Activo": "#f39c12",
    "flow": list(px.colors.qualitative.Set2[:4]),
    "frust": ["#27ae60", "#f1c40f", "#e74c3c"],
}

FRUST_LABELS = {0: "Baja (0)", 1: "Media (1)", 2: "Alta (2)"}
