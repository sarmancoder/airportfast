from db import cnx
from db_queries import query_flights
from langchain.tools import tool # Esta librería es clave
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
import uuid

SYSTEM_INSTRUCTIONS = """
Si es que el pais que te ha pedido no lo encuentras, entonces entragale una lista completa de paises al usuario
Si simplemente te llega el nombre de un pais, entonces quiero que respondas con los vuelos desde ese pais
Debes indicarle al usuario la duracion del vuelo en horas y minutos, aunque en la base de datos te lo muestras en minutos nada mas...
Los vuelos quiero que los devuelvas enumerados
"""

@tool
def retrieve_queries(country: str, rows: int):
    "Retrieve determined number of flights of a departure country"
    print("Ejecutando retreive queries")
    cur = cnx.cursor()
    
    cur.execute(query_flights(rows), (country,))

    rows_query = cur.fetchall()
    return rows_query

@tool
def retrieve_countries():
    "Retrieve countries from the databases"
    cur = cnx.cursor()
    cur.execute("select distinct country from airport_geo")
    return cur.fetchall()

tools = [retrieve_queries, retrieve_countries]

def prompt(question, llm, id):
    thread_id = id if id else str(uuid.uuid4())

    yield 'id: ' + thread_id

    agent = create_agent(
        tools=tools,
        model=llm
    )

    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    res = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config,
    )
    yield _extract_text(res["messages"][-1].content)


def _extract_text(content: str | list) -> str:
    """Extrae texto limpio tanto si content es str como si es lista de bloques."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        return "".join(parts)
    return str(content)