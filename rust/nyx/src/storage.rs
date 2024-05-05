use anyhow::{bail, Result};
use indoc::indoc;
use log::*;
use rusqlite::{params, Connection, Row};
use std::path::{Path, PathBuf};

#[derive(Debug)]
struct Storage {
    db: PathBuf,
}

const NO_PARAMS : () = ();

impl Storage {
    const DDL_SESSIONS: &'static str = indoc! {r#"
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                model TEXT NOT NULL,
                temperature REAL NOT NULL
            );
        "#};

    const DDL_MESSAGES: &'static str = indoc! {r#"
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                role TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                session_id  INTEGER,
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            );
        "#};

    fn init(&self) -> Result<()> {
        debug!("Initializing database ({:?})", self.db);
        let con = Connection::open(&self.db)?;
        con.execute(Self::DDL_SESSIONS, NO_PARAMS)?;
        con.execute(Self::DDL_MESSAGES, NO_PARAMS)?;
        Ok(())
    }

    pub fn new<P: AsRef<Path>>(path: P) -> Result<Self> {
        let storage = Self {
            db: path.as_ref().to_path_buf(),
        };
        storage.init()?;
        Ok(storage)
    }

    pub fn session(&self) -> SessionBuilder {
        SessionBuilder {
            db: self.db.clone(),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Session {
    id: u64,
    name: String,
    model: String,
    temperature: f32,
}

impl Session {
    fn from_row(row: &Row) -> rusqlite::Result<Session> {
        Ok(Self {
            id: row.get(0)?,
            name: row.get(1)?,
            model: row.get(2)?,
            temperature: row.get(3)?,
        })
    }
}

struct SessionBuilder {
    db: PathBuf,
}

impl SessionBuilder {
    pub fn load(&self, id: u64) -> Result<Session> {
        let con = Connection::open(&self.db)?;
        let session: Session = con.query_row(
            "SELECT * FROM sessions WHERE id = ?;",
            params![id],
            Session::from_row,
        )?;
        Ok(session)
    }

    pub fn create(&self, name: &str, model: &str, temperature: f32) -> Result<Session> {
        let con = Connection::open(&self.db)?;
        let id: u64 = con.query_row(
            "SELECT COALESCE(MAX(id), 0) FROM sessions;",
            NO_PARAMS,
            |row| row.get(0),
        )?;

        let session = Session {
            id: id + 1,
            name: name.into(),
            model: model.into(),
            temperature,
        };
        con.execute(
            "INSERT INTO sessions(id, name, model, temperature) VALUES(?, ?, ?, ?);",
            params![session.id, session.name, session.model, session.temperature],
        )?;

        Ok(session)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Once;

    static INIT: Once = Once::new();
    pub fn initialize() {
        INIT.call_once(|| env_logger::init());
    }

    #[test]
    fn init() {
        initialize()
    }

    #[test]
    fn test_a_new_session_can_be_created() -> anyhow::Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.as_ref())?;
        let expected = Session {
            id: 1,
            name: "test-session".into(),
            model: "openai:gpt-4".into(),
            temperature: 1.0,
        };
        let actual = storage
            .session()
            .create("test-session", "openai:gpt-4", 1.0)?;
        assert_eq!(actual, expected);
        Ok(())
    }

    #[test]
    fn test_loading_existing_session() -> anyhow::Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.as_ref())?;
        storage
            .session()
            .create("test-session1", "openai:gpt-4", 1.0)?;
        storage
            .session()
            .create("test-session2", "openai:gpt-4", 0.5)?;

        let expected = Session {
            id: 2,
            name: "test-session2".into(),
            model: "openai:gpt-4".into(),
            temperature: 0.5,
        };
        let actual = storage.session().load(2)?;
        assert_eq!(expected, actual);
        Ok(())
    }

    #[test]
    fn test_loading_non_existing_session_returns_an_error() -> anyhow::Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.as_ref())?;
        let result = storage.session().load(1);
        assert!(result.is_err());
        Ok(())
    }
}
