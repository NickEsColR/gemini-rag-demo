"""Session state initialization and reset logic."""

import streamlit as st

from manage_docs import cleanup_docs


def init_state() -> None:
    """Initialize session state with default values (idempotent)."""
    st.session_state.setdefault("store", None)
    st.session_state.setdefault("indexed_names", [])
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("_last_chunk", None)
    st.session_state.setdefault("pending_files", {})  # {filename: UploadedFile}
    st.session_state.setdefault("file_uploader_key", 0)


def reset_session() -> None:
    """Clean up docs directory and reset all session state."""
    cleanup_docs()
    st.session_state.store = None
    st.session_state.indexed_names = []
    st.session_state.messages = []
    st.session_state.pop("_last_chunk", None)
    st.session_state.pending_files = {}
    st.session_state.file_uploader_key += 1
