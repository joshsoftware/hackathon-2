CREATE TYPE source_enum AS ENUM ('F', 'B');
CREATE TYPE status_enum AS ENUM ('PENDING', 'PROCESSED');
CREATE TYPE result_enum AS ENUM ('SUCCESS', 'FAILED');

CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            source source_enum NOT NULL,
            url VARCHAR(255) NOT NULL,
            payload TEXT,
            status status_enum NOT NULL DEFAULT 'PENDING',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            result result_enum NOT NULL,
            user_agent VARCHAR(255),
            ad_blocker_active BOOLEAN NOT NULL,
            plugin_installed VARCHAR(255)
);

CREATE TABLE error_logs (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            log TEXT,
            title VARCHAR(255),
            status status_enum NOT NULL DEFAULT 'PENDING',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            source source_enum NOT NULL,
            origin VARCHAR(255)
);

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