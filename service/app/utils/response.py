
from fastapi import  Response

# Function to handle success response
def success_response(response: Response, message: str, status_code: int):
    response.status_code = status_code
    return {"message": message}

# Function to handle failure response
def error_response(response: Response, error_message: str, status_code:int):
    response.status_code = status_code
    return {"error": f"Failed to insert event: {error_message}"}