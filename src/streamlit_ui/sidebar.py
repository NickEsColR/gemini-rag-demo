"""Sidebar UI component: document upload, indexed document list, and cleanup."""

import streamlit as st

from check_docs import check_docs
from upload_docs import upload_docs

from .helpers import EXTENSIONS, save_uploaded_files
from .state import reset_session


def render_sidebar() -> None:
    """Render the full sidebar: upload control, indexed doc list, and reset button."""
    with st.sidebar:
        st.title(":material/robot_2: Gemini RAG")
        st.caption(
            "Upload documents and ask questions grounded in your knowledge base."
        )
        st.divider()

        # ── Step 0: Document upload ──────────────────────────────────────────
        st.subheader("Upload documents")

        # Dynamic key lets us reset the widget after merging files so the
        # picker always returns to an empty state and duplicates never appear.
        new_files = st.file_uploader(
            "Select files",
            type=EXTENSIONS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key=f"uploader_{st.session_state.file_uploader_key}",
        )

        # Merge newly picked files into pending_files, skipping duplicates and
        # already-indexed documents, then reset the uploader widget.
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

        # Custom file list with per-file remove buttons
        pending = st.session_state.pending_files
        if pending:
            for name in list(pending.keys()):
                col_name, col_btn = st.columns([5, 1])
                with col_name:
                    size_kb = pending[name].size / 1024
                    st.markdown(
                        f"📄 **{name}**  \n"
                        f"<small style='color:gray'>{size_kb:.1f} KB</small>",
                        unsafe_allow_html=True,
                    )
                with col_btn:
                    if st.button("✕", key=f"remove_{name}", help=f"Remove {name}"):
                        del st.session_state.pending_files[name]
                        st.rerun()

        if st.button(
            "Upload & Index",
            icon=":material/cloud_upload:",
            type="primary",
            disabled=not pending,
            use_container_width=True,
        ):
            with st.status("Indexing documents…", expanded=True) as status:
                st.write("Saving files to staging area…")
                saved = save_uploaded_files(list(pending.values()))

                def _progress(filename: str) -> None:
                    st.write(f"✓ Indexed: **{filename}**")

                store = upload_docs(file_list=saved, on_progress=_progress)
                st.session_state.store = store
                st.session_state.indexed_names = check_docs(store)
                st.session_state.pending_files = {}
                status.update(
                    label="Indexing complete!", state="complete", expanded=False
                )

        st.divider()

        # ── Step 1: Indexed documents list ──────────────────────────────────
        st.subheader("Indexed documents")
        if st.session_state.store and st.session_state.indexed_names:
            for name in st.session_state.indexed_names:
                st.markdown(f"- {name}")
        else:
            st.caption("No documents indexed.")

        st.divider()

        # ── Cleanup button ───────────────────────────────────────────────────
        if st.button(
            "Cleanup & Reset",
            icon=":material/delete_sweep:",
            use_container_width=True,
            disabled=st.session_state.store is None,
        ):
            reset_session()
            st.rerun()
