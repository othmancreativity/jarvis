from __future__ import annotations

import json
import logging
import sqlite3
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.memory")


@dataclass
class MemoryEntry:
    id: str = ""
    content: Any = None
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)


@dataclass
class WorkingMemoryEntry(MemoryEntry):
    ttl_seconds: float = 300.0
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        return (time.time() - self.last_accessed) > self.ttl_seconds


@dataclass
class EpisodicMemoryEntry(MemoryEntry):
    session_id: str = ""
    action: str = ""
    result: str = ""
    duration_ms: int = 0
    tags: list[str] = field(default_factory=list)


@dataclass
class SemanticMemoryEntry(MemoryEntry):
    category: str = ""
    key: str = ""
    value: Any = None
    updated_at: float = field(default_factory=time.time)


@dataclass
class ProceduralMemoryEntry(MemoryEntry):
    name: str = ""
    description: str = ""
    steps: list[dict] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    last_used: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.5


class LRUCache:
    def __init__(self, max_size: int = 100) -> None:
        self._cache: OrderedDict[str, WorkingMemoryEntry] = OrderedDict()
        self._max_size = max_size
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[WorkingMemoryEntry]:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if entry.is_expired():
                del self._cache[key]
                return None
            entry.access_count += 1
            entry.last_accessed = time.time()
            self._cache.move_to_end(key)
            return entry

    def put(self, key: str, entry: WorkingMemoryEntry) -> None:
        with self._lock:
            self._cache[key] = entry
            self._cache.move_to_end(key)
            while len(self._cache) > self._max_size:
                self._cache.popitem(last=False)

    def remove(self, key: str) -> bool:
        with self._lock:
            return bool(self._cache.pop(key, None))

    def clear_expired(self) -> int:
        with self._lock:
            expired = [k for k, v in self._cache.items() if v.is_expired()]
            for k in expired:
                del self._cache[k]
            return len(expired)

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._cache.keys())

    def values(self) -> list[WorkingMemoryEntry]:
        with self._lock:
            return list(self._cache.values())

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._cache)


class SQLiteMemoryStore:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or paths.memory_db
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id TEXT PRIMARY KEY, session_id TEXT NOT NULL, content TEXT NOT NULL,
                    action TEXT, result TEXT, duration_ms INTEGER DEFAULT 0,
                    tags TEXT DEFAULT '[]', timestamp REAL NOT NULL,
                    source TEXT DEFAULT 'unknown', confidence REAL DEFAULT 1.0
                );
                CREATE INDEX IF NOT EXISTS idx_episodic_session ON episodic_memory(session_id);

                CREATE TABLE IF NOT EXISTS semantic_memory (
                    id TEXT PRIMARY KEY, category TEXT NOT NULL, key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL, timestamp REAL NOT NULL, updated_at REAL NOT NULL,
                    source TEXT DEFAULT 'unknown', confidence REAL DEFAULT 1.0
                );

                CREATE TABLE IF NOT EXISTS procedural_memory (
                    id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, description TEXT,
                    steps TEXT DEFAULT '[]', success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0, last_used REAL DEFAULT 0,
                    timestamp REAL NOT NULL, source TEXT DEFAULT 'unknown'
                );
            """)
            conn.commit()

    def save_semantic(self, entry: SemanticMemoryEntry) -> None:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO semantic_memory
                   (id, category, key, value, timestamp, updated_at, source, confidence)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (entry.id, entry.category, entry.key, json.dumps(entry.value),
                 entry.timestamp, entry.updated_at, entry.source, entry.confidence)
            )
            conn.commit()

    def load_semantic(self, category: Optional[str] = None,
                      key: Optional[str] = None) -> list[SemanticMemoryEntry]:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM semantic_memory WHERE 1=1"
            params = []
            if category:
                query += " AND category = ?"
                params.append(category)
            if key:
                query += " AND key = ?"
                params.append(key)
            rows = conn.execute(query, params).fetchall()
            return [SemanticMemoryEntry(
                id=r["id"], content=None, timestamp=r["timestamp"], source=r["source"],
                confidence=r["confidence"], category=r["category"], key=r["key"],
                value=json.loads(r["value"]), updated_at=r["updated_at"],
            ) for r in rows]

    def save_episodic(self, entry: EpisodicMemoryEntry) -> None:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO episodic_memory
                   (id, session_id, content, action, result, duration_ms, tags, timestamp, source, confidence)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (entry.id, entry.session_id, json.dumps(entry.content), entry.action,
                 entry.result, entry.duration_ms, json.dumps(entry.tags),
                 entry.timestamp, entry.source, entry.confidence)
            )
            conn.commit()

    def load_episodic(self, session_id: Optional[str] = None, limit: int = 50,
                      since: Optional[float] = None) -> list[EpisodicMemoryEntry]:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM episodic_memory WHERE 1=1"
            params = []
            if session_id:
                query += " AND session_id = ?"
                params.append(session_id)
            if since:
                query += " AND timestamp > ?"
                params.append(since)
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(query, params).fetchall()
            return [EpisodicMemoryEntry(
                id=r["id"], content=json.loads(r["content"]), timestamp=r["timestamp"],
                source=r["source"], confidence=r["confidence"],
                session_id=r["session_id"], action=r["action"] or "",
                result=r["result"] or "", duration_ms=r["duration_ms"] or 0,
                tags=json.loads(r["tags"] or "[]"),
            ) for r in rows]

    def save_procedural(self, entry: ProceduralMemoryEntry) -> None:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO procedural_memory
                   (id, name, description, steps, success_count, failure_count, last_used, timestamp, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (entry.id, entry.name, entry.description, json.dumps(entry.steps),
                 entry.success_count, entry.failure_count, entry.last_used,
                 entry.timestamp, entry.source)
            )
            conn.commit()

    def load_procedural(self, name: Optional[str] = None) -> list[ProceduralMemoryEntry]:
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM procedural_memory"
            params = []
            if name:
                query += " WHERE name = ?"
                params.append(name)
            rows = conn.execute(query, params).fetchall()
            return [ProceduralMemoryEntry(
                id=r["id"], content=None, timestamp=r["timestamp"], source=r["source"],
                name=r["name"], description=r["description"] or "",
                steps=json.loads(r["steps"] or "[]"),
                success_count=r["success_count"] or 0, failure_count=r["failure_count"] or 0,
                last_used=r["last_used"] or 0,
            ) for r in rows]


class MemorySystem:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.working = LRUCache(max_size=100)
        self.store = SQLiteMemoryStore(db_path)

    def working_set(self, key: str, value: Any, ttl_seconds: float = 300.0,
                    source: str = "runtime") -> None:
        self.working.put(key, WorkingMemoryEntry(content=value, source=source, ttl_seconds=ttl_seconds))

    def working_get(self, key: str) -> Optional[Any]:
        entry = self.working.get(key)
        return entry.content if entry else None

    def learn_fact(self, category: str, key: str, value: Any,
                   confidence: float = 1.0, source: str = "agent") -> str:
        import hashlib
        entry = SemanticMemoryEntry(
            id=hashlib.sha256(f"{time.time()}:{key}".encode()).hexdigest()[:16],
            category=category, key=key, value=value,
            source=source, confidence=confidence, updated_at=time.time(),
        )
        self.store.save_semantic(entry)
        return entry.id

    def recall_fact(self, category: Optional[str] = None,
                    key: Optional[str] = None) -> list[SemanticMemoryEntry]:
        return self.store.load_semantic(category, key)

    def record_episode(self, session_id: str, action: str, content: Any,
                       result: str = "", duration_ms: int = 0,
                       tags: Optional[list[str]] = None, source: str = "agent") -> str:
        import hashlib
        entry = EpisodicMemoryEntry(
            id=hashlib.sha256(f"{time.time()}:{session_id}".encode()).hexdigest()[:16],
            session_id=session_id, action=action, content=content,
            result=result, duration_ms=duration_ms, tags=tags or [], source=source,
        )
        self.store.save_episodic(entry)
        return entry.id

    def update_preference(self, key: str, value: Any) -> str:
        return self.learn_fact("PREFERENCE", key, value, source="user")

    def get_preferences(self) -> dict:
        return {e.key: e.value for e in self.recall_fact(category="PREFERENCE")}

    def get_user_profile(self) -> dict:
        return {e.key: e.value for e in self.recall_fact(category="PROFILE")}

    def get_stats(self) -> dict:
        return {
            "working_size": self.working.size,
            "db_path": str(self.store.db_path),
        }


memory = MemorySystem()
