from langchain_google_genai import ChatGoogleGenerativeAI
from os import environ
from langchainconfig import SYSTEM_INSTRUCTIONS, prompt
from langchain_core.messages import HumanMessage, SystemMessage
import uuid
gemini_client = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=environ.get("GOOGLE_API_KEY"),
)

async def makeResponseGoogle(question: str, id: str | None = None):
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\nPregunta: {question}"
    thread_id = id if id else str(uuid.uuid4())
    print("id generado " + thread_id)
    yield f"id: {thread_id}"
    res = prompt(
        question=full_prompt,
        llm=gemini_client,
        thread_id=thread_id
    )
    yield res