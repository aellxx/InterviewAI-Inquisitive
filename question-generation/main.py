from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from nlp import get_questions

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



@app.get("/generate")
async def generate_json():
    return json.loads(open("demo-data.json").read())
    #contexts, questions = get_contexts_and_questions("context.txt")
    #data = [{"context": c, "question": q} for c in contexts for q in questions]
    #data = {"context": "context", "question": "question"}
    #return dict(content=data)


if __name__ == "__main__":
    # Test server at: https://dev<X>.kenarnold.org/generate
    uvicorn.run(app, host="0.0.0.0", port=int(sys.argv[1]))
