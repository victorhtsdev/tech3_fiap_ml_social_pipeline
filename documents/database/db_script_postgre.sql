CREATE TABLE ml_executions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    version VARCHAR NOT NULL
);

CREATE TABLE content (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR NOT NULL,
    date_posted TIMESTAMP,
    cluster_id INTEGER,
    embeddings BYTEA,
    user_id VARCHAR
);

CREATE TABLE pipeline_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    stage VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    details TEXT
);

