SELECT title, url, description, tags FROM [bookmarks.web.fts] WHERE [bookmarks.web.fts] MATCH :query;
