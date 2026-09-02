
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    author TEXT,
    category TEXT,
    is_politics_related BOOLEAN NOT NULL
);