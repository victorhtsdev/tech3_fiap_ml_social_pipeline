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

CREATE TABLE ml_model (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_version INTEGER,
    model_name VARCHAR,
    model_type VARCHAR,
    model_path TEXT,
    is_recommended BOOLEAN,
    CONSTRAINT uq_model_name_type UNIQUE (model_version, model_name, model_type)
);

CREATE TABLE public.model_metric (
    model_id UUID PRIMARY KEY REFERENCES ml_model(id) ON DELETE CASCADE,
    accuracy REAL,
    macro_f1 REAL,
    weighted_f1 REAL
);

CREATE TABLE public.class_metric (
    model_id UUID REFERENCES ml_model(id) ON DELETE CASCADE,
    class_name TEXT,
    f1_score REAL,
    PRIMARY KEY (model_id, class_name)
);
