from database import get_db_connection

def execute_query(query, params=None):
    """
    Execute a query on the database.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()  # Return rows for SELECT queries
            connection.commit()  # Commit changes for INSERT/UPDATE/DELETE
    except Exception as e:
        connection.rollback()
        print(f"Error executing query: {e}")
        raise
    finally:
        connection.close()