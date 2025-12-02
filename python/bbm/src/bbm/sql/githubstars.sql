CREATE TABLE IF NOT EXISTS githubstars (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    homepage TEXT,
    language TEXT,
    license TEXT,
    topics TEXT,
);
