from db import cnx
from db_queries import query_flights, query_flights_minutes
from langchain.tools import tool # Esta librería es clave
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
import uuid
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_INSTRUCTIONS = """
Debes indicarle al usuario la duracion del vuelo en horas y minutos, aunque en la base de datos te lo muestras en minutos nada mas...
Si el usuario no especifica pais, entonces preguntale el pais
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
def retrieve_queries_minutes(country: str, rows: int, minutes: int):
    "Retrieve determined number of flights of a departure country filtered by time in minutes"
    print("Ejecutando retreive queries by minutes: " + str(minutes))
    cur = cnx.cursor()
    
    cur.execute(query_flights_minutes(rows), (country, minutes))

    rows_query = cur.fetchall()
    return rows_query

@tool
def retrieve_countries():
    "Retrieve countries from the databases"
    cur = cnx.cursor()
    cur.execute("select distinct country from airport_geo")
    return cur.fetchall()

tools = [retrieve_queries, retrieve_countries, retrieve_queries_minutes]

checkpinter = InMemorySaver()

def prompt(question, llm, id):
    thread_id = id if id else str(uuid.uuid4())

    print('id conversacion ' + thread_id)

    yield 'id: ' + thread_id

    agent = create_agent(
        tools=tools,
        model=llm,
        checkpointer=checkpinter
    )

    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    for token, metadata in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        config=config,
        stream_mode="messages",
    ):
        # Ignora las salidas de herramientas (ToolMessage)
        msg_type = getattr(token, "type", None)
        is_tool_node = isinstance(metadata, dict) and metadata.get("langgraph_node") == "tools"
        if msg_type == "tool" or is_tool_node:
            continue

        text = _extract_text(getattr(token, "content", token))
        if text:
            yield text


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