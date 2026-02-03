from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

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

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "search",
    func = search.run,
    description = "Search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results = 1, doc_content_chars_max = 100)
wiki_tool = Tool(
    name = "wiki",
    func = api_wrapper.run,
    description = "Search Wikipedia for information"
)

