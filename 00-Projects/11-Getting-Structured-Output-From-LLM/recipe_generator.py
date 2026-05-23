from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import List

load_dotenv()


class Recipe(BaseModel):
    name: str = Field(description="Name of the recipe")
    description: str = Field(description = "Brief description of the recipe")
    prep_time: str = Field(description="Estimated preparation time of the recipe")

# Esta es la plantilla.
# ingredients en el nombre de la key y Field... es el value.
# Notar que recipes es del tipo Recipe (otra plantilla)
# Con esto damos instrucciones a Langchain usando Pydantic.
# Y Langchain da las instrucciones al LLM.
class Response(BaseModel):
    """A single recipe"""
    ingredients: List[str] = Field(description="List of main ingredients")
    recipes: List[Recipe] = Field(description="List of 3 recipe suggestions")



# Initialize the model
model = init_chat_model("gemini-3-flash-preview", model_provider="google_genai")
structured_model = model.with_structured_output(Response)
system_prompt = """
"You are a helpful chef. Identify the main ingredients. Suggest 3 recipes based those ingredients."
"""

# Create message
message = [{"role": "system", "content": system_prompt},
           {"role": "user", "content": "I have broccoli, butter, and eggs."}]

# Get and print the response
# En vez de invocar el modelo invocamos el modelo pero con la salida estructurada que queremos.
# structured_model es una derivación del modelo.
response = structured_model.invoke(message)
# Como la respuesta ya no es texto plano, usamos model_dump() en vez de text.
print(response.model_dump())