
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import time
from google.api_core.exceptions import ResourceExhausted

# Rich imports
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.status import Status
from rich.text import Text

load_dotenv()

# Initialize Rich Console
console = Console()

class ResearchResponse(BaseModel):
    topic:str
    summary:str
    sources:list[str]
    tools_used:list[str]
    
# To use the free model, you need a Google API Key from https://aistudio.google.com/app/apikey
# Make sure GOOGLE_API_KEY is set in your .env file
# Using gemini-2.5-flash which is available in free tier
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that researches and answers questions on various topics. Wrap the output in this format and provide no other text. Ensure the output is valid JSON. \n{format_instructions}",
        ),
        ( "placeholder","{chat_history}"),  
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(llm = llm, tools = tools, prompt = prompt)

# Set verbose to False to abstract away the logs as requested
agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = False)

# Clear screen for better performance/look
console.clear()

console.print(Panel.fit("[bold blue]AI Research Assistant[/bold blue]", subtitle="Powered by Gemini"))

query = Prompt.ask("[bold green]Ask a question about anything[/bold green]")

max_retries = 5
base_delay = 10

raw_response = None
with console.status("[bold yellow]Researching...[/bold yellow]", spinner="dots"):
    for attempt in range(max_retries):
        try:
            raw_response = agent_executor.invoke({"input": query})
            break
        except ResourceExhausted as e:
            console.print(f"[red]Quota exceeded. Waiting for {60} seconds before retrying... (Attempt {attempt + 1}/{max_retries})[/red]")
            time.sleep(60)
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                 console.print(f"[red]Hit rate limit. Waiting 60 seconds... (Attempt {attempt + 1}/{max_retries})[/red]")
                 time.sleep(60)
            else:
                console.print(f"[red]Error occurred: {e}[/red]")
                raise e
            
if raw_response is None:
    console.print("[bold red]Failed to get response after multiple retries due to rate limits.[/bold red]")
    exit()

try:
    output_text = raw_response.get("output")
    if isinstance(output_text, list):
        full_text = ""
        for item in output_text:
            if isinstance(item, dict):
                full_text += item.get("text", "")
            elif isinstance(item, str):
                full_text += item
        output_text = full_text
    # Clean up markdown code blocks if present
    if "```json" in output_text:
        output_text = output_text.split("```json")[1].split("```")[0].strip()
    elif "```" in output_text: # Handle case where language isn't specified
        output_text = output_text.split("```")[1].split("```")[0].strip()
        
    structured_response = parser.parse(output_text)
    
    # Display Result
    sources_text = ", ".join(structured_response.sources) if structured_response.sources else "None"
    tools_text = ", ".join(structured_response.tools_used) if structured_response.tools_used else "None"
    
    md = Markdown(structured_response.summary)
    
    console.print(Panel(
        md,
        title=f"[bold cyan]{structured_response.topic}[/bold cyan]",
        subtitle=f"[dim]Sources: {sources_text} | Tools: {tools_text}[/dim]",
        border_style="green",
        expand=False
    ))
    
except Exception as e:
    console.print(f"[bold red]Error parsing response:[/bold red] {e}")
    console.print(f"Raw Response: {raw_response}")
    exit()
