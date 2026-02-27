import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

_env_key = os.getenv("GEMINI_API_KEY")

# Module-level singleton used by the CLI workflow.
# Will be None when GEMINI_API_KEY is not set; the Streamlit app
# creates its own per-session client via create_client().
client: genai.Client | None = genai.Client(api_key=_env_key) if _env_key else None


def create_client(api_key: str) -> genai.Client:
    """Create and return a new Gemini client for the given API key."""
    return genai.Client(api_key=api_key)
