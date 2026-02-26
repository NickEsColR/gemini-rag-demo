from gemini_client import client


def check_docs(store) -> list[str]:
    """Return the display names of all documents in the given file search store."""
    names: list[str] = []
    for document in client.file_search_stores.documents.list(
        parent=store.name if store.name else "no_name_found"
    ):
        names.append(document.display_name or "Unnamed document")
    return names
