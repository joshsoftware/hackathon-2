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