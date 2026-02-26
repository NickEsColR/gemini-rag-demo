import os
import time
from collections.abc import Callable

from google.genai.types import FileSearchStore

from configs import DOCS_DIR, FILE_SEARCH_STORE_NAME
from gemini_client import client

if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR, exist_ok=True)
    print(f"Created docs directory: {DOCS_DIR}")


def create_store() -> FileSearchStore:
    """Create a new Gemini file search store and return it."""
    store = client.file_search_stores.create(
        config={"display_name": FILE_SEARCH_STORE_NAME}
    )
    print(f"Created file search store: {store.name}")
    return store


def upload_docs(
    file_list: list[str] | None = None,
    on_progress: Callable[[str], None] | None = None,
) -> FileSearchStore:
    """
    Create a file search store, upload documents to it, and return the store.

    Args:
        file_list:  Explicit list of filenames (basenames) to upload from
                    DOCS_DIR. If None, all non-hidden files in DOCS_DIR are used.
        on_progress: Optional callback called with each filename after it finishes
                    uploading. Defaults to printing the filename.
    """
    store = create_store()

    if file_list is None:
        file_list = [f for f in os.listdir(DOCS_DIR) if not f.startswith(".")]

    for filename in file_list:
        operation = client.file_search_stores.upload_to_file_search_store(
            file=os.path.join(DOCS_DIR, filename),
            file_search_store_name=store.name if store.name else "no_name_found",
            config={"display_name": filename},
        )

        while not operation.done:
            time.sleep(2)
            operation = client.operations.get(operation)

        if on_progress:
            on_progress(filename)
        else:
            print(f"Finished uploading: {filename}")

    return store
