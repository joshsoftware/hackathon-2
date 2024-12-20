from typing import Union

from fastapi import FastAPI, Response

from models.handler.event import EventRequest
from models.handler.log import LogRequest
from utils.db_helper import execute_query

from utils.response import success_response, error_response

app = FastAPI()


@app.get("/ping")
def read_ping():
    query = "SELECT 1"  # Simple query to check if the DB is responsive
    result = execute_query(query)
    return {"ping": "pong", "result": result}





@app.post("/event")
async def receive_event(event: EventRequest,response: Response):
    """
    Receive an event and insert it into the database.
    """


    insert_query = """
    INSERT INTO events (
        uuid, source, url, payload,  result,
        user_agent, ad_blocker_active, plugin_installed
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    # convert the payload to a string
    event.payload = str(event.payload)

    # convert the plugin_installed list to a string separated by commas
    event.p_installed = ",".join(event.p_installed) if event.p_installed else None

    try:
        execute_query(insert_query, (
            event.uuid,
            event.source,
            event.url,
            event.payload,
            event.result,
            event.user_agent,
            event.ab_active,
            event.p_installed
        ))
        return success_response(response, "event received", 201)
    except Exception as e:
        return error_response(response, e, 400)


@app.post("/log")
async def log_event(log_request: LogRequest):
    print(log_request)
    # You can access the data from log_request here
    return {"message": "log received"}