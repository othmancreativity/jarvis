"""
JARVIS 4.5 — Memory System Tests
=================================
"""

import pytest
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_system import MemorySystem, LRUCache, WorkingMemoryEntry


class TestLRUCache:
    def test_put_and_get(self):
        cache = LRUCache(max_size=10)
        entry = WorkingMemoryEntry(content="test_value")
        cache.put("key1", entry)
        result = cache.get("key1")
        assert result is not None
        assert result.content == "test_value"

    def test_expired_entry(self):
        cache = LRUCache(max_size=10)
        entry = WorkingMemoryEntry(content="test", ttl_seconds=0.01)
        cache.put("key1", entry)
        time.sleep(0.02)
        result = cache.get("key1")
        assert result is None

    def test_lru_eviction(self):
        cache = LRUCache(max_size=3)
        for i in range(5):
            cache.put(f"key_{i}", WorkingMemoryEntry(content=f"value_{i}"))
        assert cache.size == 3
        assert cache.get("key_0") is None
        assert cache.get("key_4") is not None

    def test_clear(self):
        cache = LRUCache(max_size=10)
        cache.put("k1", WorkingMemoryEntry(content="v1"))
        cache.clear()
        assert cache.size == 0


class TestMemorySystem:
    def test_working_memory(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.working_set("test_key", "test_value", ttl_seconds=60)
        assert mem.working_get("test_key") == "test_value"

    def test_working_memory_expiry(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.working_set("key1", "value1", ttl_seconds=0.01)
        time.sleep(0.02)
        assert mem.working_get("key1") is None

    def test_learn_and_recall_fact(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.learn_fact("PREFERENCE", "theme", "dark")
        facts = mem.recall_fact(category="PREFERENCE", key="theme")
        assert len(facts) == 1
        assert facts[0].value == "dark"

    def test_user_profile(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.learn_fact("PROFILE", "name", "User")
        mem.learn_fact("PROFILE", "language", "en")
        profile = mem.get_user_profile()
        assert profile.get("name") == "User"
        assert profile.get("language") == "en"

    def test_preferences(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.update_preference("notifications", True)
        prefs = mem.get_preferences()
        assert prefs.get("notifications") is True

    def test_record_episode(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        eid = mem.record_episode("session_1", "test_action", "content", "success")
        assert eid is not None
        episodes = mem.recall_episodes(session_id="session_1")
        assert len(episodes) == 1
        assert episodes[0].action == "test_action"

    def test_learn_procedure(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.learn_procedure("test_proc", "Test procedure", [{"step": 1, "action": "test"}])
        procs = mem.recall_procedure("test_proc")
        assert len(procs) == 1
        assert procs[0].name == "test_proc"

    def test_procedure_success_tracking(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.learn_procedure("proc1", "Description", [])
        mem.record_procedure_success("proc1")
        mem.record_procedure_success("proc1")
        mem.record_procedure_failure("proc1")
        procs = mem.recall_procedure("proc1")
        assert procs[0].success_count == 2
        assert procs[0].failure_count == 1
        assert procs[0].success_rate == 2 / 3

    def test_find_best_procedure(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.learn_procedure("backup_files", "Backup workflow", [])
        mem.learn_procedure("backup_db", "Database backup", [])
        mem.record_procedure_success("backup_files")
        mem.record_procedure_success("backup_files")
        mem.record_procedure_failure("backup_db")
        best = mem.find_best_procedure("backup")
        assert best is not None
        assert best.name == "backup_files"

    def test_cleanup(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.working_set("key", "value", ttl_seconds=0.01)
        time.sleep(0.02)
        stats = mem.cleanup()
        assert stats["working_expired"] >= 1

    def test_export_all(self, tmp_path):
        mem = MemorySystem(db_path=tmp_path / "test.db")
        mem.working_set("k", "v")
        mem.learn_fact("FACT", "key", "value")
        exported = mem.export_all()
        assert "working" in exported
        assert "semantic" in exported
        assert "procedures" in exported


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
