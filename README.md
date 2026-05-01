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

## 🤝 Contributing
We politely welcome contributions! Feel free to open issues or submit pull requests. Please ensure your code adheres to our formatting guidelines.

*Thank you for using the AI Research Agent. Happy researching!*
