# AI Research Agent with Gemini & Rich UI

A powerful, autonomously researching AI agent powered by **Google's Gemini Flash** (Free Tier). This agent breaks down complex queries, searches the web and Wikipedia, and presents the results in a beautiful, structured terminal interface.

## 🚀 Features

- **Autonomous Research**: Intelligently breaks down queries to find comprehensive answers.
- **Multi-Source Retrieval**:
  - **DuckDuckGo Search**: For real-time web information.
  - **Wikipedia**: For encyclopedic knowledge.
- **Premium Terminal UI**: Built with `rich` for a clean, app-like experience with loading spinners and formatted panels.
- **Structured Output**: Delivers clear, concise summaries with sources and tool usage.
- **Robust Error Handling**: Automatically handles rate limits and retries for uninterrupted usage.

## 🛠️ Prerequisites

- **Python 3.10+**
- **Google AI Studio API Key** (Free)

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd Python_AI_Agent_project
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   # myenv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key**:
   - Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Create a `.env` file in the root directory:
     ```env
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

## 🏃 Usage

Run the agent:

```bash
python main.py
```

1. The interface will launch with a clean banner.
2. Enter your question (e.g., _"What are the latest breakthroughs in fusion energy?"_).
3. The agent will show a **loading spinner** while it researches.
4. The final answer will be displayed in a **formatted panel** with sources.

## 🧠 Why We Use the Free Model

We use the **Gemini Flash** model (specifically `gemini-flash-latest` or `gemini-2.5-flash`) for this project because:

1.  **Cost-Effective**: It allows for extensive testing and development without incurring costs.
2.  **Speed**: The "Flash" models are optimized for low latency, providing quick responses for interactive agents.
3.  **Capability**: Despite being free, it has excellent reasoning and tool-use capabilities sufficient for research tasks.

## ⚠️ Challenges & Troubleshooting

### Rate Limits (429 Errors)

The free tier has strict rate limits (e.g., 5-15 requests per minute).

- **Challenge**: Complex queries triggers multiple internal steps (searching, reading, summarizing), which can quickly hit the limit.
- **Solution**: The agent includes built-in **exponential backoff**. If it hits a limit, it will wait (e.g., 60 seconds) and retry automatically.

### Model Availability (404/Found Errors)

Google frequently updates model names (e.g., `gemini-1.5-flash` vs `gemini-2.0-flash`).

- **Solution**: We currently use `gemini-flash-latest` which points to the newest stable version.

### "Limit Exceeded"

If you see a quota error despite retries, you may have exhausted your daily free tier allowance.

- **Fix**: Wait for the quota to reset (usually daily) or switch to a different Google account/API key.

## 📂 Project Structure

- `main.py`: Core logic, UI (Rich), and Agent configuration.
- `tools.py`: Tool definitions (Search, Wiki, File Save).
- `requirements.txt`: Dependencies.
- `.env`: API Credentials.
