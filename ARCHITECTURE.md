# Architecture and Tradeoffs

## 1. System Architecture
The AI Research Agent uses a **ReAct (Reasoning and Acting)** loop architecture. Instead of a hardcoded linear pipeline (Search -> LLM), the agent dynamically iterates through thoughts, actions, and observations.

- **Orchestrator (`orchestrator.py`)**: Manages the conversation loop with the LLM, parses the LLM's chosen actions, executes local Python tools, and appends the observations back into the context window.
- **Search & Retrieval (`searcher.py`)**: Provides tools to the agent, such as searching the web and reading specific URLs. Crucially, extracted content is chunked and filtered to remove noise before being sent to the LLM.
- **LLM Engine (`llm.py`)**: Uses Google's `genai` SDK to reason over the conversation history and decide whether to gather more information or produce the final JSON output.

## 2. Tool Selection Strategy
The agent dynamically selects tools based on the user's query:
- `search_web(query)`: Uses DuckDuckGo to find recent URLs.
- `read_url(url)`: Fetches HTML, strips boilerplate, and returns the text.
- `final_answer()`: Triggers the completion of the task.

If a query requires general knowledge, the agent might skip searching altogether. If it requires deep research, it might call `search_web` multiple times with different keywords.

## 3. Data Filtering & Noise Reduction
A major challenge with web scraping is context window pollution. We address this by:
1. Stripping all `<script>` and `<style>` tags via BeautifulSoup.
2. Limiting the total extracted characters per page.
3. The LLM acts as an active filter—if a page is irrelevant, it ignores it and continues searching.

## 4. Tradeoffs and Limitations

### DuckDuckGo vs. Paid Search APIs
**Tradeoff**: We chose `ddgs` (DuckDuckGo) because it is free and requires no API keys, making the project highly portable.
**Limitation**: DuckDuckGo's unofficial library is subject to rate limiting and sometimes returns fewer high-quality academic results compared to enterprise solutions like SerpAPI or Google Custom Search.

### BeautifulSoup vs. Headless Browsers
**Tradeoff**: We use `requests` + `BeautifulSoup` for high speed and minimal dependencies.
**Limitation**: This approach completely fails on Client-Side Rendered (React/Angular) websites or sites protected by Cloudflare/CAPTCHAs (e.g., scientific journals). A headless browser (like Playwright) would bypass these but massively increase the complexity and resource footprint of the app.

### LLM Context Size
**Tradeoff**: Passing full website text into the prompt gives the LLM maximum context.
**Limitation**: Even with large context windows (like Gemini 1.5/2.0), extremely long pages must be arbitrarily truncated (e.g., at 4000 chars), which risks cutting off the exact paragraph needed. A Vector DB + RAG approach would be superior for massive documents but is overkill for simple web queries.

## 5. Failure Handling
- **API Errors**: Caught gracefully, returning structured error messages to the CLI/Web UI.
- **Scraping Failures**: If a site blocks our scraper, `read_url` returns an empty string or error string, and the ReAct agent observes this and knows to try a different URL.
- **Hallucination Prevention**: The prompt strictly instructs the agent to cite sources for its claims and assign a "Low" confidence if it had to guess or rely on weak general knowledge.
