"""Sidebar UI component: API key input, document upload, indexed doc list, and cleanup."""

import streamlit as st

from check_docs import check_docs
from gemini_client import create_client
from upload_docs import upload_docs

from .helpers import EXTENSIONS, save_uploaded_files
from .state import reset_session


# ── API Key ──────────────────────────────────────────────────────────────────


def _render_api_key_section() -> None:
    """Render the API key input and validation controls."""
    st.subheader(":material/key: API Key")

    entered_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="Paste your Gemini API key…",
        label_visibility="collapsed",
    )

    if st.button(
        "Apply",
        icon=":material/check:",
        use_container_width=True,
        type="primary" if not st.session_state.gemini_client else "secondary",
    ):
        if not entered_key or not entered_key.strip():
            st.error("Please enter an API key.")
        else:
            with st.spinner("Validating API key…"):
                try:
                    test_client = create_client(entered_key.strip())
                    # Lightweight call to confirm the key is valid.
                    next(iter(test_client.models.list()))
                    st.session_state.api_key = entered_key.strip()
                    st.session_state.gemini_client = test_client
                    st.success("API key validated!", icon=":material/check_circle:")
                except Exception as e:
                    st.session_state.api_key = ""
                    st.session_state.gemini_client = None
                    st.error(f"Invalid API key: {e}")

    if st.session_state.gemini_client:
        st.caption(":material/check_circle: API key is active")
    else:
        st.caption(":material/info: Enter a valid API key to get started.")


# ── File picker ───────────────────────────────────────────────────────────────


def _render_file_picker() -> None:
    """Render the file uploader and merge new picks into pending_files.

    Uses a dynamic widget key so the picker resets to an empty state after
    each batch, preventing the same file from appearing twice.
    """
    new_files = st.file_uploader(
        "Select files",
        type=EXTENSIONS,
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.file_uploader_key}",
    )

    if new_files:
        already_indexed = set(st.session_state.indexed_names)
        for f in new_files:
            if (
                f.name not in st.session_state.pending_files
                and f.name not in already_indexed
            ):
                st.session_state.pending_files[f.name] = f
        st.session_state.file_uploader_key += 1
        st.rerun()


# ── Pending files list ────────────────────────────────────────────────────────


def _render_pending_files() -> None:
    """Render the staged file list with per-file remove buttons."""
    pending = st.session_state.pending_files
    if not pending:
        return

    for name in list(pending.keys()):
        col_name, col_btn = st.columns([5, 1])
        with col_name:
            size_kb = pending[name].size / 1024
            st.markdown(
                f"📄 **{name}**  \n<small style='color:gray'>{size_kb:.1f} KB</small>",
                unsafe_allow_html=True,
            )
        with col_btn:
            if st.button("✕", key=f"remove_{name}", help=f"Remove {name}"):
                del st.session_state.pending_files[name]
                st.rerun()


# ── Upload & index button ─────────────────────────────────────────────────────


def _render_upload_button() -> None:
    """Render the Upload & Index button and run the indexing pipeline."""
    pending = st.session_state.pending_files

    if st.button(
        "Upload & Index",
        icon=":material/cloud_upload:",
        type="primary",
        disabled=not pending,
        use_container_width=True,
    ):
        with st.status("Indexing documents…", expanded=True) as status:
            try:
                st.write("Saving files to staging area…")
                saved = save_uploaded_files(list(pending.values()))

                def _progress(filename: str) -> None:
                    st.write(f"✓ Indexed: **{filename}**")

                store = upload_docs(
                    file_list=saved,
                    on_progress=_progress,
                    client=st.session_state.gemini_client,
                )
                st.session_state.store = store
                st.session_state.indexed_names = check_docs(
                    store, client=st.session_state.gemini_client
                )
                st.session_state.pending_files = {}
                status.update(
                    label="Indexing complete!", state="complete", expanded=False
                )
            except Exception as e:
                status.update(label="Indexing failed.", state="error", expanded=True)
                st.error(f"Error during indexing: {e}")


# ── Upload section (composed) ─────────────────────────────────────────────────


def _render_upload_section() -> None:
    """Render the full document upload section: picker, staged list, and action button."""
    st.subheader("Upload documents")
    _render_file_picker()
    _render_pending_files()
    _render_upload_button()


# ── Indexed documents list ────────────────────────────────────────────────────


def _render_indexed_docs_section() -> None:
    """Render the list of already-indexed documents."""
    st.subheader("Indexed documents")
    if st.session_state.store and st.session_state.indexed_names:
        for name in st.session_state.indexed_names:
            st.markdown(f"- {name}")
    else:
        st.caption("No documents indexed.")


# ── Cleanup ───────────────────────────────────────────────────────────────────


def _render_cleanup_section() -> None:
    """Render the Cleanup & Reset button."""
    if st.button(
        "Cleanup & Reset",
        icon=":material/delete_sweep:",
        use_container_width=True,
        disabled=st.session_state.store is None,
    ):
        reset_session()
        st.rerun()


# ── Public entry point ────────────────────────────────────────────────────────


def render_sidebar() -> None:
    """Render the full sidebar, composing all section components."""
    with st.sidebar:
        st.title(":material/robot_2: Gemini RAG")
        st.caption(
            "Upload documents and ask questions grounded in your knowledge base."
        )
        st.divider()

        _render_api_key_section()
        st.divider()

        if not st.session_state.gemini_client:
            st.warning(
                "Enter a valid API key above to upload and index documents.",
                icon=":material/lock:",
            )
            return

        _render_upload_section()
        st.divider()

        _render_indexed_docs_section()
        st.divider()

        _render_cleanup_section()
