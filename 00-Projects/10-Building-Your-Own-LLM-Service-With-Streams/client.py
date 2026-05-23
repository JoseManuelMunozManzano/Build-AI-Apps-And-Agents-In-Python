import json
import requests

API_URL = "http://localhost:5002"
url = f"{API_URL}/chat"

history = []

while True:
    user_input = input("You: ")

    history.append({
        "role": "user",
        "content": user_input
    })

    assistant_content = ""

    with requests.post(
        url,
        json={"messages": history},
        stream=True
    ) as response:

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            chunk = data["message"]["content"]
            assistant_content += chunk

            print(chunk, end="", flush=True)

    print()

    history.append({
        "role": "assistant",
        "content": assistant_content
    })