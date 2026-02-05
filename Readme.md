# AI Research Agent with Gemini & LangChain

This project is a Python-based AI Agent capable of performing autonomous research on any topic. It utilizes **Google's Gemini 2.5 Flash** (via LangChain) to understand queries, and uses a suite of tools to gather information from the web and Wikipedia, finally structuring and saving the results.

## 🚀 Features

- **Autonomous Research**: Break down queries and search for information.
- **Multi-Source Retrieval**:
  - **DuckDuckGo Search**: For real-time web results.
  - **Wikipedia**: For encyclopedic knowledge.
- **Structured Output**: Returns data in a consistent JSON format (Topic, Summary, Sources, Tools Used).
- **File Persistence**: Can save research findings directly to text files.
- **Robust Error Handling**: Includes automatic retries for Google API rate limits (429 errors).

## 🛠️ Prerequisites

- Python 3.10 or higher
- A Google AI Studio API Key (for Gemini)

## 📦 Installation

1.  **Clone the repository** (if applicable) or navigate to the project folder.

2.  **Create a virtual environment**:

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Google API Key:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```
    _You can get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)._

## 🏃 Usage

Run the main script:

```bash
python main.py
```

1.  The agent will ask: `Ask a question about anything:`
2.  Type your query (e.g., _"What is the future of quantum computing?"_).
3.  The agent will use its tools to find answers.
4.  It will display the structured result and optionally save it to a file.

## 📂 Project Structure

- `main.py`: The entry point. Initializes the Gemini LLM, configures the Agent, handles the user input loop, and manages error handling (retries).
- `tools.py`: Definitions for the agent's capabilities:
  - `search_tool`: DuckDuckGo search integration.
  - `wiki_tool`: Wikipedia API wrapper.
  - `save_tool`: Function to write text to disk.
- `requirements.txt`: Python package dependencies.

## ⚠️ Troubleshooting

### Quota Exceeded (429 Error)

If you see `ResourceExhausted` or "Quota exceeded", it means you have hit the rate limit for the free Gemini API tier.

- **Free Tier Limits**: `gemini-2.5-flash` has a limit of **5 requests per minute (RPM)** on the free tier.
- **Solution**: The script will automatically wait 60 seconds and retry up to 5 times. If the issue persists:
  - Wait for the rate limit window to reset (1 minute for RPM limits)
  - Reduce the frequency of requests
  - Consider upgrading to a paid plan for higher quotas

### Model Not Found (404 Error)

If you encounter a 404 error regarding the model name:

- **Check Available Models**: Run `python list_models.py` to see which models are available for your API key.
- **Update Model**: Edit `main.py` line 21 and change the model name in `ChatGoogleGenerativeAI(model="...")`.
- **Recommended Free Tier Models**: `gemini-2.5-flash`, `gemini-flash-latest`

### Rate Limit Best Practices

- The agent makes multiple API calls per query (for tool calling and final response)
- On free tier, limit your queries to avoid hitting the 5 RPM cap
- Each research query may use 3-5 API calls depending on complexity
