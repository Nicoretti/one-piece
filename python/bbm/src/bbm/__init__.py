import sqlite3
from pathlib import Path
from typing import Optional
from loguru import logger
import importlib.resources as resources
import sqlglot


def main() -> None:
    initalize()


def bbm_db() -> Path:
    return Path.home() / ".bbm.sqlite"


def initalize(db: Path = None):
    db = db or bbm_db()
    if not db.exists():
        logger.info(f"Creating database at: {db}")

    with sqlite3.connect(db) as con:
        for file in resources.files("bbm.sql").iterdir():
            sql = file.read_text()
            stmt = sqlglot.transpile(sql, read="postgres", write="sqlite", pretty=True)[0]
            logger.debug(f"SQL:\n{stmt}")
            con.execute(stmt)
