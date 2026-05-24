"""
ConversaAI Dashboard — Data loading utilities.

Provides session-level and metrics data with Streamlit caching.
"""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from dashboard.config import DATA_PATH, METRICS_PATH


@st.cache_data(ttl=3600)
def load_session_data() -> pd.DataFrame:
    """Load and preprocess session-aggregated data."""
    df = pd.read_csv(DATA_PATH)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["max_frustracion"] = df["max_frustracion"].astype(int)
    df["any_churn"] = df["any_churn"].astype(int)
    df["any_resolved"] = df["any_resolved"].astype(int)
    return df


@st.cache_data(ttl=3600)
def load_metrics() -> dict:
    """Load aggregated pattern metrics from JSON."""
    with open(METRICS_PATH) as f:
        return json.load(f)  # type: ignore[no-any-return]
