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