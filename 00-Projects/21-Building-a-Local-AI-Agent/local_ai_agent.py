import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

console = Console()

# Elegir uno de los modelos y comentar el otro.
llm = init_chat_model(
    # "gemini-3-flash-preview",
    # model_provider='google_genai',
    "gpt-5-mini",
    model_provider='openai',
    temperature=0.5,
)


def list_directory(path: str=".") -> str:
    """List all files and folders in the given directory path. Default is current directory."""
    try:
        result = ""
        items = os.listdir(path)
        
        files = []
        folders = []
        
        for item in items:
            if os.path.isdir(item):
                folders.append(item)
            else:
                files.append(item)
        
        if folders:
            result += "Folders:\n"
            result += "\n".join(folders)
            result += "\n\n"
        if files:
            result += "Files:\n"
            result += "\n".join(files)
            
        return result
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def write_file(filepath: str, content: str) -> str:
    """Write content to a file. Creates new data.csv file or overwrites existing file"""
    answer = input("Allow write? [y/N]: ").strip().lower()
    
    if answer != "y":
        return "User denied the write operation."
    
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return f"File {filepath} created succesfully"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def read_file(filepath: str) -> str:
    """Read and return the contents of a file at the given filepath"""
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def create_directory(path: str) -> str:
    """Create a new directory at the given path. Can create nested directories"""
    answer = input("Allow create? [y/N]: ").strip().lower()
    
    if answer != "y":
        return "User denied the create operation."

    try:
        os.makedirs(path, exist_ok=True)    # Si el directorio existe, no lo crea.
        return f"Successfully created directory {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"


system_prompt = """
You are a helpful coding assistant that can help users navigate, read and edit files.
    
You have access to four tools:
- list_directory: Show files and folders in a directory
- read_file: Read the contents of a file
- write_file: Create or edit files.
- create_directory: Create new directories (including nested directories)

Be helpful and clear in your responses. When editing files or creating directories, always confirm what changes you made.
"""

agent = create_agent(
    model=llm,
    tools=[list_directory, write_file, read_file, create_directory],
)

# user_input = "Give me the list of files in the current dir"
# user_input = "Create me a csv file with some fake data. Write 3 rows"
# user_input = "Tell me the content of requirements.txt"
user_input = "Create me a hello world Flask app in a directory called hello_flask"

messages = [{"role":"user", "content":user_input}]

ai_message = ""

chunks = agent.stream({"messages":messages}, stream_mode='updates')

for chunk in chunks:
    for step, data in chunk.items():
        if step == 'model':
            msg = data['messages'][-1]
            if msg.tool_calls:
                tool = msg.tool_calls[0]['name']
                message = f"[bold yellow]🔧 Using tool: [/bold yellow][cyan]{tool}[/cyan]"
                console.print(message)
            else:
                ai_message = msg.text
        elif step == 'tools':
            result = data['messages'][-1].content
            result = result if len(result) < 50 else result[:50] + "..."
            console.print(f"🗒️[bold green] Tool result:[/bold green]\n [dim]{result}[/dim]")

markdown_output = Markdown(ai_message)
panel_output = Panel(markdown_output,
                     title="[bold cyan]Assistant Response[/bold cyan]",
                     border_style="blue",
                     padding=(1, 2))
console.print(panel_output)