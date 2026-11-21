from langchain_google_genai import ChatGoogleGenerativeAI
from os import environ
from langchainconfig import prompt

gemini_client = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=environ.get("GOOGLE_API_KEY")
)

async def makeResponseGoogle(question: str):
    yield prompt(question=question, llm=gemini_client)