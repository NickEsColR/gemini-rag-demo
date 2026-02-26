import os
import time

from configs import FILE_SEARCH_STORE_NAME
from gemini_client import client


files = os.listdir("docs")
DOCS_PATH = "./docs/"

file_search_store = client.file_search_stores.create(
    config={
        "display_name": FILE_SEARCH_STORE_NAME,
    }
)
print(f"Created file search store with name: {file_search_store.name}")


def upload_docs():
    for file in files:
        operation = client.file_search_stores.upload_to_file_search_store(
            file=os.path.join(DOCS_PATH, file),
            file_search_store_name=file_search_store.name
            if file_search_store.name
            else "no_name_found",
            config={
                "display_name": file,
            },
        )

        while not operation.done:
            time.sleep(2)
            operation = client.operations.get(operation)

        print(f"Finished uploading file: {file}")
