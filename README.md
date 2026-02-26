# Gemini RAG Demo

A minimal, production-ready demonstration of **Retrieval-Augmented Generation (RAG)** built with the Google Gemini API. This project showcases how to upload documents to a Gemini File Search Store, ground model responses against that knowledge base, and extract verifiable citations from every answer.

This version runs on CLI, requires to manually upload documents to the `docs/` folder, and uses a hardcoded prompt for testing.

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
3. Generate a grounded, citation-backed response using `gemini-3-flash-preview`.

---

## Features

| Capability | Details |
| --- | --- |
| Document ingestion | Uploads all files in `docs/` to a Gemini File Search Store |
| Grounded generation | Responses are anchored to indexed documents via the `FileSearch` tool |
| Citation extraction | Retrieves source titles from `grounding_metadata` for transparency |
| Minimal dependencies | Only `google-genai` and `python-dotenv` required |
| Fast setup | Single `uv sync` command to install all dependencies |

---

The pipeline is fully orchestrated in `main.py` through four sequential steps:

1. **Upload** — documents are uploaded and indexed.
2. **Check** — indexed document names are listed to confirm ingestion.
3. **Generate** — a grounded response is produced for the configured prompt.
4. **Cite** — source titles are extracted and displayed.

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

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> You can obtain a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Add your documents

Place any text or PDF files you want to index inside the `docs/` directory.

### 5. Run the pipeline

```bash
uv run python src/main.py
```

---

## Project Structure

```bash
gemini-rag-demo/
├── docs/                  # Knowledge base documents (gitignored by default)
├── src/
│   ├── main.py            # Pipeline orchestrator
│   ├── configs.py         # Shared configuration constants
│   ├── gemini_client.py   # Gemini SDK client initialisation
│   ├── upload_docs.py     # Document ingestion into File Search Store
│   ├── check_docs.py      # Lists indexed documents
│   ├── query_docs.py      # Grounded generation with FileSearch tool
│   └── citate_docs.py     # Citation extraction from grounding metadata
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependency versions
└── .env                   # Environment variables (not committed)
```

---

## Configuration

All tuneable constants are centralised in [src/configs.py](src/configs.py):

| Variable | Default | Description |
| --- | --- | --- |
| `FILE_SEARCH_STORE_NAME` | `"rag-demo"` | Display name for the File Search Store |
| `MODEL` | `"gemini-3-flash-preview"` | Gemini model used for generation |
| `TEST_PROMPT` | `"Test prompt"` | Default prompt when none is entered |
| `DOCS_DIR` | `"./docs/"` | Staging directory for documents before upload |
| `SUPPORTED_FILETYPES` | PDF, TXT, HTML, CSV, MD, XML | File types shown in the native picker dialog |

---

## Roadmap

Planned improvements aligned with the senior AI Engineer path:

- [X] Add streaming responses via Server-Sent Events (SSE)
- [X] Allow dynamic user input for queries instead of hardcoded prompt
- [X] Allow dynamic document uploads through the CLI instead of manual `docs/` folder
- [ ] Add UI interface for document upload and query input

---

## License

This project is open-source and available under the [MIT License](LICENSE).
