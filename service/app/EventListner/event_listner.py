# Description: Middleware to log failed API events. 
from datetime import datetime
import logging

class APIEventMiddleware:
    def __init__(self, failure_callback=None):
        """
        Initialize the middleware with a user-defined failure callback.

        Args:
            failure_callback (function): A user-defined function to handle failed API events.
        """
        self.failure_callback = failure_callback
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger(__name__)

    async def process_exception(self, request, exception):
        """
        Handle exceptions during API calls.

        Args:
            request: FastAPI request object.
            exception: The exception that occurred.
        """
        event = {
            "uuid": request.headers.get("uuid") or datetime.now().isoformat(),
            "logs": [f"Server error: {exception} - Path: {request.url.path}"],
            "title": "Server error",
            "source": "B",
            "status_code": 500,
        }
        self.logger.error(f"Failed API Event: {event}")

        # Trigger the user-defined callback if set
        if self.failure_callback:
            await self.failure_callback(event)
