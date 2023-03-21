import openai
import os
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseSettings

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY)")


class Settings(BaseSettings):
    OPENAI_API_KEY: str = OPENAI_API_KEY

    class Config:
        env_file = '.env'


settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index(request: Request, animal: str = Form(...)):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_prompt(animal),
        temperature=0.6,
    )
    result = response.choices[0].text
    return templates.TemplateResponse("index.html", {"request": request, "result": result})


@app.get("/chat", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_class=HTMLResponse)
async def index(request: Request, animal: str = Form(...)):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generate_prompt2(animal)
    )
    result2 = response['choices'][0]['message']['content']
    return templates.TemplateResponse("index.html", {"request": request, "result2": result2})


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.
Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


def generate_prompt2(animal):
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work

    return [
        {"role": "system", "content": "You are a helpful assistant that translates English to French."},
        {"role": "user", "content": f'Translate the following English text to French: f"{animal}"'}
    ]


if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)
