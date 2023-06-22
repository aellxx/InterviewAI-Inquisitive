#!/usr/bin/env python3

import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend import get_contexts_and_questions

app = FastAPI()


@app.get("/generate")
async def generate_json():
    contexts, questions = get_contexts_and_questions("context.txt")
    data = [{"context": c, "question": q} for c in contexts for q in questions]
    return JSONResponse(content=data)


if __name__ == "__main__":
    # Test server at: https://dev<X>.kenarnold.org/generate
    uvicorn.run(app, host="0.0.0.0", port=int(sys.argv[1]))
