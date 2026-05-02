import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-2.0-flash"

# ── Groq (OpenAI-compatible) ─────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "llama-3.3-70b-versatile"

# ── OpenAI ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ── Anthropic (Claude) ────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")

# ── Search / Scraping ────────────────────────────────────────────────────────
MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", 3))
MAX_CONTENT_CHARS: int = int(os.getenv("MAX_CONTENT_CHARS", 4000))
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 10))

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR: str = os.getenv("LOG_DIR", "logs")
