# Realmente no es un RAG sino una inyección de contexto.

from pathlib import Path
from pypdf import PdfReader

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Para pasar system_prompt + big_string y user_prompt al LLM.
from langchain.messages import HumanMessage, SystemMessage

# Load the API key
load_dotenv()


def format_response(content: str | list):
    """Format the IA response"""
    if isinstance(content, list):
        text = " ".join(part.get("text", "") for part in content)
    else:
        text = content
    return text


def load_documents(directory = 'My Documents'):
    documents = []
    # Iterate over each file
    for file_path in Path(directory).rglob('*'):
        if file_path.suffix in {'.txt', '.pdf', '.md'}:
            if file_path.suffix == '.pdf':
                reader = PdfReader(file_path)
                content = "\n".join(page.extract_text() for page in reader.pages)
            else:
                content = file_path.read_text()
            documents.append({
                'path': str(file_path),
                'content': content
            })
    return documents


def create_context(document_list):
    context = ''
    for doc in document_list:
        context = context + f'{doc['path']}:\n{doc['content']}\n----------------------\n'
    return context


documents = load_documents()
context = create_context(documents) # context es Big String

system_prompt = f"""
You are a helpful assistant that answers questions about these documents: {context}
"""

# Set up message for the LLM
messages = [
    SystemMessage(content=system_prompt)
]

# No hace falta pasar la api key si en .env el nombre de la variante de entorno es GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

while True:
    # Get user query
    user_query = input("Enter your query: ")
    
    # Append the user query to messages
    messages.append(HumanMessage(content=user_query))

    # Invoke the LLM
    response = llm.invoke(messages)
    # <class 'langchain_core.messages.ai.AIMessage'>
    # print(type(response))
    
    # Display and add (for history) the response to messages
    print(format_response(response.content))
    messages.append(response)