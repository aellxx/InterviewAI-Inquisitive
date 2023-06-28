from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from nlp import get_questions

app = FastAPI()

# May risk unauthorized access
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


# JSON-like object
class Data(BaseModel):
    paragraph: str
    comment: str


# Memory-based database for now
database: List[Data] = []


# POST method for appending new paragraphs to the database
@app.post("/database")
async def store_data(data: List[str]):
    for d in data:
        if not any(db.paragraph == d for db in database):
            database.append(
                # Generate question when appending
                # This may be an inefficient approach
                Data(paragraph=d, comment=get_questions(sequence=d, num_questions=1)[0])
            )


# GET method for retrieving the database
@app.get("/database")
async def get_data() -> List[Data]:
    return database
