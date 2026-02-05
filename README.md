# Python AI Research Agent

A LangChain-powered AI research agent that can search the web, query Wikipedia, and save results to files using Google's Gemini API.

## Features

- 🔍 **Web Search**: DuckDuckGo search with automatic retry logic for rate limits
- 📚 **Wikipedia**: Query Wikipedia for factual information
- 💾 **Save Results**: Export research findings to timestamped text files
- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash model (free tier)

## Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# myenv\Scripts\activate   # Windows

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get a free Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Agent

```bash
python main.py
```

## Dependencies

Key packages (see `requirements.txt` for full list):

- `langchain` - Agent framework
- `langchain-google-genai` - Google Gemini integration
- `langchain-community` - Community tools (DuckDuckGo, Wikipedia)
- `ddgs` - DuckDuckGo search library
- `python-dotenv` - Environment variable management

## Rate Limits (Free Tier)

**Google Gemini API:**

- 15 requests per minute
- 1 million tokens per minute
- Daily limits apply

**DuckDuckGo:**

- Built-in retry logic handles rate limits automatically
- Falls back gracefully after 3 retries

## Project Structure

```
├── main.py           # Main agent entry point
├── tools.py          # Tool definitions (search, wiki, save)
├── requirements.txt  # Python dependencies
├── .env              # API keys (create this file)
└── README.md         # This file
```

## Troubleshooting

### Rate Limit Errors (429)

- Wait a few minutes and try again
- The agent has built-in retry logic for both Gemini API and DuckDuckGo
- Consider upgrading to a paid plan for higher limits

### Model Not Found Errors

- Ensure you're using `gemini-2.0-flash` (current recommended model)
- Check that your API key is valid and set correctly

## License

MIT License
