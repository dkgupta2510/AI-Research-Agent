# 🤖 AI Research Agent

Welcome to the **AI Research Agent**! This application is designed to act as your intelligent, autonomous research assistant. Powered by Google Gemini and real-time web search capabilities (via DuckDuckGo), it dynamically fetches live data, reasons over the information, and presents beautifully structured insights.

---

## ✨ Features

- **Real-time Web Search:** Automatically scours the web for the most up-to-date information.
- **Agentic Reasoning:** Parses multiple sources, extracts key findings, and synthesizes accurate answers.
- **Structured Output:** Beautifully formats results into actionable Research Plans, Answers, Key Findings, Limitations, and Next Steps.
- **Dual Interface:** Run it via a robust Command Line Interface (CLI) or through a stunning, modern Web UI.
- **Fully Automated Logging:** Automatically saves all queries and results in JSON format for later review.

---

## 🛠️ Installation

1. **Clone or Download the Repository**
2. **Install Dependencies:**
   Make sure you have Python 3.9+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Copy the example environment file and update it with your Google Gemini API key:
   ```bash
   copy .env.example .env
   ```
   *Open `.env` and replace `AIzaSy...` with your actual key from [Google AI Studio](https://aistudio.google.com/app/apikey).*

---

## 🚀 Usage

### 1. The Web UI (Recommended)
Experience the sleek, modern interface with glassmorphism and smooth animations.

To start the web server, run:
```bash
python app.py
```
*(Alternatively: `uvicorn app:app --reload`)*

Then, open your browser and navigate to: **http://127.0.0.1:8000**

### 2. The CLI (Command Line Interface)
For quick terminal access, you can run the agent in interactive mode:
```bash
python cli.py
```

Or, ask a single question directly:
```bash
python cli.py --query "What is quantum computing?"
```

---

## 🏗️ Architecture

- **Backend / Pipeline**: Python 3.11+, FastAPI, `google-genai`, `ddgs` (DuckDuckGo Search), and BeautifulSoup4.
- **Frontend**: Pure HTML5, Vanilla JavaScript, and CSS3 (with zero heavy frontend frameworks).

---

## Why Agent Approach
Traditional semantic search or standard RAG implementations often fail on complex, multi-hop queries. An agentic approach allows the system to autonomously break down the user query, plan its execution, dynamically search the live web, and iteratively refine its context. By operating in an observe-act-evaluate loop, the agent ensures that the final response is highly contextualized and structurally robust, emitting a predictable, structured JSON payload that downstream services can reliably consume.

## Tools Used
- **Google Gemini API**: Serves as the core reasoning engine. We chose Gemini for its strong instruction-following capabilities, fast inference times, and native JSON-mode support, which is critical for enforcing structured output schemas.
- **DuckDuckGo Search (`ddgs`)**: Integrated for real-time web discovery. It provides a lightweight, unauthenticated entry point to live internet data without strict rate limits.
- **BeautifulSoup4**: Used for DOM parsing and content extraction. It reliably sanitizes raw HTML into dense, readable text, minimizing token overhead before injecting content into the LLM context window.
- **FastAPI**: Powers the asynchronous backend routing, allowing the tool-calling and LLM-generation loops to run without blocking the event loop.

## Hallucination Mitigation
Hallucination is aggressively mitigated through strict prompt engineering, grounding, and programmatic confidence checks. The system is designed to fail gracefully rather than fabricate information. For example, during edge-case testing (e.g., Query: *"Compare quantum biology theories in plants"*), the system accurately detects the lack of reliable, retrieved data. Instead of generating a hallucinated response, it returns a structured JSON payload with a `LOW` confidence score and explicit limitations, prioritizing safety and reliability over ungrounded completion.

## Tradeoffs
- **Latency vs. Accuracy**: Executing live web searches, scraping DOMs, and running multi-step reasoning cycles inherently introduces higher latency compared to a single-shot LLM inference.
- **Token Consumption**: Pumping raw, extracted web text into the context window for evaluation significantly increases token usage, which impacts both cost and context limits.
- **Non-Deterministic Searching**: Relying on live search engines means the quality of the final output is tightly coupled to SEO rankings and search engine algorithmic whims on any given day.

## Future Improvements
- **Parallel Search Execution**: Refactoring the pipeline to fan-out search queries concurrently, heavily reducing total execution time.
- **Vector-Backed Memory Cache**: Storing previous queries and their parsed results locally to short-circuit redundant web scraping and LLM evaluations.
- **Specialized Tooling**: Integrating domain-specific search endpoints (e.g., ArXiv, PubMed, or financial APIs) to improve the quality of data retrieval for technical subjects.

---

## 🤝 Contributing
We politely welcome contributions! Feel free to open issues or submit pull requests. Please ensure your code adheres to our formatting guidelines.

*Thank you for using the AI Research Agent. Happy researching!*
