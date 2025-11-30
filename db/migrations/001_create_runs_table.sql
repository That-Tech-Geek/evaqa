CREATE TABLE IF NOT EXISTS runs (
    run_id UUID PRIMARY KEY,
    founder_email VARCHAR(255) NOT NULL,
    startup_name VARCHAR(255) NOT NULL,
    workflow_status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    votes JSONB,
    verdict VARCHAR(50),
    memo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
