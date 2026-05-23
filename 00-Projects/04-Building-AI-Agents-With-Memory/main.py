from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
# Para dar historial de chat a la IA necesitamos langgraph
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


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

agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt,
    # Para dar historial de chat a la IA
    checkpointer=InMemorySaver()
)

print("First conversation")
user_query1 = input("Enter your query: ")
# Necesario el segundo argumento (diccionario) para dar historial de chat (memoria) a la IA
# En concreto, esto: {"configurable": {"thread_id": "1"}}
# thread_id puede valer cualquier número, y todas las respuestas producidas con ese thread_id
# estarán conectadas entre sí. Esto significa que podemos crear más thread_id si queremos 
# mantener varias conversaciones.
response1 = agent.invoke({"messages": [{'role': 'user', 'content': user_query1}]},
                         {"configurable": {"thread_id": "1"}})
print(format_response(response1['messages'][-1].content))

print("Second conversation")
user_query2 = input("Enter your query: ")
response2 = agent.invoke({"messages": [{'role': 'user', 'content': user_query2}]},
                         {"configurable": {"thread_id": "1"}})
print(format_response(response2['messages'][-1].content))


# Aquí usamos otro thread_id distinto, por lo que es una conversación distinta.
print("Third conversation")
user_query3 = input("Enter your query: ")
response3 = agent.invoke({"messages": [{'role': 'user', 'content': user_query3}]},
                         {"configurable": {"thread_id": "2"}})
print(format_response(response3['messages'][-1].content))