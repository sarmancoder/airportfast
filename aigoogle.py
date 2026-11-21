from httpx2 import query
from langchain_google_genai import ChatGoogleGenerativeAI
from os import environ
from db import cnx
from db_queries import query_flights

gemini_client = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=environ.get("GOOGLE_API_KEY")
)

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

async def makeResponseGoogle(question: str):
    cur = cnx.cursor()

    cur.execute(query_flights(10), ("UNITED STATES",))

    rows = cur.fetchall()
    print(rows[0])
    print(len(rows))

    cur.close()

    async for res in gemini_client.astream(question):
        text = _extract_text(res.content)
        yield text