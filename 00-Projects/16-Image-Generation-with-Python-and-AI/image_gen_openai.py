from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

user_prompt = "create me an image of a boss bird swimming in the sea"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.images.generate(
    model="gpt-image-1",
    prompt=user_prompt,
    size="1024x1024"
)

# Guardamos la imagen en un fichero
image_base64 = response.data[0].b64_json

with open("generated_image.png", "wb") as f:
    f.write(base64.b64decode(image_base64))