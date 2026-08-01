"""SQLite-backed, local-only application provenance ledger."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'discovered',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY,
    opportunity_id INTEGER NOT NULL REFERENCES opportunities(id),
    kind TEXT NOT NULL,
    path TEXT NOT NULL,
    source_version TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS application_events (
    id INTEGER PRIMARY KEY,
    opportunity_id INTEGER NOT NULL REFERENCES opportunities(id),
    status TEXT NOT NULL,
    verification_signal TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS exceptions (
    id INTEGER PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    kind TEXT NOT NULL,
    message TEXT NOT NULL,
    resolved_at TEXT,
    created_at TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(UTC).isoformat()


class Ledger:
    """Store provenance metadata only; artifact contents stay on the local filesystem."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    def record_opportunity(self, company: str, role: str, url: str) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO opportunities (company, role, url, created_at)
                   VALUES (?, ?, ?, ?)""",
                (company, role, url, _now()),
            )
            return int(cursor.lastrowid)

    def record_artifact(self, opportunity_id: int, kind: str, path: str, source_version: str | None = None) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO artifacts (opportunity_id, kind, path, source_version, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (opportunity_id, kind, path, source_version, _now()),
            )
            return int(cursor.lastrowid)

    def record_event(self, opportunity_id: int, status: str, verification_signal: str | None = None) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO application_events (opportunity_id, status, verification_signal, created_at)
                   VALUES (?, ?, ?, ?)""",
                (opportunity_id, status, verification_signal, _now()),
            )
            connection.execute("UPDATE opportunities SET status = ? WHERE id = ?", (status, opportunity_id))
            return int(cursor.lastrowid)

    def record_exception(self, kind: str, message: str, opportunity_id: int | None = None) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO exceptions (opportunity_id, kind, message, created_at)
                   VALUES (?, ?, ?, ?)""",
                (opportunity_id, kind, message, _now()),
            )
            return int(cursor.lastrowid)

    def counts(self) -> dict[str, int]:
        tables = ("opportunities", "artifacts", "application_events", "exceptions")
        with self.connect() as connection:
            return {
                table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in tables
            }
