"""SQLite structured storage for conversations, facts, and tasks.

Schema auto-creates on init.  All queries are parameterised.
"""

from __future__ import annotations

import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any

from loguru import logger


def _now() -> float:
    return time.time()


def _uid() -> str:
    return uuid.uuid4().hex[:12]


class Database:
    """Lightweight SQLite wrapper for structured Jarvis data.

    Parameters
    ----------
    db_path : str | Path
        Path to the SQLite file.  Directories are created automatically.
    """

    def __init__(self, db_path: str | Path = "data/jarvis.db") -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None
        self._ensure_schema()

    # -- Connection ----------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self._path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def _ensure_schema(self) -> None:
        conn = self._get_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id          TEXT PRIMARY KEY,
                session_id  TEXT NOT NULL,
                role        TEXT NOT NULL,
                content     TEXT NOT NULL,
                timestamp   REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS facts (
                id          TEXT PRIMARY KEY,
                content     TEXT NOT NULL,
                source      TEXT DEFAULT 'auto',
                category    TEXT DEFAULT 'general',
                created_at  REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                status      TEXT DEFAULT 'pending',
                priority    INTEGER DEFAULT 0,
                created_at  REAL NOT NULL,
                updated_at  REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);
            CREATE INDEX IF NOT EXISTS idx_conv_ts      ON conversations(timestamp);
            CREATE INDEX IF NOT EXISTS idx_facts_cat     ON facts(category);
            CREATE INDEX IF NOT EXISTS idx_tasks_status  ON tasks(status);
            """
        )
        conn.commit()
        logger.debug("Database: schema ready at {}", self._path)

    # -- Conversations -------------------------------------------------------

    def save_message(
        self, role: str, content: str, session_id: str = "default"
    ) -> str:
        uid = _uid()
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO conversations (id, session_id, role, content, timestamp) VALUES (?,?,?,?,?)",
            (uid, session_id, role, content, _now()),
        )
        conn.commit()
        return uid

    def get_messages(
        self, session_id: str = "default", limit: int = 50
    ) -> list[dict[str, Any]]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT role, content, timestamp FROM conversations "
            "WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def list_sessions(self, limit: int = 100) -> list[dict[str, Any]]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT session_id, COUNT(*) as msg_count, MAX(timestamp) as last_ts "
            "FROM conversations GROUP BY session_id ORDER BY last_ts DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def delete_session(self, session_id: str) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "DELETE FROM conversations WHERE session_id = ?", (session_id,)
        )
        conn.commit()
        return cur.rowcount

    # -- Facts ---------------------------------------------------------------

    def save_fact(
        self, content: str, *, source: str = "auto", category: str = "general"
    ) -> str:
        uid = _uid()
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO facts (id, content, source, category, created_at) VALUES (?,?,?,?,?)",
            (uid, content, source, category, _now()),
        )
        conn.commit()
        return uid

    def search_facts(self, keyword: str, limit: int = 10) -> list[dict[str, Any]]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT id, content, source, category, created_at FROM facts "
            "WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{keyword}%", limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_facts(self, category: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        conn = self._get_conn()
        if category:
            rows = conn.execute(
                "SELECT * FROM facts WHERE category = ? ORDER BY created_at DESC LIMIT ?",
                (category, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM facts ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    # -- Tasks ---------------------------------------------------------------

    def save_task(
        self, title: str, *, status: str = "pending", priority: int = 0
    ) -> str:
        uid = _uid()
        now = _now()
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO tasks (id, title, status, priority, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?)",
            (uid, title, status, priority, now, now),
        )
        conn.commit()
        return uid

    def update_task(self, task_id: str, **fields: Any) -> None:
        conn = self._get_conn()
        allowed = {"title", "status", "priority"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return
        updates["updated_at"] = _now()
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        conn.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = ?",
            (*updates.values(), task_id),
        )
        conn.commit()

    def get_tasks(self, status: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        conn = self._get_conn()
        if status:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY priority DESC, created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY priority DESC, created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    # -- Maintenance ---------------------------------------------------------

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def clear_all(self) -> None:
        conn = self._get_conn()
        conn.executescript(
            "DELETE FROM conversations; DELETE FROM facts; DELETE FROM tasks;"
        )
        conn.commit()
        logger.info("Database: all tables cleared")
