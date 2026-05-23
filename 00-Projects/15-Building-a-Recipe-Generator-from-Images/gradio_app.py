import gradio as gr
import base64
import mimetypes

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Initialize the model
model = init_chat_model("gemini-3-flash-preview", model_provider="google_genai")

system_prompt = """
"You are a helpful chef. Identify the main ingredients. Suggest 3 recipes based on those ingredients."
"""

def identify_ingredients(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)

    with open(image_path, 'rb') as file:
        raw_binary = file.read()
        base64_bytes = base64.b64encode(raw_binary)
        image_base64 = base64_bytes.decode("utf-8")

    # Create message
    # Hemos quitado los paréntesis de invoke([message]) y los hemos puesto aquí.
    message = [{"role": "system", "content": system_prompt},
               {"role": "user", "content": [{"type": "image", "base64": image_base64, "mime_type": mime_type}]}]

    response = model.invoke(message)
    return response.text

demo = gr.Interface(
    fn=identify_ingredients, # Esta es la función conectadora entre inputs y outputs
    inputs=gr.Image(type="filepath"), # La imagen subida se manda como argumento a identify_ingredients
    outputs=gr.Markdown(),  # La salida de identify_ingredients se escribe en outputs
    title='Recipe Generator',
    description="Upload an image with ingredients",
    flagging_mode="never"   # No muestra el botón Flag (obtiene feedback, logs, de la app)
)

# Así es como lanzamos la app
demo.launch(debug=True)