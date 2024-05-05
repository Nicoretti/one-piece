use indoc::indoc;
use log::*;
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

struct SessionBuilder {
    db: PathBuf,
}

impl SessionBuilder {
    pub fn new<P: AsRef<Path>>(path: P) -> Result<Self> {
        Ok(Self {
            db: path.as_ref().to_path_buf(),
        })
    }

    pub fn load(&self, id: u64) -> Result<Session> {
        let con = Connection::open(&self.db)?;
        debug!("Loading session ({}) from the database.", id);
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

    fn create(&self, name: &str, model: &str, temperature: f32) -> Result<Session> {
        let con = Connection::open(&self.db)?;
        let mut id = con.query_row("SELECT COALESCE(MAX(id), 0) FROM sessions;", (), |row| {
            row.get(0)
        })?;
        id += 1;

        let session = Session {
            id,
            name: name.into(),
            model: model.into(),
            temperature,
        };

        debug!("Creating new session, details: {:?}", session);
        con.execute(
            "INSERT INTO sessions(id, name, model, temperature) VALUES(?, ?, ?, ?);",
            params![session.id, session.name, session.model, session.temperature],
        )?;

        Ok(session)
    }
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
        debug!("Initializing DB {:?}.", self.db);
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

    pub fn session(&self) -> Result<SessionBuilder> {
        SessionBuilder::new(self.db.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Once;
    static INIT: Once = Once::new();

    pub fn initialize() {
        INIT.call_once(|| {
            env_logger::init();
        });
    }

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
            id: 1,
            name: "test-session".into(),
            model: "openai:gpt-4".into(),
            temperature: 1.0,
        };
        let actual = storage
            .session()?
            .create("test-session", "openai:gpt-4", 1.0)?;

        assert_eq!(actual, expected);
        Ok(())
    }

    #[test]
    fn test_loading_existing_session() -> Result<()> {
        initialize();
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.path())?;
        {
            storage
                .session()?
                .create("test-session1", "openai:gpt-4", 1.0)?;
            storage
                .session()?
                .create("test-session2", "openai:gpt-4", 0.5)?;
        }
        let expected = Session {
            id: 2,
            name: "test-session2".into(),
            model: "openai:gpt-4".into(),
            temperature: 0.5,
        };

        let actual = storage.session()?.load(2)?;

        assert_eq!(expected, actual);
        Ok(())
    }

    #[test]
    fn test_loading_non_existing_session_returns_an_error() -> Result<()> {
        let db = tempfile::Builder::new()
            .prefix("test")
            .suffix(".db")
            .tempfile()?;
        let storage = Storage::new(db.path())?;
        let result = storage.session()?.load(1);

        assert!(result.is_err());
        Ok(())
    }
}
