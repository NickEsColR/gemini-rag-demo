from typing import Iterator

from google.genai import types
from google.genai.types import GenerateContentResponse, FileSearchStore

from gemini_client import client
from configs import MODEL

has_thinking_level: bool = "3" in MODEL  # Thinking levels only supported in Gemini 3+


def generate_response(
    prompt: str, store: FileSearchStore
) -> Iterator[GenerateContentResponse]:
    """Stream a response grounded in the documents of the given file search store."""
    return client.models.generate_content_stream(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[store.name] if store.name else []
                    )
                )
            ],
            system_instruction="Based your responses on the provided documents. If the answer is not in the documents, say it's not in the knowledge base.",
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.MINIMAL
                if has_thinking_level
                else None,
            ),
        ),
    )
