from google.genai.types import Candidate


def cite_documents(candidate: Candidate | None) -> str:
    if not candidate:
        return "No candidates available."

    citations = []
    grounding_metadata = candidate.grounding_metadata
    if grounding_metadata and grounding_metadata.grounding_chunks:
        for chunk in grounding_metadata.grounding_chunks:
            if chunk.retrieved_context:
                citations.append(chunk.retrieved_context.title)

    if not citations:
        return "No citations found in the candidates."

    return "\n".join(f"- {citation}" for citation in citations)
