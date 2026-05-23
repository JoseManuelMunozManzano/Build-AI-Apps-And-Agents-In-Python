from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
# Usando PostgreSQL
from langgraph.checkpoint.postgres import PostgresSaver
import os

load_dotenv()

DB_URI = os.getenv("POSTGRESQL_DB_URI")

def get_weather(city: str):
    """Get weather for a given city"""
    return {'condition':'sunny', 'temperature': 25}

def get_location():
    """Get user's current location. Use this when the user asks about weather."""
    return "Rome, Italy"

def format_response(content: str | list):
    """Format the IA response"""
    if isinstance(content, list):
        text = " ".join(part.get("text", "") for part in content)
    else:
        text = content
    return text

# Initialize Gemini Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.7,
)
system_prompt = """
You are a helpful weather assistant. 
YOUR WORKFLOW:
1. If the user asks about weather WITHOUT specifying a location, you MUST:
   - First call get_location() to find their location
   - Then call get_weather(city) with that location
   
2. If the user provides a city, call get_weather(city) directly.

"""

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # Esto hay que hacerlo cuando nos conectamos a una BD.
    # Crea las tablas necesarias si no existen.
    checkpointer.setup()
    agent = create_agent(
        model=llm,
        tools=[get_weather, get_location],
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )

    while True:
        user_query = input("Enter your query: ")
        if user_query in ['bye', 'quit', 'exit']:
            break
        response = agent.invoke({"messages": [{'role': 'user', 'content':user_query}]},
                                 {"configurable": {"thread_id":"1"}})
        # for i in response['messages']:
        #     if i.type == 'human':
        #         print("You: ", format_response(i.content))
        #     if i.type == 'ai' and i.content:
        #         print("Agent: ", format_response(i.content))

        print(format_response(response['messages'][-1].content))