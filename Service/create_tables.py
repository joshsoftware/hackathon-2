import psycopg2
from urllib.parse import urlparse
import configparser

def load_config():
    """Load database configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["database"]["url"]

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TYPE source_enum AS ENUM ('F', 'B');
        CREATE TYPE status_enum AS ENUM ('pending', 'processed');
        CREATE TYPE result_enum AS ENUM ('success', 'failed');
        """,
        """
        CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            source source_enum NOT NULL,
            url VARCHAR(255) NOT NULL,
            payload TEXT,
            status status_enum NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            result result_enum NOT NULL,
            user_agent VARCHAR(255),
            ad_blocker_active BOOLEAN NOT NULL,
            plugin_installed VARCHAR(255)
        );
        """,
        """
        CREATE TABLE error_logs (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            log TEXT,
            title VARCHAR(255),
            status status_enum NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            source source_enum NOT NULL
        );
        """,
        """
        CREATE TABLE analysis (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            event_id INT NOT NULL,
            insights VARCHAR(255),
            fixable BOOLEAN DEFAULT FALSE,
            remarks TEXT,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events (id)
        );
        """
    )

    db_url = load_config()
    parsed_url = urlparse(db_url)

    db_config = {
        "dbname": parsed_url.path[1:],  
        "user": parsed_url.username,
        "password": parsed_url.password,
        "host": parsed_url.hostname,
        "port": parsed_url.port,
        "sslmode": "require",
    }

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)   
                conn.commit()   
        print("Tables created successfully")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")

if __name__ == '__main__':
    create_tables()