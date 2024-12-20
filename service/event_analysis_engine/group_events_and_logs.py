import psycopg2
import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from event_analysis_engine import analyse_events_and_logs
from event_analysis_engine import create_prompt

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def fetch_and_process_events() -> Dict[str, List[Dict]]:
    """
    Fetches data from the events and error_logs tables, processes them, and returns
    grouped lists for frontend and backend events and logs.

    Returns:
        Dict[str, List[Dict]]: A dictionary containing lists:
            - frontend_events
            - backend_events
            - frontend_logs
            - backend_logs
    """
    try:
        
        # Connect to the database
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Query events table
        cursor.execute("""
            SELECT uuid, url, result, user_agent, ad_blocker_active, plugin_installed, source
            FROM events
        """)
        events = cursor.fetchall()

        # Query error_logs table
        cursor.execute("""
            SELECT id, uuid, log, source
            FROM error_logs
        """)
        logs = cursor.fetchall()

        # Initialize result lists
        frontend_events = []
        backend_events = []
        frontend_logs = []
        backend_logs = []

        # Process events
        for event in events:
            event_data = {
                "uuid": event[0],
                "url": event[1],
                "success": event[2] == "SUCCESS",
                "user_agent": event[3],
                "ab_active": event[4],
                "p_installed": event[5] or []
            }
            if event[6] == 'F':
                frontend_events.append(event_data)
            elif event[6] == 'B':
                backend_events.append(event_data)

        # Process logs
        for log in logs:
            log_data = {
                "id": log[0],
                "logs": log[2]
            }
            if log[3] == 'F':
                frontend_logs.append(log_data)
            elif log[3] == 'B':
                backend_logs.append(log_data)

        return {
            "frontend_events": frontend_events,
            "backend_events": backend_events,
            "frontend_logs": frontend_logs,
            "backend_logs": backend_logs,
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "frontend_events": [],
            "backend_events": [],
            "frontend_logs": [],
            "backend_logs": [],
        }
    finally:
        cursor.close()
        connection.close()
    

# Main execution
if __name__ == "__main__":
    # Fetch and process data
    data = fetch_and_process_events()

    # Call the create_prompt method with the processed data
    prompt = create_prompt(
        frontend_events=data["frontend_events"],
        backend_events=data["backend_events"],
        frontend_logs=data["frontend_logs"],
        backend_logs=data["backend_logs"]
    )

    # Analyze events and logs
    analysis_result = analyse_events_and_logs(
        frontend_events=data["frontend_events"],
        backend_events=data["backend_events"],
        frontend_logs=data["frontend_logs"],
        backend_logs=data["backend_logs"]
    )

    print("Generated Prompt:")
    print(prompt)
    print("Analysis Result:")
    print(analysis_result)
