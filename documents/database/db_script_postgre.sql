CREATE TABLE ml_execution (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    search VARCHAR NOT NULL,
    date TIMESTAMP NOT NULL,
    classification_model_version INTEGER NULL,
    classification_model_name VARCHAR NULL,
    classification_model_type VARCHAR NULL,
    date_ranges TEXT NULL 
);

CREATE TABLE content (
    exec_id UUID NOT NULL, 
    content_id INTEGER NOT NULL, 
    content TEXT NOT NULL,
    source VARCHAR NOT NULL,
    url VARCHAR,
    user_id VARCHAR NOT NULL,
    user_id2 VARCHAR NOT NULL,
    date_posted TIMESTAMP NOT NULL,
    PRIMARY KEY (exec_id, content_id) 
);

CREATE TABLE pipeline_log (
    id UUID DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP DEFAULT NOW(),
    stage VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    details TEXT,
	PRIMARY KEY (id,timestamp) 
);
	
CREATE TABLE ml_clusters (
    exec_id UUID NOT NULL,
    cluster INTEGER NOT NULL,
    topic TEXT,
    pattern_found TEXT,
    keyword TEXT,
    conclusion TEXT,
    is_consistent BOOLEAN,
    record_count INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (exec_id, cluster),
    FOREIGN KEY (exec_id) REFERENCES ml_execution(id) ON DELETE CASCADE
);

CREATE TABLE content_processed (
    exec_id UUID NOT NULL, 
    content_id INTEGER NOT NULL, 
    processed_id INTEGER NOT NULL, 
    sentence TEXT,
    embeddings BYTEA,
    label VARCHAR, 
    sentiment VARCHAR,  
    PRIMARY KEY (exec_id, content_id, processed_id)
);