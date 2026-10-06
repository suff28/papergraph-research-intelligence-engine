CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    year INTEGER NOT NULL,
    venue TEXT NOT NULL,
    doi TEXT,
    url TEXT,
    domain TEXT NOT NULL,
    task TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    author_name TEXT NOT NULL,
    author_order INTEGER NOT NULL,
    PRIMARY KEY (paper_id, author_name)
);

CREATE TABLE IF NOT EXISTS extracted_entities (
    entity_id BIGSERIAL PRIMARY KEY,
    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    entity_type TEXT NOT NULL,
    entity_value TEXT NOT NULL,
    confidence NUMERIC(4,3) NOT NULL DEFAULT 1.0
);

CREATE TABLE IF NOT EXISTS paper_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC(10,4) NOT NULL,
    dataset TEXT
);

CREATE TABLE IF NOT EXISTS paper_edges (
    edge_id BIGSERIAL PRIMARY KEY,
    source_paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    target_paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    weight NUMERIC(6,4) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_entities_value ON extracted_entities(entity_value);
CREATE INDEX IF NOT EXISTS idx_papers_task ON papers(task);
CREATE INDEX IF NOT EXISTS idx_papers_domain ON papers(domain);
