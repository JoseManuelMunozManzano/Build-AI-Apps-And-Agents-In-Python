# También podemos usar la función para crear agentes que
# hemos visto en otros proyectos
from langchain.chat_models import init_chat_model

# Para saber los modelos descargados, ejecutar
# en una terminal: ollama list
model = init_chat_model(
    model='qwen2.5-coder:7b',
    model_provider='ollama',
)

# Usando streams
for chunk in model.stream("Can I learn Python in one year?"):
    print(chunk.content, end="", flush=True)

# Respuesta cuando lo tiene todo
#response = model.invoke("Qué es una función en Python?")
#print(response.text)