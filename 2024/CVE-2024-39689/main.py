from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"isHealthy": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
