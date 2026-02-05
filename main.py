from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool


load_dotenv()

class ResearchResponse(BaseModel):
    topic:str
    summary:str
    sources:list[str]
    tools_used:list[str]
    
# To use the free model, you need a Google API Key from https://aistudio.google.com/app/apikey
# Make sure GOOGLE_API_KEY is set in your .env file
# Using gemini-2.0-flash which is available in free tier
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
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

agent_executor = AgentExecutor(agent = agent, tools = tools,verbose = True)

query = input("Ask a question about anything: ")
import time
from google.api_core.exceptions import ResourceExhausted

max_retries = 5
base_delay = 10

raw_response = None
for attempt in range(max_retries):
    try:
        raw_response = agent_executor.invoke({"input": query})
        break
    except ResourceExhausted as e:
        print(f"Quota exceeded. Waiting for {60} seconds before retrying... (Attempt {attempt + 1}/{max_retries})")
        time.sleep(60)
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
             print(f"Hit rate limit. Waiting 60 seconds... (Attempt {attempt + 1}/{max_retries})")
             time.sleep(60)
        else:
            raise e
            
if raw_response is None:
    print("Failed to get response after multiple retries due to rate limits.")
    exit()

# print(raw_response)

try:
    output_text = raw_response.get("output")
    # Clean up markdown code blocks if present
    if "```json" in output_text:
        output_text = output_text.split("```json")[1].split("```")[0].strip()
    elif "```" in output_text: # Handle case where language isn't specified
        output_text = output_text.split("```")[1].split("```")[0].strip()
        
    structured_response = parser.parse(output_text)
    print(structured_response)
except Exception as e:
    print("error parsing response",e, "Raw Response:",raw_response)
    exit()
