use indoc::indoc;
use std::path::{Path, PathBuf};

use anyhow::{bail, Result};
use rusqlite::{params, Connection};

#[derive(Debug)]
struct Storage {
    db: PathBuf,
}

#[derive(Debug, PartialEq)]
struct Session {
    id: u64,
    name: String,
    model: String,
    temperature: f32,
}

impl Storage {
    const DDL_SESSIONS: &'static str = indoc! {
    r#"
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                model TEXT NOT NULL,
                temperature REAL NOT NULL
            );
        "#};

    const DDL_MESSAGES: &'static str = indoc! {
        r#"
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                role TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                session_id  INTEGER,
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            );
        "#
    };

    fn init(&self) -> Result<()> {
        let con = Connection::open(&self.db)?;
        con.execute(Storage::DDL_SESSIONS, ())?;
        con.execute(Storage::DDL_MESSAGES, ())?;
        Ok(())
    }

    pub fn new<P: AsRef<Path>>(path: P) -> Result<Self> {
        let storage = Self {
            db: path.as_ref().to_path_buf(),
        };
        if let Err(e) = storage.init() {
            bail!("Could not initialize DB: {}", e);
        }
        Ok(storage)
    }

    pub fn session(&self, id: Option<u64>) -> Result<Session> {
        let con = Connection::open(&self.db)?;

        fn create(con: &Connection) -> Result<Session> {
            let id = con
                .query_row("SELECT MAX(id) FROM sessions;", (), |row| {
                    row.get(0)
                })
                .unwrap_or(0u64);

            let session = Session {
                id,
                name: "test-session".into(),
                model: "openai:gpt-4".into(),
                temperature: 1.0,
            };

            con.execute(
                "INSERT INTO sessions(id, name, model, temperature) VALUES(?, ?, ?, ?);",
                params![session.id, session.name, session.model, session.temperature]
            )?;

            Ok(session)
        }

        fn load(con: &Connection, id: u64) -> Result<Session> {
            Ok(
                con.query_row("SELECT * FROM sessions WHERE id = ?;", (id,), |row| {
                    Ok(Session {
                        id: row.get(0)?,
                        name: row.get(1)?,
                        model: row.get(2)?,
                        temperature: row.get(3)?,
                    })
                })?,
            )
        }

        match id {
            Some(id) => load(&con, id),
            None => create(&con),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_new_storage() -> Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;

        Storage::new(db.path())?;

        let con = Connection::open(db.path()).expect("Could not open DB.");
        let res = con.execute("SELECT * FROM sessions;", ());

        assert!(res.is_ok());
        Ok(())
    }

    #[test]
    fn test_a_new_session_can_be_created() -> Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.path())?;

        let expected = Session {
            id: 0,
            name: "test-session".into(),
            model: "openai:gpt-4".into(),
            temperature: 1.0,
        };
        let actual = storage.session(None)?;

        assert_eq!(actual, expected);
        Ok(())
    }

    #[test]
    fn test_loading_non_existing_session_returns_an_error() -> Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.path())?;

        let result = storage.session(Some(1));

        assert!(result.is_err());
        Ok(())
    }
}
