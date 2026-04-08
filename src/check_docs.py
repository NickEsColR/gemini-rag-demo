from gemini_client import client as _default_client


def check_docs(store, client=None) -> list[str]:
    """Return the display names of all documents in the given file search store.

    Args:
        store: The file search store to list documents from.
        client: Optional Gemini client. Defaults to the module-level singleton
                (used by the CLI). Pass a per-session client from the Streamlit app.
    """
    _client = client if client is not None else _default_client
    if _client is None:
        raise ValueError(
            "No Gemini client available. Set the GEMINI_API_KEY environment variable."
        )
    names: list[str] = []
    for document in _client.file_search_stores.documents.list(
        parent=store.name if store.name else "no_name_found"
    ):
        names.append(document.display_name or "Unnamed document")
    return names
