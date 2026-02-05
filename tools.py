from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime
import time

def save_to_txt(data:str, filename:str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{filename}"
    with open(filename, "w") as f:
        f.write(data)
    return f"Data saved to {filename}"

save_tool = Tool(
    name = "save_to_txt",
    func = save_to_txt,
    description = "Save data to a text file"
)

# DuckDuckGo search with retry logic to handle rate limits
search = DuckDuckGoSearchRun()

def search_with_retry(query: str, max_retries: int = 3) -> str:
    """Search with retry logic to handle DuckDuckGo rate limits."""
    for attempt in range(max_retries):
        try:
            result = search.run(query)
            return result
        except Exception as e:
            error_str = str(e).lower()
            if "ratelimit" in error_str or "rate" in error_str or "429" in error_str:
                wait_time = (attempt + 1) * 10  # 10s, 20s, 30s
                print(f"DuckDuckGo rate limit hit. Waiting {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                # For non-rate-limit errors, return a fallback message
                return f"Search temporarily unavailable: {str(e)[:100]}"
    return "Search failed after multiple retries due to rate limits. Try Wikipedia instead."

search_tool = Tool(
    name = "search",
    func = search_with_retry,
    description = "Search the web for information. Has retry logic for rate limits."
)

api_wrapper = WikipediaAPIWrapper(top_k_results = 1, doc_content_chars_max = 100)
wiki_tool = Tool(
    name = "wiki",
    func = api_wrapper.run,
    description = "Search Wikipedia for information"
)

