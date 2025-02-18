CREATE TABLE IF NOT EXISTS [meta.migrations] (
    id INTEGER PRIMARY KEY,
    migration TEXT NOT NULL,
    mode TEXT NOT NULL,
    applied_at TEXT
);

CREATE TABLE IF NOT EXISTS [sessions] (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    model TEXT NOT NULL,
    created INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS [messages] (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    session_id INTEGER,
    model TEXT NOT NULL, -- tracks the actually used model. only set for assistant for users it should be set to <USER>
    role TEXT NOT NULL,
    created INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Create FTS table for messages
CREATE VIRTUAL TABLE IF NOT EXISTS [fts.messages]
USING fts5(content, session_id);

-- Trigger to insert into fts.messages after a new row is inserted into messages
CREATE TRIGGER IF NOT EXISTS [trigger.messages.ai] AFTER INSERT
ON messages
BEGIN
    INSERT INTO [fts.messages] (rowid, content, session_id)
    VALUES (new.id, new.content, new.session_id);
END;


-- Trigger to update fts.messages when a row in messages is updated
CREATE TRIGGER IF NOT EXISTS [trigger.messages.au] AFTER UPDATE
ON messages
BEGIN
    INSERT INTO [fts.messages] ([fts.messages], rowid, content, session_id)
    VALUES ('delete', old.id),
           (new.id, new.content, new.session_id);
END;

-- Trigger to delete from messages_fts when a row in messages is deleted
CREATE TRIGGER IF NOT EXISTS [trigger.messages.ad] AFTER DELETE
ON messages
BEGIN
    INSERT INTO [fts.messages] ([fts.messages], rowid, content, session_id)
    VALUES ('delete', old.id);
END;


CREATE TABLE  IF NOT EXISTS [images] (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt TEXT NOT NULL,
    revised_prompt TEXT NOT NULL,
    created INTEGER NOT NULL, 
    blob BLOB NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS [fts.images]
USING fts5(name, model, prompt, revised_prompt);

-- Trigger to insert into images_fts after a new row is inserted into images
CREATE TRIGGER IF NOT EXISTS [trigger.images.ai] AFTER INSERT ON images
BEGIN
    INSERT INTO [fts.images] (rowid, name, model, prompt, revised_prompt)
    VALUES (new.id, new.name, new.model, new.prompt, new.revised_prompt);
END;

-- Trigger to update images_fts when a row in images is updated
CREATE TRIGGER IF NOT EXISTS [trigger.images.au] AFTER UPDATE
ON images
BEGIN
    INSERT INTO [fts.images] ([fts.images], rowid, name, model, prompt, revised_prompt)
    VALUES ('delete', old.id),
           (new.id, new.name, new.model, new.prompt, new.revised_prompt);
END;

-- Trigger to delete from images_fts when a row in images is deleted
CREATE TRIGGER IF NOT EXISTS [trigger.images.ad] AFTER DELETE
ON images
BEGIN
    INSERT INTO [fts.images] ([fts.images], rowid, name, model, prompt, revised_prompt)
    VALUES ('delete', old.id);
END;


INSERT INTO [meta.migrations] (migration, mode, applied_at)
VALUES ('init', 'up', datetime('now'));

