from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def read_ping():
    return {"Hello": "World"}

