# Realmente es un RAG.

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage, SystemMessage
# Para crear embeddings
from langchain_huggingface import HuggingFaceEmbeddings
# Para vector store
from langchain_core.vectorstores import InMemoryVectorStore
# Para cargar los documentos
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader

# Load the API key
load_dotenv()
directory = "My Documents"


def format_response(content: str | list):
    """Format the IA response"""
    if isinstance(content, list):
        text = " ".join(part.get("text", "") for part in content)
    else:
        text = content
    return text


# No hace falta pasar la api key si en .env el nombre de la variante de entorno es GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

# Vamos a obtener el context (Small String) usando técnicas de:
#   Embedding
#   Vector Store
#   Similarity Search

# Load Documents (pdf + txt + csv)
pdf_loader = PyPDFDirectoryLoader(directory)
pdf_docs = pdf_loader.load()

text_loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)
text_docs = text_loader.load()

csv_loader = DirectoryLoader(directory, glob="**/*.csv", loader_cls=TextLoader)
csv_docs = csv_loader.load()

docs = pdf_docs + text_docs + csv_docs

# Creating embeddings and vector store
# La librería sentence-transformers descarga automáticamente el modelo all-MiniLM-L6-v2
# Y el modelo será usado por el script Python para convertir documentos en listas de números.
# Luego, todo se almacenará en un vector store, en el que cada documento se representará por
# una larga lista de números llamados vectores.
# Sobre este vector store aplicaremos Similarity Search, ya que user_query también se convierte
# en una lista de números, y estos números se compararán con la lista de números de los
# documentos que están en el vector store.
# Los vectores similares se extraen y se convierte en un String (Small String)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(docs)

# Get user query
user_query = input("Enter your query: ")

# Similarity Search
# k es la cantidad de documentos que se devuelven, los más relacionados a lo que puede responder a nuestra pregunta.
# Esos 2 documentos son los que realmente se pasan al contexto (al LLM).
retreived_docs = vector_store.similarity_search(user_query, k=2)
context = "\n".join(doc.page_content for doc in retreived_docs)

# Inyectamos el contexto al sistem prompt.
system_prompt = f"""
You are a helpful assistant that answers questions about these documents: {context}
"""

# Set up message for the LLM
messages = [
    SystemMessage(content=system_prompt)
]

# Append the user query to messages
messages.append(HumanMessage(content=user_query))

# Invoke the LLM
response = llm.invoke(messages)
print(format_response(response.content))