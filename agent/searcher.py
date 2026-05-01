import logging
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from config import MAX_SEARCH_RESULTS, MAX_CONTENT_CHARS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

def search_web(query: str) -> list[dict]:
    """Uses DuckDuckGo to find top URLs for the query."""
    try:
        results = DDGS().text(query, max_results=MAX_SEARCH_RESULTS)
        # return list of dicts with title and href
        return [{"title": r.get("title", ""), "href": r.get("href", "")} for r in results]
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []

def read_url(url: str) -> str:
    """Fetches URL and extracts text content using BeautifulSoup."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # Remove noisy elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.extract()
        
        text = soup.get_text(separator="\n", strip=True)
        
        # Simple data filtering: truncate if too long to prevent context explosion
        if len(text) > MAX_CONTENT_CHARS:
            text = text[:MAX_CONTENT_CHARS] + "\n...[TRUNCATED]"
            
        return text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return f"Error fetching {url}: {e}"
