"""
Simple Text Chat using LangChain v1 and Google Gemini
pip install langchain langchain-google-genai python-dotenv
"""

import base64
import mimetypes

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

image_path = "images/img.png"
mime_type, _ = mimetypes.guess_type(image_path) # Devuelve una tupla, donde el tipo de imagen es el primer valor de la tupla.

with open(image_path, 'rb') as file:
    raw_binary = file.read()
    base64_bytes = base64.b64encode(raw_binary)
    image_base64 = base64_bytes.decode("utf-8")
    # print(type(image_base64))

# Initialize the model
model = init_chat_model("gemini-3-flash-preview", model_provider="google_genai")

# Create message
# El contenido es una lista que contiene dos diccionarios.
# Lo que hay en los diccionarios es un formato estandarizado de Langchain que funciona
# tanto en Gemini como en otros modelos de IA.
# Notar que tenemos que convertir la imagen a base64 (string) porque no acepta bytes,
# e indicar el tipo de imagen ("image/png", etc.)
message = {"role": "user",
           "content": [{"type": "text", "text": "Describe what you see in this image."},
                       {"type": "image", "base64": image_base64, "mime_type": mime_type}]
           }

# Get and print the response
# invoke espera una lista de diccionarios, de ahí que message aparezca entre paréntesis.
response = model.invoke([message])
print(response.text)