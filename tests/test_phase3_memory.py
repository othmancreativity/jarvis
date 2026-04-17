"""Phase 3 tests: memory system (short-term, long-term, database, manager, user profile)."""

from __future__ import annotations

import os
import tempfile

import pytest


# ---------------------------------------------------------------------------
# Short-term memory
# ---------------------------------------------------------------------------

class TestShortTermMemory:
    def test_add_and_retrieve(self):
        from core.memory.short_term import ShortTermMemory

        stm = ShortTermMemory(max_messages=10, max_tokens=5000)
        stm.add("user", "Hello Jarvis")
        stm.add("assistant", "Hello! How can I help?")

        msgs = stm.get_messages()
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"
        assert msgs[1]["role"] == "assistant"

    def test_trim_by_message_count(self):
        from core.memory.short_term import ShortTermMemory

        stm = ShortTermMemory(max_messages=3, max_tokens=100000)
        for i in range(5):
            stm.add("user", f"Message {i}")

        assert stm.count == 3
        msgs = stm.get_messages()
        assert msgs[0]["content"] == "Message 2"

    def test_trim_by_token_budget(self):
        from core.memory.short_term import ShortTermMemory

        stm = ShortTermMemory(max_messages=100, max_tokens=50)
        stm.add("user", "A" * 200)  # ~50 tokens
        stm.add("user", "B" * 40)   # ~10 tokens

        # After trimming, only the last message should fit
        assert stm.count >= 1
        assert stm.total_tokens <= 60  # allow some tolerance

    def test_clear(self):
        from core.memory.short_term import ShortTermMemory

        stm = ShortTermMemory()
        stm.add("user", "test")
        stm.clear()
        assert stm.count == 0

    def test_get_last_n(self):
        from core.memory.short_term import ShortTermMemory

        stm = ShortTermMemory()
        for i in range(10):
            stm.add("user", f"msg {i}")

        msgs = stm.get_messages(3)
        assert len(msgs) == 3
        assert msgs[-1]["content"] == "msg 9"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

class TestDatabase:
    def test_save_and_get_messages(self, tmp_path):
        from core.memory.database import Database

        db = Database(db_path=tmp_path / "test.db")
        db.save_message("user", "Hello", session_id="s1")
        db.save_message("assistant", "Hi there", session_id="s1")

        msgs = db.get_messages(session_id="s1")
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"
        db.close()

    def test_facts(self, tmp_path):
        from core.memory.database import Database

        db = Database(db_path=tmp_path / "test.db")
        fid = db.save_fact("Python is a programming language", category="tech")
        results = db.search_facts("Python")
        assert len(results) >= 1
        assert "Python" in results[0]["content"]
        db.close()

    def test_tasks(self, tmp_path):
        from core.memory.database import Database

        db = Database(db_path=tmp_path / "test.db")
        tid = db.save_task("Build memory system", priority=5)
        tasks = db.get_tasks()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Build memory system"

        db.update_task(tid, status="done")
        done = db.get_tasks(status="done")
        assert len(done) == 1
        db.close()

    def test_sessions(self, tmp_path):
        from core.memory.database import Database

        db = Database(db_path=tmp_path / "test.db")
        db.save_message("user", "msg1", session_id="s1")
        db.save_message("user", "msg2", session_id="s2")

        sessions = db.list_sessions()
        assert len(sessions) == 2
        db.close()

    def test_clear_all(self, tmp_path):
        from core.memory.database import Database

        db = Database(db_path=tmp_path / "test.db")
        db.save_message("user", "test")
        db.save_fact("test fact")
        db.save_task("test task")
        db.clear_all()

        assert len(db.get_messages()) == 0
        assert len(db.get_facts()) == 0
        assert len(db.get_tasks()) == 0
        db.close()


# ---------------------------------------------------------------------------
# User profile
# ---------------------------------------------------------------------------

class TestUserProfile:
    def test_create_and_save(self, tmp_path):
        from core.memory.user_profile import UserProfile

        p = UserProfile(user_id="test_user", profiles_dir=tmp_path)
        assert p.preferred_language == "ar"
        assert p.total_interactions == 0

        p.record_interaction("code", 120)
        assert p.total_interactions == 1
        assert p.task_counts["code"] == 1

    def test_persistence(self, tmp_path):
        from core.memory.user_profile import UserProfile

        p1 = UserProfile(user_id="persist_test", profiles_dir=tmp_path)
        p1.update(preferred_language="en")
        p1.record_interaction("chat", 50)

        # Reload
        p2 = UserProfile(user_id="persist_test", profiles_dir=tmp_path)
        assert p2.preferred_language == "en"
        assert p2.total_interactions == 1

    def test_code_heavy_detection(self, tmp_path):
        from core.memory.user_profile import UserProfile

        p = UserProfile(user_id="coder", profiles_dir=tmp_path)
        for _ in range(6):
            p.record_interaction("code", 100)
        for _ in range(2):
            p.record_interaction("chat", 50)

        assert p.is_code_heavy is True

    def test_failure_tracking(self, tmp_path):
        from core.memory.user_profile import UserProfile

        p = UserProfile(user_id="fail_test", profiles_dir=tmp_path)
        p.record_failure()
        p.record_failure()
        assert p.recent_failures == 2

        p.record_success()
        assert p.recent_failures == 1


# ---------------------------------------------------------------------------
# Memory Manager (integration)
# ---------------------------------------------------------------------------

class TestMemoryManager:
    def test_save_and_get_context(self, tmp_path):
        from core.memory.manager import MemoryManager

        mm = MemoryManager(
            db_path=str(tmp_path / "test.db"),
            chroma_dir=str(tmp_path / "chroma"),
            session_id="test",
        )
        mm.save_interaction("user", "What is Python?")
        mm.save_interaction("assistant", "Python is a programming language.")

        ctx = mm.get_context(5)
        assert len(ctx) == 2

        mm.close()

    def test_search_returns_structure(self, tmp_path):
        from core.memory.manager import MemoryManager

        mm = MemoryManager(
            db_path=str(tmp_path / "test.db"),
            chroma_dir=str(tmp_path / "chroma"),
        )
        results = mm.search("test query")
        assert "semantic" in results
        assert "facts" in results
        mm.close()
