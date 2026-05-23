from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()


# En general, es importante indicar el docstring.
# Pero en caso de agentes IA, es todavía más importante, porque el
# agente lee este docstring para comprender que hace la función,
# para poder decidir si ejecuta o no esta función.
#
# Igual, es importante el hint del tipo de dato, para que el LLM tenga más claro
# que el argumento esperado es un String.
#
# No vamos a usar ninguna API para obtener el tiempo (como Open Weather API).
# Solo vamos a devolver un valor, simulando que la API devuelve esto.
def get_weather(city: str):
    """Get weather for a given city"""
    #return "sunny"
    return {'condition':'sunny', 'temperature': 25}


# En la vida real, usaríamos la geolocalización del usuario.
# Por ejemplo, detectar la IP del usuario.
# De nuevo, lo importante es ver como funcionan los agentes.
# Es muy importante ser específico en el docstring.
def get_location():
    """Get user's current location. Use this when the user asks about weather
    without specifying a city"""
    return "Rome, Italy"


# Initialize Gemini Flash
# temperature a 0.7 indica que queremos las respuestas más creativas.
# temperature a 0.1 indica que queremos las respuestas más rígidas, pero más precisas.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

# Al agente le pasamos, como mínimo, el modelo.
# También tenemos que indicar las funciones que puede invocar.
# También podemos indicar un prompt, usando un string. Tener en cuenta lo siguiente:
#   Es importante comenzar indicando siempre el rol del agente (qué es lo que hace)
#   Luego, es opcional, pero bueno, especificar el flujo de trabajo que queremos que siga el agente de IA.
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
    system_prompt=system_prompt
)


# La función invoke, cuando es un agente, espera un diccionario en vez de un string.
# Tenemos que indicar como key del diccionario messages, y una lista que a su vez tenga uno o más diccionarios.
response1 = agent.invoke(
    {"messages": [{'role': 'user',
                   'content': 'How is the weather?'}]})

# Cogemos de la respuesta la parte que necesitamos.
print(response1['messages'][-1].content)