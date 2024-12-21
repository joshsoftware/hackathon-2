from typing import Union

from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse

from models.handler.event import EventRequest
from models.handler.log import LogRequest
from utils.db_helper import execute_query

from utils.response import success_response, error_response
import uvicorn

from EventListner.event_listner import APIEventMiddleware

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
async def log_event(log_request: LogRequest, response: Response):
    """
    Receive a log and insert it into the database.
    """

    insert_query = """
    INSERT INTO error_logs (
        uuid, log, title, source
    ) VALUES (%s, %s, %s, %s);
    """

    #  Convert the log list to a , separated string
    log_request.logs = ",".join(log_request.logs)

    try :
        execute_query(insert_query, (
            log_request.uuid,
            log_request.logs,
            log_request.title,
            log_request.source
        ))
        return success_response(response, "log received", 201)
    except Exception as e:
        return error_response(response, e, 400)

async def log_backend_event(event):
    """
    Log failed events to the backend.
    """

    insert_query = """
    INSERT INTO error_logs (
        uuid, log, title, source
    ) VALUES (%s, %s, %s, %s);
    """

    #  Convert the log list to a , separated string
    event["logs"] = ",".join(event["logs"])

    try :
        execute_query(insert_query, (
            event["uuid"],
            event["logs"],
            event["title"],
            event["source"]
        ))
        print("\n\n Insertion Successfull\n\n")
    except Exception as e:
        print("Error >>>>>>>>>>>>>>> ", e)
    
event_middleware = APIEventMiddleware(failure_callback=log_backend_event)

@app.middleware("http")
async def handle_http_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            await event_middleware.process_exception(request, f"HTTP Error {response.status_code}")
        return response
    except Exception as e:
        await event_middleware.process_exception(request, e)
        return JSONResponse(
            content={"error": "Internal Server Error"},
            status_code=500,
        )        

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
