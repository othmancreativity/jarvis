from __future__ import annotations

import time
from pathlib import Path

import pytest

from memory.memory_system import MemorySystem, LRUCache, WorkingMemoryEntry


class TestLRUCache:
    def test_put_and_get(self):
        cache = LRUCache(max_size=3)
        cache.put("a", WorkingMemoryEntry(content=1))
        entry = cache.get("a")
        assert entry is not None
        assert entry.content == 1

    def test_expired_entry(self):
        cache = LRUCache(max_size=3)
        cache.put("a", WorkingMemoryEntry(content=1, ttl_seconds=0))
        time.sleep(0.01)
        entry = cache.get("a")
        assert entry is None

    def test_lru_eviction(self):
        cache = LRUCache(max_size=2)
        cache.put("a", WorkingMemoryEntry(content=1))
        cache.put("b", WorkingMemoryEntry(content=2))
        cache.put("c", WorkingMemoryEntry(content=3))
        assert cache.size <= 2

    def test_clear(self):
        cache = LRUCache(max_size=3)
        cache.put("a", WorkingMemoryEntry(content=1))
        cache.put("b", WorkingMemoryEntry(content=2))
        cache.clear()
        assert cache.size == 0

    def test_remove(self):
        cache = LRUCache(max_size=3)
        cache.put("a", WorkingMemoryEntry(content=1))
        assert cache.remove("a") is True
        assert cache.remove("nonexistent") is False


class TestMemorySystem:
    @pytest.fixture
    def mem(self, tmp_path):
        return MemorySystem(db_path=tmp_path / "test_memory.db")

    def test_working_memory(self, mem):
        mem.working_set("key1", "value1")
        assert mem.working_get("key1") == "value1"

    def test_working_memory_expiry(self, mem):
        mem.working_set("key2", "value2", ttl_seconds=0)
        import time
        time.sleep(0.01)
        assert mem.working_get("key2") is None

    def test_learn_and_recall_fact(self, mem):
        mid = mem.learn_fact("PROFILE", "name", "John")
        assert mid is not None
        facts = mem.recall_fact(category="PROFILE")
        assert any(f.key == "name" and f.value == "John" for f in facts)

    def test_user_profile(self, mem):
        mem.learn_fact("PROFILE", "name", "Jane")
        mem.learn_fact("PROFILE", "age", "30")
        profile = mem.get_user_profile()
        assert profile.get("name") == "Jane"
        assert profile.get("age") == "30"

    def test_preferences(self, mem):
        mem.update_preference("theme", "dark")
        prefs = mem.get_preferences()
        assert prefs.get("theme") == "dark"

    def test_record_episode(self, mem):
        eid = mem.record_episode("session_1", "test_action", "test content", "ok")
        assert eid is not None

    def test_get_stats(self, mem):
        stats = mem.get_stats()
        assert "working_size" in stats
        assert "db_path" in stats
