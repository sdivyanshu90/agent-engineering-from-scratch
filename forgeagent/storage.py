"""Week 2: owner-scoped document state, short transactions, per-call connections."""
from contextlib import closing
from pathlib import Path
import sqlite3


class DocumentStore:
    def __init__(self, path: Path):
        self.path = str(path)
        # A file database is required because every operation opens a connection.
        if self.path == ":memory:":
            raise ValueError("use a file-backed database")
        with closing(self._connect()) as connection, connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS documents (
                owner TEXT NOT NULL,
                identifier TEXT NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (owner, identifier)
            )""")

    def _connect(self):
        return sqlite3.connect(self.path, timeout=1.0, autocommit=False)

    def put(self, owner: str, identifier: str, text: str) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute("""INSERT INTO documents(owner, identifier, text)
                VALUES (?, ?, ?) ON CONFLICT(owner, identifier)
                DO UPDATE SET text=excluded.text""", (owner, identifier, text))

    def get(self, owner: str, identifier: str) -> str | None:
        with closing(self._connect()) as connection, connection:
            row = connection.execute("SELECT text FROM documents WHERE owner=? AND identifier=?",
                                     (owner, identifier)).fetchone()
        return None if row is None else row[0]
