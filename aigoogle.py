from langchain_google_genai import ChatGoogleGenerativeAI
from os import environ
from langchainconfig import SYSTEM_INSTRUCTIONS, prompt
gemini_client = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=environ.get("GOOGLE_API_KEY"),
)

async def makeResponseGoogle(question: str, id: str | None = None):
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\nPregunta: {question}"
    res = prompt(
        question=full_prompt,
        llm=gemini_client,
        id=id
    )
    for chunk in res:
        yield chunk