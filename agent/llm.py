import json
import logging
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

def generate_react_step(history_text: str) -> dict:
    """Passes the ReAct conversation history to Gemini and parses the next action."""
    if not GEMINI_API_KEY or "AIzaSy..." in GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set.")
        return {"error": "API key missing. Check your .env file."}

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=history_text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0,
                system_instruction="You are an autonomous ReAct agent. You must output ONLY valid JSON matching the exact requested formats."
            ),
        )
        content = response.text
        
        if not content:
             raise ValueError("Gemini returned empty content.")
        
        result = json.loads(content)
        return result
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM: {e}\nContent was: {content}")
        return {"error": "Invalid JSON response from LLM."}
    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        return {"error": str(e)}
