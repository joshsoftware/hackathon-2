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
            SELECT id, uuid, url, status, result, user_agent, ad_blocker_active, plugin_installed, source, created_at
            FROM events
        """)
        events = cursor.fetchall()

        # Query error_logs table
        cursor.execute("""
            SELECT id, uuid, log, title, status, origin, source, created_at
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
                "p_installed": event[7].split(",") or [],
                "created_at": event[9].isoformat()
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
                "log": log[2],
                "title": log[3],
                "status": log[4],
                "origin": log[5],
                "created_at": log[7].isoformat()
            }
            if log[6] == 'F':
                frontend_logs.append(log_data)
            elif log[6] == 'B':
                backend_logs.append(log_data)

        return {
            "frontend_events": frontend_events,
            "backend_events": backend_events,
            "frontend_logs": frontend_logs,
            "backend_logs": backend_logs
        }

    except Exception as e:
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
                    event_id, reason, insights, fixable, remarks
                ) VALUES (
                    %s, %s, %s, %s, %s
                ) RETURNING id
            """
            
            # Insert into the analysis_error_logs table
            insert_logs_query = """
                INSERT INTO analysis_error_logs (
                    analysis_id, log_id
                ) VALUES (
                    %s, %s
                )
            """

            for analysis in analysis_results:
                # Insert into the analysis table and get the generated ID
                cursor.execute(
                    insert_analysis_query,
                    (
                        analysis["event_id"],
                        analysis["reason"],
                        ", ".join(analysis["insights"]),
                        analysis["fixable"],
                        analysis["remarks"]
                    ),
                )
                result = cursor.fetchone()
                if result is None:
                    raise ValueError("Failed to retrieve analysis ID after insertion.")
                analysis_id = result[0]
                
                # Insert associated logs into the analysis_error_logs table
                log_ids = analysis["logs"]
                processed_logs = [(analysis_id, log_id) for log_id in log_ids]
                
                for processed_log in processed_logs:
                    cursor.execute(
                        insert_logs_query,
                        processed_log,
                    )

            connection.commit()

            #TODO: Update all events and logs included in above analysis
            
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

    if analysis_result["result"]:
        try:
            with psycopg2.connect(DATABASE_URL) as connection:
                insert_analysis_results(analysis_result["result"], connection)
        except Exception as e:
            print(f"Database connection error: {e}")
    print("Process completed.")
    