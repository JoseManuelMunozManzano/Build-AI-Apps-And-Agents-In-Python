from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

query = "coffee health benefits"

tavily_search = TavilySearch(
    max_results=5,
    topic="news",   # Puede tener tres valores: news, general, finance
    search_depth="basic",    # basic gasta 1 credit y advanced gasta 2, pero Tavily piensa más.
    time_range="week",   # Obtenemos páginas web publicadas en la última semana. Otro valor es day
    include_raw_content=False,  # False significa que no nos de la página web completa, solo el resumen.
    include_answer=True,    # Por defecto es False. Con True obtenemos un resumen de las páginas web.
)

results = tavily_search.invoke(query)
pprint(results)
