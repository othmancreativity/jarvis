from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from agents.memory_agent import SemanticMemory


class TestSemanticMemory:
    @pytest.fixture
    def semantic_memory(self):
        sm = SemanticMemory()
        sm._loaded = False
        sm._model = None
        return sm

    def test_add_and_keyword_search(self, semantic_memory):
        sm = semantic_memory
        sm.add_memory("Jarvis likes to browse the web", {"type": "preference"})
        sm.add_memory("User prefers dark mode", {"type": "preference"})
        sm.add_memory("The capital of France is Paris", {"type": "fact"})

        results = sm.search("browse web", top_k=2)
        assert len(results) >= 1
        assert "browse" in results[0]["text"]

    def test_search_empty(self, semantic_memory):
        results = semantic_memory.search("anything")
        assert results == []

    def test_search_no_match(self, semantic_memory):
        sm = semantic_memory
        sm.add_memory("Hello world", {})
        results = sm.search("nonexistent_term_xyz", top_k=1)
        assert len(results) == 0

    def test_add_memory_with_metadata(self, semantic_memory):
        sm = semantic_memory
        sm.add_memory("test memory", {"key": "value"})
        results = sm.search("test memory", top_k=1)
        assert len(results) >= 1
        assert results[0]["metadata"].get("key") == "value"

    def test_stats(self, semantic_memory):
        sm = semantic_memory
        assert sm.stats["text_count"] == 0
        sm.add_memory("some text")
        assert sm.stats["text_count"] == 1

    def test_keyword_search_scoring(self, semantic_memory):
        sm = semantic_memory
        sm.add_memory("the quick brown fox jumps")
        sm.add_memory("fox is quick")
        sm.add_memory("lazy dog sleeps")

        results = sm.search("quick fox", top_k=3)
        assert len(results) >= 1
        assert results[0]["score"] > 0

    def test_persistence(self, semantic_memory):
        sm = semantic_memory
        sm.add_memory("persistent memory", {"tag": "test"})
        assert len(sm._texts) == 1
        assert sm._metadata[0]["tag"] == "test"


class TestMemoryAgent:
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        from agents.memory_agent import MemoryAgent
        agent = MemoryAgent()
        result = await agent.initialize()
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_agent_info(self):
        from agents.memory_agent import MemoryAgent
        agent = MemoryAgent()
        info = agent.get_info()
        assert info["agent_id"] == "memory"
        assert "semantic_search" in info["capabilities"]
