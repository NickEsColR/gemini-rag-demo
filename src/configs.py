FILE_SEARCH_STORE_NAME = "rag-demo"
MODEL = "gemini-3-flash-preview"
TEST_PROMPT = "En una frase, cuales son las etapas del roadmap"

DOCS_DIR = "./docs/"

# Gemini File Search supported formats
SUPPORTED_FILETYPES = [
    ("Supported files", "*.pdf *.txt *.html *.htm *.csv *.md *.xml"),
    ("All files", "*.*"),
]
