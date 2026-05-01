import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-2.0-flash"

# ── Search / Scraping ────────────────────────────────────────────────────────
MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", 3))
MAX_CONTENT_CHARS: int = int(os.getenv("MAX_CONTENT_CHARS", 4000))
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 10))

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR: str = os.getenv("LOG_DIR", "logs")
