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