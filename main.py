from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from asyncio import sleep
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class QuestionBody(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

async def makeReseponse(question: str):
    yield "# Pregunta hecha"
    await sleep(3)
    yield " * " + question

@app.post("/question")
async def question(body: QuestionBody):
    return StreamingResponse(makeReseponse(body.question))