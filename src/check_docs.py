from gemini_client import client
from upload_docs import file_search_store


def check_docs():
    for document in client.file_search_stores.documents.list(
        parent=file_search_store.name if file_search_store.name else "no_name_found"
    ):
        print(document.display_name)
