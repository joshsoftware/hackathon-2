DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source_enum') THEN
        CREATE TYPE source_enum AS ENUM ('F', 'B');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_enum') THEN
        CREATE TYPE status_enum AS ENUM ('PENDING', 'PROCESSED');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'events'
    ) THEN
        CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            source source_enum NOT NULL,
            url VARCHAR(255) NOT NULL,
            payload TEXT,
            status status_enum NOT NULL DEFAULT 'PENDING',
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            result result_enum NOT NULL,
            user_agent VARCHAR(255),
            ad_blocker_active BOOLEAN NOT NULL,
            plugin_installed TEXT
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'error_logs'
    ) THEN
        CREATE TABLE error_logs (
            id SERIAL PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            log TEXT,
            title VARCHAR(255),
            status status_enum NOT NULL DEFAULT 'PENDING',
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            source source_enum NOT NULL,
            origin VARCHAR(255)
        );
    END IF;
END $$;
 
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'analysis'
    ) THEN
        CREATE TABLE analysis (
            id SERIAL PRIMARY KEY,
            event_id INT NOT NULL,
            reason VARCHAR(255),
            insights TEXT,
            fixable BOOLEAN DEFAULT FALSE,
            remarks TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            FOREIGN KEY (event_id) REFERENCES events (id)
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'analysis_error_logs'
    ) THEN
        CREATE TABLE analysis_error_logs (
            analysis_id INT NOT NULL,
            log_id INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            PRIMARY KEY (analysis_id, log_id),
            FOREIGN KEY (analysis_id) REFERENCES analysis (id),
            FOREIGN KEY (log_id) REFERENCES error_logs (id)
        );
    END IF;
END $$;

IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'error_logs' AND column_name = 'country'
    ) THEN
        ALTER TABLE error_logs ADD COLUMN country VARCHAR(255);
    END IF;

    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'error_logs' AND column_name = 'city'
    ) THEN
        ALTER TABLE error_logs ADD COLUMN city VARCHAR(255);
    END IF;

    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'error_logs' AND column_name = 'region'
    ) THEN
        ALTER TABLE error_logs ADD COLUMN region VARCHAR(255);
    END IF;
END $$;

IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'country'
    ) THEN
        ALTER TABLE events ADD COLUMN country VARCHAR(255);
    END IF;

    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'city'
    ) THEN
        ALTER TABLE events ADD COLUMN city VARCHAR(255);
    END IF;

    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'region'
    ) THEN
        ALTER TABLE events ADD COLUMN region VARCHAR(255);
    END IF;
END $$;
