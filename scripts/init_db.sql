CREATE TABLE IF NOT EXISTS raw_leads (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    source VARCHAR,
    company_name VARCHAR,
    domain VARCHAR,
    employee_count INTEGER,
    industry VARCHAR,
    job_title VARCHAR,
    estimated_revenue DOUBLE PRECISION,
    uses_salesforce BOOLEAN DEFAULT FALSE,
    is_b2b_from_llm BOOLEAN,
    score INTEGER,
    has_been_routed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_raw_leads_email ON raw_leads(email);
