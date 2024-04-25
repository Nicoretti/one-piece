import argparse
import json
import sqlite3
import sys
from pathlib import Path
from inspect import cleandoc
from typing import List


def _initalize(path: Path) -> Path:
    with sqlite3.connect(path) as con:
        query = cleandoc("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            data BLOB,
            tags JSON,
            description TEXT
        );""")
        con.execute(query)
    return path


def _store(db: Path, file: Path, description: str, tags: List[str], *args, **kwargs):
    if not db.exists():
        print(f"Initalizing database [{db}]", file=sys.stderr)
        _ = _initalize(db)
    with sqlite3.connect(db) as con:
        query = cleandoc("""
            INSERT INTO files (name, data, tags, description)
            VALUES (?, ?, ?, ?)
        """)
        with open(file, 'rb') as f:
            data = f.read()
            tags = json.dumps(tags)
            con.execute(query, (file.name, data, tags, description))


def _export(db: Path, id: int, path: Path | None, *args, **kwargs) -> Path:
    with sqlite3.connect(db) as con:
        query = cleandoc("""
            SELECT id, name, data FROM files WHERE id = ?;
        """)
        _, name, data = con.execute(query, (id,)).fetchone()
        if path is None:
            destination = Path.cwd() / name
        else:
            destination = path / name if path.is_dir() else path
        with open(destination, 'wb') as f:
            f.write(data)

        return destination


def _search(db: Path, fts: str | None, tags: str | None, *args, **kwargs):
    pass


def _create_parser():
    parser = argparse.ArgumentParser(prog='docbox')
    default_db = Path().home() / '.docbox.db'
    parser.add_argument('--db', default=default_db, type=Path)
    subcommands = parser.add_subparsers(dest='command', help='sub-command help')

    # Create the parser for the "store" command
    store = subcommands.add_parser('store', help='store help')
    store.add_argument('file', type=Path, help='Path to the file to store')
    store.add_argument('--tags', type=str, default=[], help='Tags for the file')
    store.add_argument('--description', type=str, help='Description of the file')
    store.set_defaults(func=_store)

    # Create the parser for the "export" command
    export = subcommands.add_parser('export', help='export help')
    export.add_argument('id', type=int, help='id of the file to export')
    export.add_argument('--path', type=Path, help="""
    If it is a path the orignal file name will be used and written to the path.
    If it is a file path the file will be exported to this file.
    If nothing is specified the orignal name will be exported to the current directory
    """)
    export.set_defaults(func=_export)

    # Create the parser for the "search" command
    search = subcommands.add_parser('search', help='search help')
    group = search.add_mutually_exclusive_group()
    group.add_argument('--fts', type=str, help='full text search')
    group.add_argument('--tag', type=str, help='tag based search')
    search.set_defaults(func=_search)

    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()
    args.func(**vars(args))


if __name__ == '__main__':
    main()
