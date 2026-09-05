DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS pipeline_runs;


CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    text_url TEXT UNIQUE NOT NULL,
    image_url TEXT,
    summary TEXT,
    author_name TEXT,
    author_email TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    extracted INT,
    transformed INT,
    valid INT,
    loaded INT,
    error TEXT
);