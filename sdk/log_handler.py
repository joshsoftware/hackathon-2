import logging
import time
import requests
import uuid  # For generating unique UUIDs


# Custom Log Handler
class APILogHandler(logging.Handler):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    def emit(self, record):
        try:
            # Only send ERROR level logs to the API
            if record.levelname != "ERROR":
                return

            # Format the log message
            log_message = self.format(record)

            # Generate a unique UUID
            unique_uuid = str(uuid.uuid4())

            # Prepare payload
            payload = {
                "uuid": unique_uuid,
                "logs": [log_message],
                "source": "B"  # Backend source
            }

            # Send log to API
            response = requests.post(f"{self.api_url}/log", json=payload)

            # Check API response
            if response.status_code != 201:
                print(f"Failed to send log to API: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error in sending log to API: {e}")
        except Exception as e:
            print(f"Error in emitting log: {e}")


# Function to simulate log generation every 5 seconds
def generate_logs():
    # API endpoint (update this with your actual API endpoint)
    api_url = "http://127.0.0.1:8000"

    # Create a logger
    logger = logging.getLogger("RealTimeLogger")
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to log all levels

    # Add the custom log handler to the logger
    api_log_handler = APILogHandler(api_url)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    api_log_handler.setFormatter(formatter)
    logger.addHandler(api_log_handler)

    # Add a StreamHandler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Generate logs every 5 seconds
    try:
        while True:
            logger.info("This is an info log message.")  # Only printed to console
            logger.debug("This is a debug log message.")  # Only printed to console
            logger.error("This is an error log message.")  # Printed and sent to API
            time.sleep(5)  # Wait for 5 seconds before generating the next log
    except KeyboardInterrupt:
        print("Log generation stopped.")


# Run the log generator
if __name__ == "__main__":
    generate_logs()
