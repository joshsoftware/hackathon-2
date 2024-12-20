import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def apply_migration(migration_file):
    """
    Apply a single migration file.
    """
    try:
        with open(migration_file, 'r') as f:
            migration_query = f.read()
        
        # Connect to the database
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        
        # Execute the migration query
        cursor.execute(migration_query)
        
        # Commit the transaction
        connection.commit()
        print(f"Applied migration: {migration_file}")
        
        # Close connection
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(f"Error applying migration {migration_file}: {e}")
        raise

def apply_all_migrations():
    """
    Apply all migrations in the 'migrations' folder.
    """
    migrations_folder = "migrations"
    
    # Get a list of all migration scripts
    migration_files = sorted([f for f in os.listdir(migrations_folder) if f.endswith(".sql")])
    
    for migration_file in migration_files:
        apply_migration(os.path.join(migrations_folder, migration_file))

if __name__ == "__main__":
    apply_all_migrations()
