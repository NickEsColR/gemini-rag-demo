"""Utility functions and computed configuration for the Streamlit UI."""

import os
from typing import Generator

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from google.genai.types import FileSearchStore

from configs import DOCS_DIR, SUPPORTED_FILETYPES
from query_docs import generate_response

# ── Supported extensions for Streamlit's file_uploader ─────────────────────
EXTENSIONS: list[str] = [
    ext.lstrip("*.")
    for label, pattern in SUPPORTED_FILETYPES
    if label != "All files"
    for ext in pattern.split()
]


def save_uploaded_files(uploaded_files: list[UploadedFile]) -> list[str]:
    """Write Streamlit UploadedFile objects to DOCS_DIR and return basenames."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    saved: list[str] = []
    for uf in uploaded_files:
        dest = os.path.join(DOCS_DIR, uf.name)
        with open(dest, "wb") as f:
            f.write(uf.read())
        saved.append(uf.name)
    return saved


def streaming_wrapper(
    prompt: str, store: FileSearchStore
) -> Generator[str, None, None]:
    """
    Wrap generate_response so st.write_stream receives plain strings
    while we capture the final raw chunk for citation extraction.
    """
    last = None
    for chunk in generate_response(prompt, store):
        last = chunk
        if chunk.text:
            yield chunk.text

    # Store the last chunk so citations can be extracted after streaming ends
    st.session_state["_last_chunk"] = last
