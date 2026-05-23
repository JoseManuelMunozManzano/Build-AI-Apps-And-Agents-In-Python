import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os


load_dotenv()

def get_weather(city: str):
    """Get weather for a given city.
    Return the temperature_fahrenheit value in Fahrenheit label for locations such as US, Liberia, Burma"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    temperature_celsius = data['main']['temp']
    temperature_fahrenheit = temperature_celsius * 9/5 + 32
    # Es importante devolver un diccionario, para que dada la clave,
    # la IA sepa a que se refiere el valor.
    return data, {'temperature_fahrenheit': temperature_fahrenheit}


def get_location():
    """Get user's current location. Use this when the user asks about weather."""
    # El header {'User-agent': 'your-bot 0.1'} imita al navegador.
    response = requests.get("https://ipapi.co/json/", headers = {'User-agent': 'your-bot 0.1'})
    data = response.json()
    city = data['city']
    country = data.get('country_name')
    return f"{city}, {country}"


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

3. Use your knowledge to determine which temperature unit is standard for the given location.

4. Present the weather information including temperature, condition, wind speed, and any other relevant details.

"""

agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt
)

# Para probar las funciones sin ejecutar la IA.
#
# Queremos que se ejecute este trozo de código cuando el usuario ejecuta
# python main.py
#
# Pero este código no se ejecuta si abrimos una consola de Python
# usando en la terminal el comando python y ejecutamos estas sentencias:
#           import main
#           main.get_weather('madrid')
#           main.get_location()
if __name__ == "__main__":
    user_query = input("Enter you query: ")

    response1 = agent.invoke(
        {"messages": [{'role': 'user',
                    'content': user_query}]})
    
    content = response1['messages'][-1].content

    if isinstance(content, list):
        text = " ".join(part.get("text", "") for part in content)
    else:
        text = content

    print(text)