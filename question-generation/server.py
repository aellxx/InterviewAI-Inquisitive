import os

import sqlite3
from pydantic import BaseModel

import openai

import nest_asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

nest_asyncio.apply()

# Read env file
with open(".env", "r") as f:
    for line in f:
        key, value = line.split("=")
        os.environ[key] = value.strip()

openai.organization = "org-9bUDqwqHW2Peg4u47Psf9uUo"
openai.api_key = os.getenv("OPENAI_API_KEY")


class ReflectionRequestPayload(BaseModel):
    paragraph: str
    prompt: str


class ReflectionResponsePayload(BaseModel):
    response: str


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_file = "requests.db"

with sqlite3.connect(db_file) as conn:
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS requests (timestamp, prompt, paragraph, response)"
    )


async def get_reflections_chat(
    request: ReflectionRequestPayload,
) -> ReflectionResponsePayload:
    # Check if this request has been made before
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM requests WHERE prompt=? AND paragraph=?",
            (request.prompt, request.paragraph),
        )
        result = c.fetchone()

        if result:
            return ReflectionResponsePayload(response=result[3])

    # Else, make the request and cache the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": request.prompt},
            {"role": "user", "content": request.paragraph},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the response
    response_text = response["choices"][0]["message"]["content"]

    # Cache the response
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        # Use SQL timestamp
        c.execute(
            'INSERT INTO requests VALUES (datetime("now"), ?, ?, ?)',
            (request.prompt, request.paragraph, response_text),
        )

    return ReflectionResponsePayload(response=response_text)


@app.post("/reflections")
async def reflections(payload: ReflectionRequestPayload):
    # ! Look at prompt and guidance/jsonformer
    api = "chat"

    if api == "chat":
        return await get_reflections_chat(payload)
    elif api == "completions":
        prompt = (
            """
            You are a writing assistant. Your purpose is to ask the writer helpful and thought-provoking reflections to help them think of how to improve their writing. For each question, include the phrase from the paragraph that it applies to. You must writing your reflections in the following JSON format:

            ```json
                    {
                    "reflections": [
                            {
                                "question": "{{gen 'question'}}",
                                "phrase": "{{gen 'phrase'}}"
                            },
                        ]
                    }
            ```

            Create 5 reflections for the following piece of writing using the JSON format above.
        """
            + payload.paragraph
            + "\n\n ```json \n"
        )

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            echo=True,
        )

    return response["choices"][0]["text"].split("```json")[2]


@app.get("/logs")
async def logs():
    with sqlite3.connect("requests.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM requests")
        result = c.fetchall()

    return result


uvicorn.run(app, port=8000)
