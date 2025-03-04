CREATE TABLE ml_execution (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    search VARCHAR NOT NULL,
    date TIMESTAMP NOT NULL,
    version INTEGER NOT NULL
);

CREATE TABLE content (
    id UUID DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    source VARCHAR NOT NULL,
    url VARCHAR,
    user_id VARCHAR NOT NULL,
	user_id2 VARCHAR NOT NULL,
    date_posted TIMESTAMP NOT NULL,
    cluster_id INTEGER,
    embeddings BYTEA,
    PRIMARY KEY (id, source, user_id,user_id2, date_posted) 
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
