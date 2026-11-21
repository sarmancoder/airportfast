from db import cnx
from db_queries import query_flights
from langchain.tools import tool # Esta librería es clave
from langchain.agents import create_agent

@tool
def retrieve_queries(country: str, rows: int):
    "Retrieve determined number of flights of a departure country"
    print("Ejecutando retreive queries")
    cur = cnx.cursor()
    
    cur.execute(query_flights(rows), (country,))

    rows_query = cur.fetchall()
    return rows_query

tools = [retrieve_queries]

def prompt(question, llm):
    agent = create_agent(
        tools=tools,
        model=llm
    )

    # 3. Crear el Executor: Este es el motor que ejecuta el plan
    res = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return _extract_text(res["messages"][-1].content)


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