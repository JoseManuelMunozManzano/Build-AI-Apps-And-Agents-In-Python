import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Nos conectamos al modelo de Gemini.
model = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google-genai",
    api_key=GOOGLE_API_KEY)

# Le mandamos al modelo una pregunta y asignamos su respuesta a una variable que luego imprimimos.
# La respuesta depende del modelo. En Gemini es un JSON del tipo content=[{}], donde las llaves
# significa que tenemos una lista de diccionarios.
# Por eso indicamos .content[0]['text'] al imprimir la respuesta, ya que ahí está en concreto
# el texto de la respuesta.
# Como el modo gratuito tiene un límite, si ejecutamos esto muchas veces, llegará un momento
# donde obtendremos un error.
with open('wood.txt') as file:
    wood = file.read()

response = model.invoke(f"Which of these is best for furniture: {wood}?")
print(response.content[0]['text'])