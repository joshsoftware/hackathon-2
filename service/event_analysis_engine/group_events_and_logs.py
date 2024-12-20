import psycopg2
import os
from typing import Dict, List
from dotenv import load_dotenv
from event_analysis_engine import analyse_events_and_logs

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
            SELECT id, uuid, url, status, result, user_agent, ad_blocker_active, plugin_installed, source
            FROM events
        """)
        events = cursor.fetchall()

        # Query error_logs table
        cursor.execute("""
            SELECT id, uuid, log, status, source, origin
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
                "id": event[0],
                "uuid": event[1],
                "url": event[2],
                "status": event[3],
                "result": event[4] == "SUCCESS",
                "user_agent": event[5],
                "ab_active": event[6],
                "p_installed": event[7] or []
            }
            if event[8] == 'F':
                frontend_events.append(event_data)
            elif event[8] == 'B':
                backend_events.append(event_data)

        # Process logs
        for log in logs:
            log_data = {
                "id": log[0],
                "uuid": log[1],
                "logs": log[2],
                "status": log[3],
                "origin": log[5]
            }
            if log[4] == 'F':
                frontend_logs.append(log_data)
            elif log[4] == 'B':
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
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_analysis_results(analysis_results: List[Dict], connection):
    """
    Inserts analysis results into the analysis and analysis_error_logs tables.

    Args:
        analysis_results (List[Dict]): List of analysis results to insert.
        connection: Active database connection.
    """
    try:
        with connection.cursor() as cursor:
            # Insert into the analysis table
            insert_analysis_query = """
                INSERT INTO analysis (
                    event_id, insights, fixable, remarks, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, NOW(), NOW()
                ) RETURNING id
            """

            # Insert into the analysis_error_logs table
            insert_logs_query = """
                INSERT INTO analysis_error_logs (
                    analysis_id, log_id
                ) VALUES (%s, %s)
            """

            for analysis in analysis_results:
                # Insert into the analysis table and get the generated ID
                cursor.execute(
                    insert_analysis_query,
                    (
                        analysis.get("event_id"),
                        ", ".join(analysis.get("insights", [])),
                        analysis.get("fixable", False),
                        analysis.get("remarks", ""),
                    ),
                )
                analysis_id = cursor.fetchone()[0]

                # Insert associated logs into the analysis_error_logs table
                log_ids = analysis.get("logs", [])
                log_values = [(analysis_id, log_id) for log_id in log_ids]
                execute_batch(cursor, insert_logs_query, log_values)

            connection.commit()
            print(f"{len(analysis_results)} analysis results inserted successfully.")

    except Exception as e:
        print(f"Error inserting analysis results: {e}")
        connection.rollback()

# Main execution
if __name__ == "__main__":

    data = fetch_and_process_events()
    if not data:
        print("No data fetched. Exiting.")
        exit(1)

    # Analyze events and logs
    analysis_result = analyse_events_and_logs(
        frontend_events=data["frontend_events"],
        backend_events=data["backend_events"],
        frontend_logs=data["frontend_logs"],
        backend_logs=data["backend_logs"],
    )

    if analysis_result and "result" in analysis_result:
        try:
            with psycopg2.connect(DATABASE_URL) as connection:
                insert_analysis_results(analysis_result["result"], connection)
        except Exception as e:
            print(f"Database connection error: {e}")
    print("Process completed.")
    