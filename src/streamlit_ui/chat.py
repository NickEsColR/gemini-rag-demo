"""Main area chat UI component: message history, suggestion chips, streaming, and citations."""

import streamlit as st

from citate_docs import cite_documents

from .helpers import streaming_wrapper


def _render_header() -> None:
    """Render the page title and caption."""
    st.title("Gemini RAG Demo")
    st.caption(
        "Retrieval-Augmented Generation powered by [Gemini File Search](https://ai.google.dev/)."
    )


def _render_message_history() -> None:
    """Render all previous messages with their associated citations."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("citations"):
                with st.expander(":material/format_quote: Citations"):
                    st.markdown(msg["citations"])


def _handle_query_input() -> None:
    """Accept a new user query, stream the response, and attach citations."""
    if not (user_prompt := st.chat_input("Ask about your documents…")):
        return

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            response_text = st.write_stream(
                streaming_wrapper(user_prompt, st.session_state.store)
            )
        except Exception as e:
            error_msg = f"An error occurred while generating a response: {e}"
            st.error(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg, "citations": ""}
            )
            return

    last_chunk = st.session_state.pop("_last_chunk", None)
    candidate = (
        last_chunk.candidates[0] if last_chunk and last_chunk.candidates else None
    )
    citations = cite_documents(candidate)

    with st.chat_message("assistant"):
        with st.expander(":material/format_quote: Citations"):
            st.markdown(citations)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text,
            "citations": citations,
        }
    )


def render_chat() -> None:
    """Render the main chat area: header, message history, suggestions, and query input."""
    _render_header()

    if not st.session_state.get("gemini_client"):
        st.info(
            ":material/key: Enter a valid API key in the sidebar to get started.",
            icon=None,
        )
        return

    if not st.session_state.store:
        st.info(
            ":material/upload_file: Upload and index your documents using the sidebar to get started.",
            icon=None,
        )
        return

    _render_message_history()
    _handle_query_input()
