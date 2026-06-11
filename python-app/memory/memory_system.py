"""
JARVIS 4.5 — Multi-Layer Memory System
=======================================
Production-grade memory with 4 layers:
    Working:   Current context, active plans, pending confirmations
    Episodic:  Session history, past actions with outcomes
    Semantic:  Long-term facts, user preferences, learned knowledge
    Procedural: Stored workflows, reusable skill patterns
"""

from __future__ import annotations

import json
import time
import sqlite3
import threading
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Callable
from collections import OrderedDict


# ── Data Models ──────────────────────────────────────────────────────────

@dataclass
class MemoryEntry:
    """Base class for memory entries."""
    id: str = ""
    content: Any = None
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.sha256(
                f"{self.timestamp}:{str(self.content)[:50]}".encode()
            ).hexdigest()[:16]


@dataclass
class WorkingMemoryEntry(MemoryEntry):
    """Working memory entry — short-lived context."""
    ttl_seconds: float = 300.0  # 5 minutes default TTL
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        return (time.time() - self.last_accessed) > self.ttl_seconds


@dataclass
class EpisodicMemoryEntry(MemoryEntry):
    """Episodic memory entry — past events and sessions."""
    session_id: str = ""
    action: str = ""
    result: str = ""
    duration_ms: int = 0
    tags: list[str] = field(default_factory=list)


@dataclass
class SemanticMemoryEntry(MemoryEntry):
    """Semantic memory entry — long-term facts and knowledge."""
    category: str = ""  # PROFILE, PREFERENCE, FACT, KNOWLEDGE, GOAL
    key: str = ""
    value: Any = None
    updated_at: float = field(default_factory=time.time)


@dataclass
class ProceduralMemoryEntry(MemoryEntry):
    """Procedural memory entry — learned workflows and patterns."""
    name: str = ""
    description: str = ""
    steps: list[dict] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    last_used: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5
        return self.success_count / total


# ── Memory Stores ────────────────────────────────────────────────────────

class LRUCache:
    """Thread-safe LRU cache for working memory."""

    def __init__(self, max_size: int = 100):
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
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = entry
            while len(self._cache) > self._max_size:
                self._cache.popitem(last=False)

    def remove(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

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
    """Persistent SQLite-backed store for episodic and semantic memory."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (Path.home() / ".jarvis" / "memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database tables."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    action TEXT,
                    result TEXT,
                    duration_ms INTEGER DEFAULT 0,
                    tags TEXT DEFAULT '[]',
                    timestamp REAL NOT NULL,
                    source TEXT DEFAULT 'unknown',
                    confidence REAL DEFAULT 1.0
                );
                CREATE INDEX IF NOT EXISTS idx_episodic_session ON episodic_memory(session_id);
                CREATE INDEX IF NOT EXISTS idx_episodic_time ON episodic_memory(timestamp);

                CREATE TABLE IF NOT EXISTS semantic_memory (
                    id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    source TEXT DEFAULT 'unknown',
                    confidence REAL DEFAULT 1.0
                );
                CREATE INDEX IF NOT EXISTS idx_semantic_category ON semantic_memory(category);

                CREATE TABLE IF NOT EXISTS procedural_memory (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    steps TEXT NOT NULL DEFAULT '[]',
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    last_used REAL DEFAULT 0,
                    timestamp REAL NOT NULL,
                    source TEXT DEFAULT 'unknown'
                );
                CREATE INDEX IF NOT EXISTS idx_procedural_name ON procedural_memory(name);
            """)
            conn.commit()

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
            entries = []
            for row in rows:
                entries.append(EpisodicMemoryEntry(
                    id=row["id"],
                    content=json.loads(row["content"]),
                    timestamp=row["timestamp"],
                    source=row["source"],
                    confidence=row["confidence"],
                    session_id=row["session_id"],
                    action=row["action"] or "",
                    result=row["result"] or "",
                    duration_ms=row["duration_ms"] or 0,
                    tags=json.loads(row["tags"] or "[]"),
                ))
            return entries

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
            query += " ORDER BY updated_at DESC"

            rows = conn.execute(query, params).fetchall()
            entries = []
            for row in rows:
                entries.append(SemanticMemoryEntry(
                    id=row["id"],
                    content=None,
                    timestamp=row["timestamp"],
                    source=row["source"],
                    confidence=row["confidence"],
                    category=row["category"],
                    key=row["key"],
                    value=json.loads(row["value"]),
                    updated_at=row["updated_at"],
                ))
            return entries

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
            query += " ORDER BY success_count DESC"

            rows = conn.execute(query, params).fetchall()
            entries = []
            for row in rows:
                entries.append(ProceduralMemoryEntry(
                    id=row["id"],
                    content=None,
                    timestamp=row["timestamp"],
                    source=row["source"],
                    name=row["name"],
                    description=row["description"] or "",
                    steps=json.loads(row["steps"] or "[]"),
                    success_count=row["success_count"] or 0,
                    failure_count=row["failure_count"] or 0,
                    last_used=row["last_used"] or 0,
                ))
            return entries

    def cleanup_old(self, table: str, older_than_days: int = 90) -> int:
        """Remove old entries. Returns count removed."""
        cutoff = time.time() - (older_than_days * 86400)
        with self._lock, sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff,))
            conn.commit()
            return cursor.rowcount


# ── Unified Memory System ────────────────────────────────────────────────

class MemorySystem:
    """
    Unified multi-layer memory system for JARVIS.
    Coordinates Working, Episodic, Semantic, and Procedural memory.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.working = LRUCache(max_size=100)
        self.store = SQLiteMemoryStore(db_path)
        self._lock = threading.RLock()
        self._session_counter = 0

    # ── Working Memory ─────────────────────────────────────────────────

    def working_set(self, key: str, value: Any, ttl_seconds: float = 300.0,
                    source: str = "runtime") -> None:
        """Store a value in working memory."""
        entry = WorkingMemoryEntry(
            content=value,
            source=source,
            ttl_seconds=ttl_seconds,
        )
        self.working.put(key, entry)

    def working_get(self, key: str) -> Optional[Any]:
        """Retrieve a value from working memory."""
        entry = self.working.get(key)
        return entry.content if entry else None

    def working_delete(self, key: str) -> bool:
        """Remove a value from working memory."""
        return self.working.remove(key)

    def working_clear(self) -> None:
        """Clear all working memory."""
        self.working.clear()

    def working_snapshot(self) -> dict[str, Any]:
        """Get a snapshot of current working memory."""
        return {k: v.content for k, v in self.working.values()}

    # ── Episodic Memory ────────────────────────────────────────────────

    def record_episode(self, session_id: str, action: str, content: Any,
                       result: str = "", duration_ms: int = 0,
                       tags: Optional[list[str]] = None, source: str = "agent") -> str:
        """Record an episodic memory."""
        entry = EpisodicMemoryEntry(
            session_id=session_id,
            action=action,
            content=content,
            result=result,
            duration_ms=duration_ms,
            tags=tags or [],
            source=source,
        )
        self.store.save_episodic(entry)
        return entry.id

    def recall_episodes(self, session_id: Optional[str] = None, limit: int = 50,
                        since_hours: Optional[int] = None) -> list[EpisodicMemoryEntry]:
        """Recall episodic memories."""
        since = None
        if since_hours:
            since = time.time() - (since_hours * 3600)
        return self.store.load_episodic(session_id, limit, since)

    def get_session_summary(self, session_id: str) -> dict:
        """Get a summary of a session."""
        episodes = self.recall_episodes(session_id=session_id, limit=1000)
        if not episodes:
            return {"session_id": session_id, "episode_count": 0}

        actions = {}
        total_duration = 0
        for ep in episodes:
            actions[ep.action] = actions.get(ep.action, 0) + 1
            total_duration += ep.duration_ms

        return {
            "session_id": session_id,
            "episode_count": len(episodes),
            "total_duration_ms": total_duration,
            "actions": actions,
            "started": datetime.fromtimestamp(episodes[-1].timestamp).isoformat(),
            "ended": datetime.fromtimestamp(episodes[0].timestamp).isoformat(),
        }

    # ── Semantic Memory ────────────────────────────────────────────────

    def learn_fact(self, category: str, key: str, value: Any,
                   confidence: float = 1.0, source: str = "agent") -> str:
        """Store a fact in semantic memory."""
        entry = SemanticMemoryEntry(
            category=category,
            key=key,
            value=value,
            source=source,
            confidence=confidence,
            updated_at=time.time(),
        )
        self.store.save_semantic(entry)
        return entry.id

    def recall_fact(self, category: Optional[str] = None,
                    key: Optional[str] = None) -> list[SemanticMemoryEntry]:
        """Recall facts from semantic memory."""
        return self.store.load_semantic(category, key)

    def get_user_profile(self) -> dict:
        """Get consolidated user profile from semantic memory."""
        entries = self.recall_fact(category="PROFILE")
        profile = {}
        for entry in entries:
            profile[entry.key] = entry.value
        return profile

    def update_preference(self, key: str, value: Any) -> str:
        """Update a user preference."""
        return self.learn_fact("PREFERENCE", key, value, source="user")

    def get_preferences(self) -> dict:
        """Get all user preferences."""
        entries = self.recall_fact(category="PREFERENCE")
        return {e.key: e.value for e in entries}

    # ── Procedural Memory ──────────────────────────────────────────────

    def learn_procedure(self, name: str, description: str, steps: list[dict],
                        source: str = "agent") -> str:
        """Store a procedure/workflow."""
        entry = ProceduralMemoryEntry(
            name=name,
            description=description,
            steps=steps,
            source=source,
        )
        self.store.save_procedural(entry)
        return entry.id

    def recall_procedure(self, name: Optional[str] = None) -> list[ProceduralMemoryEntry]:
        """Recall procedures."""
        return self.store.load_procedural(name)

    def record_procedure_success(self, name: str) -> None:
        """Record a successful execution of a procedure."""
        procedures = self.store.load_procedural(name)
        if procedures:
            proc = procedures[0]
            proc.success_count += 1
            proc.last_used = time.time()
            self.store.save_procedural(proc)

    def record_procedure_failure(self, name: str) -> None:
        """Record a failed execution of a procedure."""
        procedures = self.store.load_procedural(name)
        if procedures:
            proc = procedures[0]
            proc.failure_count += 1
            proc.last_used = time.time()
            self.store.save_procedural(proc)

    def find_best_procedure(self, query: str) -> Optional[ProceduralMemoryEntry]:
        """Find the most successful procedure matching a query."""
        procedures = self.store.load_procedural()
        matching = [p for p in procedures if query.lower() in p.name.lower()
                    or query.lower() in p.description.lower()]
        if not matching:
            return None
        return max(matching, key=lambda p: p.success_rate)

    # ── Maintenance ────────────────────────────────────────────────────

    def cleanup(self) -> dict:
        """Clean up old entries across all memory layers."""
        expired = self.working.clear_expired()
        episodic_removed = self.store.cleanup_old("episodic_memory", 90)
        semantic_removed = self.store.cleanup_old("semantic_memory", 365)
        return {
            "working_expired": expired,
            "episodic_removed": episodic_removed,
            "semantic_removed": semantic_removed,
        }

    def get_stats(self) -> dict:
        """Get memory system statistics."""
        return {
            "working_size": self.working.size,
            "working_keys": self.working.keys()[:20],  # Sample
            "db_path": str(self.store.db_path),
        }

    def export_all(self) -> dict:
        """Export all memory for backup."""
        working_data = {}
        for k in self.working.keys():
            entry = self.working.get(k)
            if entry:
                working_data[k] = entry.content
        return {
            "working": working_data,
            "semantic": [asdict(e) for e in self.recall_fact()],
            "procedures": [asdict(e) for e in self.recall_procedure()],
        }


# Singleton
memory = MemorySystem()
