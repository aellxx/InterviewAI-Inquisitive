#!/usr/bin/env python3

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend import get_contexts_and_questions

app = FastAPI()


@app.get("/generate")
async def generate_json():
    data = [{"context": "", "question": ""}]
    return JSONResponse(content=data)


if __name__ == "__main__":
    # Test server at: https://dev0.kenarnold.org/generate
    uvicorn.run(app, host="0.0.0.0", port=5000)
