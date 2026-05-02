import json
import logging
import time
from google import genai
from google.genai import types
from config import (
    GEMINI_API_KEY, GEMINI_MODEL,
    GROQ_API_KEY, GROQ_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
)

logger = logging.getLogger(__name__)


# ── Provider-specific callers ─────────────────────────────────────────────────

def _call_groq(prompt: str, system: str) -> dict:
    """Calls Groq (OpenAI-compatible) and returns parsed JSON."""
    import groq
    client = groq.Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Groq returned empty content.")
    return json.loads(content)


def _call_openai(prompt: str, system: str) -> dict:
    """Calls OpenAI and returns parsed JSON."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned empty content.")
    return json.loads(content)


def _call_anthropic(prompt: str, system: str) -> dict:
    """Calls Anthropic (Claude) and returns parsed JSON."""
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    content = message.content[0].text
    if not content:
        raise ValueError("Anthropic returned empty content.")
    # Claude does not have native JSON mode — strip markdown fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content.strip())


def _call_gemini(prompt: str, system: str, max_retries: int = 4) -> dict:
    """Calls Gemini with retry logic for rate limits and returns parsed JSON."""
    if not GEMINI_API_KEY or "AIzaSy..." in GEMINI_API_KEY:
        raise ValueError("No valid GEMINI_API_KEY found. Check your .env file.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    base_delay = 60

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0,
                    system_instruction=system,
                ),
            )
            content = response.text
            if not content:
                raise ValueError("Gemini returned empty content.")
            return json.loads(content)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini: {e}\nContent was: {content}")
            raise
        except Exception as e:
            error_str = str(e)
            if ("429" in error_str or "RESOURCE_EXHAUSTED" in error_str) and attempt < max_retries - 1:
                logger.warning(f"Rate limit hit (429). Retrying in {base_delay}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(base_delay)
                base_delay += 10
                continue
            raise

    raise RuntimeError("Max retries exceeded due to Gemini rate limiting.")


# ── Provider router ───────────────────────────────────────────────────────────

def _route_llm_call(prompt: str, system: str) -> dict:
    """
    Routes to the first available LLM provider in priority order:
      1. Groq  (fastest, free tier)
      2. OpenAI
      3. Anthropic (Claude)
      4. Gemini (fallback with retry logic)
    """
    if GROQ_API_KEY and "gsk_" in GROQ_API_KEY:
        logger.info("Using provider: Groq")
        return _call_groq(prompt, system)

    if OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"):
        logger.info("Using provider: OpenAI")
        return _call_openai(prompt, system)

    if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY.startswith("sk-ant-"):
        logger.info("Using provider: Anthropic (Claude)")
        return _call_anthropic(prompt, system)

    logger.info("Using provider: Gemini")
    return _call_gemini(prompt, system)


# ── Public API ────────────────────────────────────────────────────────────────

def generate_react_step(history_text: str) -> dict:
    """
    Passes the ReAct conversation history to the active LLM provider
    and parses the next action (thought / action / action_input).
    """
    system = (
        "You are an autonomous ReAct agent. "
        "You must output ONLY valid JSON matching the exact requested formats."
    )
    try:
        return _route_llm_call(history_text, system)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in react step: {e}")
        return {"error": "Invalid JSON response from LLM."}
    except Exception as e:
        logger.error(f"LLM call failed in react step: {e}")
        return {"error": str(e)}
