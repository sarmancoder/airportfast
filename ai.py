from openai import AsyncOpenAI
from os import environ
from dotenv import load_dotenv
import logging

load_dotenv()

openai_client = AsyncOpenAI(
  api_key=environ.get("OPENAI_API_KEY"),
)

async def makeReseponse(question: str):
    response = await openai_client.responses.create(
        model="gpt-4o-mini",
        input=question,
        stream=True
    )

    async for event in response:
        if event.type == "response.output_text.delta":
            text = event.delta
            yield f"{text}"
        if event.type == "response.completed":
            total_tokens = event.response.usage.total_tokens
            logging.info(f"Used tokens: {total_tokens}")
 
    yield "event: end\ndata: [END]\n\n"