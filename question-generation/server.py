import os

import sqlite3
from pydantic import BaseModel

import openai

import nest_asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json

from typing import List

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


class ReflectionResponseItem(BaseModel):
    text_in_HTML_format: str
    sentence_number_in_paragraph: int
    quality: float

class ReflectionResponses(BaseModel):
    reflections: List[ReflectionResponseItem]


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
        "CREATE TABLE IF NOT EXISTS requests (timestamp, prompt, paragraph, response, success)"
    )

def sanitize(text):
    return text.replace('"', '').replace("'", "")



async def get_reflections_chat(
    request: ReflectionRequestPayload,
) -> ReflectionResponses:
    # Check if this request has been made before
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT response FROM requests WHERE prompt=? AND paragraph=? AND success='true'",
            (request.prompt, request.paragraph),
        )
        result = c.fetchone()

        if result:
            response_json = result[0]
            response = json.loads(response_json)
            # assume that the database stores only valid responses in the correct schema.
            # We check this below.
            return ReflectionResponses(**response)

    # Else, make the request and cache the response

    # TODO: improve the "quality" mechanism
    desired_schema_prompt = '''
    {
            "text_in_HTML_format": str,
            "sentence_number_in_paragraph": int,
            "quality": float
    }
    '''

    prompt = request.prompt + '''
Respond as a JSON array. Each item should have the following schema:
''' + desired_schema_prompt


    # TODO: Rate limit these requests.
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": sanitize(request.paragraph)},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the response
    response_text = response["choices"][0]["message"]["content"]

    # Attempt to parse JSON
    try:
        response_json = json.loads(response_text)
        assert isinstance(response_json, list)
        reflection_items = ReflectionResponses(**json.loads(response_json))
    except Exception as e1:
        # Ask the LM to fix the JSON.
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "The JSON should be an array of items with the following schema:\n\n" + desired_schema_prompt},
                {"role": "user", "content": response_text},
            ],
            temperature=.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        new_response = response["choices"][0]["message"]["content"]

        # Try to parse again
        try:
            response_json = json.loads(new_response)
            assert isinstance(response_json, list)
            reflection_items = ReflectionResponses(**json.loads(response_json))
        except Exception as e2:
            # If it still doesn't work, log the error and fail out
            with sqlite3.connect(db_file) as conn:
                c = conn.cursor()
                # Use SQL timestamp
                c.execute(
                    'INSERT INTO requests VALUES (datetime("now"), ?, ?, ?, ?)',
                    (request.prompt, request.paragraph, json.dumps(dict(
                        error=str(e2), 
                        response=response_text
                    )), "false"),
                )
            raise e2

    # Cache the response
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        # Use SQL timestamp
        c.execute(
            'INSERT INTO requests VALUES (datetime("now"), ?, ?, ?, ?)',
            (request.prompt, request.paragraph, json.dumps(reflection_items.dict()), "true"),
        )

    return reflection_items


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
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM requests")
        result = c.fetchall()

    return result

uvicorn.run(app, port=8000)
