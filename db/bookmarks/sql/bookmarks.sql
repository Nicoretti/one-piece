CREATE TABLE IF NOT EXISTS 'bookmarks.web'
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    url         TEXT NOT NULL UNIQUE,
    title       TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    tags        TEXT NOT NULL DEFAULT ''
);

CREATE VIRTUAL TABLE IF NOT EXISTS 'bookmarks.web.fts' USING fts5
(
    url,
    title,
    description,
    tags,
    content='bookmarks.web',
    content_rowid='id',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE TRIGGER IF NOT EXISTS 'bookmarks.web.trigger_after_insert'
    AFTER INSERT
    ON 'bookmarks.web'
BEGIN
    INSERT INTO 'bookmarks.web.fts'(rowid, url, title, description, tags)
    VALUES (new.id, new.url, new.title, new.description, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS 'bookmarks.web.trigger_after_delete'
    AFTER DELETE
    ON 'bookmarks.web'
BEGIN
    INSERT INTO 'bookmarks.web.fts'('bookmarks.web.fts', rowid, url, title, description, tags)
    VALUES ('delete', old.id, old.url, old.title, old.description, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS 'bookmarks.web.trigger_after_update'
    AFTER UPDATE
    ON 'bookmarks.web'
BEGIN
    INSERT INTO 'bookmarks.web.fts'('bookmarsk.web.fts', rowid, url, title, description, tags)
    VALUES ('delete', old.id, old.url, old.title, old.description, old.tags);

    INSERT INTO 'bookmarks.web.fts'(rowid, url, title, description, tags)
    VALUES (new.id, new.url, new.title, new.description, new.tags);
END;


