import json
from flask import Flask, request, Response
from langchain.chat_models import init_chat_model

app = Flask(__name__)

model = init_chat_model(
    model="gemma4:latest",
    model_provider="ollama"
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data["messages"]

    def generate():
        for chunk in model.stream(messages):
            if chunk.content:
                yield json.dumps({
                    "message": {
                        "role": "assistant",
                        "content": chunk.content
                    }
                }) + "\n"

    return Response(generate(), content_type="application/x-ndjson")


if __name__ == "__main__":
    app.run(debug=True, port=5002, threaded=True)