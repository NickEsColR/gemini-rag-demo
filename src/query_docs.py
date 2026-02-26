from google.genai import types
from google.genai.types import GenerateContentResponse

from gemini_client import client
from configs import MODEL
from upload_docs import file_search_store


def generate_response(prompt) -> GenerateContentResponse:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[file_search_store.name]
                        if file_search_store.name
                        else []
                    )
                )
            ],
            system_instruction="Based your responses on the provided documents. If the answer is not in the documents, say it's not in the knowledge base.",
        ),
    )

    return response
