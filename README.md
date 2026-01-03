# AI Visibility Tracker

AI Visibility Tracker is a Python-based tool that monitors your brand's presence in AI-generated responses. As AI search engines reshape how users discover information, this tool helps you understand where you stand in the AI visibility landscape and provides actionable insights to improve your positioning.

## Key Features

- **Sentiment Analysis**: Monitor how your brand is portrayed—positive, neutral, or negative
- **Citation Tracking**: Identify which URLs and pages are being cited by AI systems
- **Competitor Benchmarking**: Compare your visibility against competitors across AI engines
- **Prompt-Level Insights**: See which user queries trigger your brand mentions
- **Interactive Dashboard**: Visualize trends, metrics, and opportunities in real-time

## Installation

### Prerequisites

- Python 3.8+
- pip or [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/R-Yash/AI-Visibility-Tracker.git
   cd AI-Visibility-Tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or with uv:
   ```bash
   uv sync
   ```

3. Create a .env file and set up environment variables:
   ```bash
   GEMINI_API_KEY = YOUR API KEY HERE
   ```

## Quick Start

Launch the interactive dashboard:
```bash
streamlit run dashboard.py
```
The app will open automatically at `http://localhost:8501`. Enter a product category (e.g., "CRM Software") and list of competitors to start the analysis.

## Project Structure

- `main.py` - Core Logic and Functions
- `dashboard.py` - Interactive web-based visualization dashboard
- `prompts.py` - AI prompt templates and utilities for queries
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration

## Key Decisions

* **Google Search Grounding:** Instead of building a complex custom web scraper, I utilized Google GenAI's native `tools=[google_search]`. This provides verified, accurate citation data directly from the model's grounding metadata, ensuring the "Citation Share" metric reflects actual AI sourcing behavior.
* **Structured Output (Pydantic):** I used `pydantic` BaseModels to force the LLM to return prompt suggestions in a strict JSON format. This eliminates parsing errors and ensures the analysis pipeline never breaks due to malformed AI responses.
* **Streamlit for UI:** Chosen for its ability to rapidly turn data scripts into interactive web apps. It handles the visualization state and data caching natively, allowing for a focus on the analysis logic.
* **Gemini 2.5 Flash:** Selected as the underlying model for its low latency and high cost-efficiency, which is critical when running high-volume batch analysis loops.

## Future Improvements
* **Backend Implementation:** Implement a FastAPI Backend to seperate code execution from the frontend and allow for more scalable solutions.
* **Async/Parallel Processing:** Currently, the analysis loops through prompts sequentially. Implementing `asyncio` for the LLM calls would reduce the "Run Analysis" time by ~80%.
* **Historical Tracking:** Connect the dashboard to a simple database like Postgres to save run data. This would allow users to track how their brand visibility trends over time.
* **Sentiment Analysis:** Enhance the "Contexts" feature by running a secondary lightweight sentiment classification on the mentions (Positive/Neutral/Negative) rather than just listing them.
* **Multi-Model Support:** The long term goal is to compare visibility across all major LLM proviers.

