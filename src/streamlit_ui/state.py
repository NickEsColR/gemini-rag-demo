"""Session state initialization and reset logic."""

import os

import streamlit as st
from google import genai

from manage_docs import cleanup_docs


def init_state() -> None:
    """Initialize session state with default values (idempotent)."""
    # API key & client — persisted across resets so users don't re-enter their key.
    # Pre-populate from the environment variable when available.
    _env_key: str = os.getenv("GEMINI_API_KEY") or ""
    st.session_state.setdefault("api_key", _env_key)
    st.session_state.setdefault(
        "gemini_client",
        genai.Client(api_key=_env_key) if _env_key else None,
    )

    st.session_state.setdefault("store", None)
    st.session_state.setdefault("indexed_names", [])
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("_last_chunk", None)
    st.session_state.setdefault("pending_files", {})  # {filename: UploadedFile}
    st.session_state.setdefault("file_uploader_key", 0)


def reset_session() -> None:
    """Clean up docs directory and reset all session state.

    API key and Gemini client are intentionally preserved so the user does
    not have to re-enter their key after a reset.
    """
    cleanup_docs()
    st.session_state.store = None
    st.session_state.indexed_names = []
    st.session_state.messages = []
    st.session_state.pop("_last_chunk", None)
    st.session_state.pending_files = {}
    st.session_state.file_uploader_key += 1
