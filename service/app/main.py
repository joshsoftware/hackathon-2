from typing import Union

from fastapi import FastAPI

from models.event import EventRequest
from models.log import LogRequest

app = FastAPI()


@app.get("/ping")
def read_ping():
    return {"Hello": "World"}



@app.post("/event")
async def receive_event(event: EventRequest):
    # Handle the received event data (for now, just print it)
    print(event)

    # Return a simple response indicating the event was received
    return {"message": "event received"}


@app.post("/log")
async def log_event(log_request: LogRequest):
    print(log_request)
    # You can access the data from log_request here
    return {"message": "log received"}