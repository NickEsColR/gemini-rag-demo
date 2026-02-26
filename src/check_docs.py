from gemini_client import client


def check_docs(store) -> None:
    """Print the display names of all documents in the given file search store."""
    for document in client.file_search_stores.documents.list(
        parent=store.name if store.name else "no_name_found"
    ):
        print(document.display_name)
