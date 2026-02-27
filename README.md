# Gemini RAG Demo

A minimal, production-ready demonstration of **Retrieval-Augmented Generation (RAG)** built with the Google Gemini API. This project showcases how to upload documents to a Gemini File Search Store, ground model responses against that knowledge base, and extract verifiable citations from every answer.

It ships with a **Streamlit web UI** as the primary interface, plus a CLI pipeline for scripted or automated use. Both support dynamic document uploads, streaming responses, and citation extraction.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Large Language Models can hallucinate facts when answering questions outside their training data. RAG solves this by **retrieving relevant context from a trusted knowledge base** at inference time and feeding it to the model alongside the user query.

This demo uses the **Gemini File Search** tool — a native capability of the `google-genai` SDK — to:

1. Index local documents into a managed vector store.
2. Retrieve the most relevant chunks automatically when a query is issued.
3. Generate a grounded, citation-backed response using `gemini-2.5-flash-lite`.

---

## Features

| Capability | Details |
| --- | --- |
| Document ingestion | Uploads files to a Gemini File Search Store; supports PDF, TXT, HTML, CSV, MD, XML |
| Grounded generation | Responses are anchored to indexed documents via the `FileSearch` tool |
| Streaming responses | Output is streamed token-by-token via `generate_content_stream` for real-time display |
| Citation extraction | Source titles are extracted from `grounding_metadata` and displayed in expandable panels |
| Streamlit UI | Multi-component web interface: API key input, sidebar with pending file queue + per-file remove, grounded chat with persistent message history, and session reset |
| API key management | API key can be entered and validated directly in the Streamlit sidebar; no `.env` file required for the UI |
| Per-session client | Each Streamlit session uses its own validated `genai.Client`; the module-level singleton is only used by the CLI |
| Pending file queue | Files can be staged before upload; duplicates and already-indexed files are filtered automatically |
| Session management | Full session state lifecycle — initialize, persist across reruns, and reset with cleanup; API key is preserved across resets |
| Error handling | Streaming errors and indexing failures are caught and surfaced in the UI without crashing the session |
| CLI pipeline | `main.py` orchestrates upload → check → generate → cite in sequence |
| Minimal dependencies | Only `google-genai`, `python-dotenv`, and `streamlit` required |
| Fast setup | Single `uv sync` command to install all dependencies |

---

The pipeline is fully orchestrated in `main.py` through four sequential steps:

1. **Upload** — documents are uploaded and indexed.
2. **Check** — indexed document names are listed to confirm ingestion.
3. **Generate** — a grounded response is streamed token-by-token for the user's prompt.
4. **Cite** — source titles are extracted from the final chunk's grounding metadata and displayed.

---

## Prerequisites

| Requirement | Version |
| --- | --- |
| Python | >= 3.10 |
| [uv](https://docs.astral.sh/uv/) | latest |
| Google Gemini API key | — |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/NickEsColR/gemini-rag-demo.git
cd gemini-rag-demo
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables (optional for the UI)

For the **CLI pipeline**, create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

For the **Streamlit UI**, you can skip this step and enter your API key directly in the sidebar at runtime.

> You can obtain a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Add your documents

Place any text or PDF files you want to index inside the `docs/` directory.

### 5. Run the pipeline

**Streamlit UI (recommended):**

```bash
uv run streamlit run src/streamlit_ui/streamlit_app.py
```

This opens a browser with the full web interface:

- **Sidebar** — enter and validate your Gemini API key, stage files in a pending queue (with per-file remove), upload & index them, view the indexed document list, and reset the session.
- **Main area** — grounded chat interface with streamed responses, persistent message history, expandable citation panels per reply, and inline error messages when generation or indexing fails.

**CLI pipeline:**

```bash
uv run python src/main.py
```

---

## Project Structure

```bash
gemini-rag-demo/
├── docs/                        # Knowledge base documents (gitignored by default)
├── src/
│   ├── streamlit_ui/            # Streamlit web UI package
│   │   ├── streamlit_app.py     # UI orchestrator (entry point)
│   │   ├── sidebar.py           # Sidebar component (API key, upload, doc list, cleanup)
│   │   ├── chat.py              # Chat area component (messages, streaming, citations, error handling)
│   │   ├── helpers.py           # Utility functions and computed config
│   │   └── state.py             # Session state management (API key & client persisted across resets)
│   ├── main.py                  # CLI pipeline orchestrator
│   ├── configs.py               # Shared configuration constants
│   ├── gemini_client.py         # Gemini SDK client — module-level singleton (CLI) + create_client() (UI)
│   ├── upload_docs.py           # Document ingestion into File Search Store
│   ├── check_docs.py            # Lists indexed documents
│   ├── query_docs.py            # Grounded generation with FileSearch tool
│   └── citate_docs.py           # Citation extraction from grounding metadata
├── pyproject.toml               # Project metadata and dependencies
├── uv.lock                      # Locked dependency versions
└── .env                         # Environment variables (not committed)
```

---

## Configuration

All tuneable constants are centralised in [src/configs.py](src/configs.py):

| Variable | Default | Description |
| --- | --- | --- |
| `FILE_SEARCH_STORE_NAME` | `"rag-demo"` | Display name for the File Search Store |
| `MODEL` | `"gemini-2.5-flash-lite"` | Gemini model used for generation |
| `TEST_PROMPT` | `"En una frase, cuales son las etapas del roadmap"` | Default prompt used by the CLI pipeline |
| `DOCS_DIR` | `"./docs/"` | Staging directory for documents before upload |
| `SUPPORTED_FILETYPES` | PDF, TXT, HTML, CSV, MD, XML | File types accepted in the upload dialog and Streamlit picker |

---

## License

This project is open-source and available under the [MIT License](LICENSE).
