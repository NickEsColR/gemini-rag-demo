"""
Streamlit UI for Gemini RAG Demo — Orchestrator.

Wires together page configuration, session state, sidebar, and chat components.

Run from the project root:
  uv run streamlit run src/streamlit_ui/streamlit_app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Ensure src/ is on the path so backend modules and the streamlit_ui package resolve
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_ui.chat import render_chat  # noqa: E402
from streamlit_ui.sidebar import render_sidebar  # noqa: E402
from streamlit_ui.state import init_state  # noqa: E402

# ── Page config (must be the first Streamlit call) ───────────────────────────
st.set_page_config(
    page_title="Gemini RAG Demo",
    page_icon=":material/robot_2:",
    layout="centered",
)

# ── Initialize session state defaults ────────────────────────────────────────
init_state()

# ── Render UI components ──────────────────────────────────────────────────────
render_sidebar()
render_chat()
