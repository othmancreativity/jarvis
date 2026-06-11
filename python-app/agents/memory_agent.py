from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from agents.base_agent import BaseAgent, AgentMessage
from memory.memory_system import memory
from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.agents.memory")


class SemanticMemory:
    """Vector-based semantic memory using sentence-transformers and FAISS.

    Replaces the fake keyword-search with real embeddings for actual
    semantic retrieval.
    """

    def __init__(self, dimension: int = 384) -> None:
        self._dimension = dimension
        self._index: Any = None
        self._model: Any = None
        self._texts: list[str] = []
        self._metadata: list[dict] = []
        self._store_path: Path = paths.vector_store_dir / "semantic_index.faiss"
        self._texts_path: Path = paths.vector_store_dir / "semantic_texts.json"
        self._loaded = False

    async def initialize(self) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._dimension = self._model.get_sentence_embedding_dimension()
            self._load_persisted()
            self._loaded = True
            logger.info("SemanticMemory initialized with dim=%s", self._dimension)
            return True
        except ImportError:
            logger.warning("sentence-transformers not installed. Semantic memory disabled.")
            return False
        except Exception as e:
            logger.error("SemanticMemory init error: %s", e)
            return False

    def _ensure_index(self) -> None:
        if self._index is not None:
            return
        try:
            import faiss
            import numpy as np
            self._index = faiss.IndexFlatL2(self._dimension)
        except ImportError:
            pass

    def _load_persisted(self) -> None:
        try:
            import faiss
            import numpy as np
            if self._store_path.exists():
                self._index = faiss.read_index(str(self._store_path))
            if self._texts_path.exists():
                data = json.loads(self._texts_path.read_text(encoding="utf-8"))
                self._texts = data.get("texts", [])
                self._metadata = data.get("metadata", [])
        except Exception as e:
            logger.warning("Could not load persisted semantic index: %s", e)

    def _save_persisted(self) -> None:
        try:
            if self._index is not None:
                import faiss
                self._store_path.parent.mkdir(parents=True, exist_ok=True)
                faiss.write_index(self._index, str(self._store_path))
            self._texts_path.write_text(
                json.dumps({"texts": self._texts, "metadata": self._metadata}, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning("Could not persist semantic index: %s", e)

    def add_memory(self, text: str, metadata: dict = None) -> bool:
        if not self._loaded or self._model is None:
            self._texts.append(text)
            self._metadata.append(metadata or {})
            return True
        try:
            import numpy as np
            embedding = self._model.encode(text, normalize_embeddings=True)
            self._ensure_index()
            if self._index is not None:
                self._index.add(np.array([embedding], dtype=np.float32))
            self._texts.append(text)
            self._metadata.append(metadata or {})
            self._save_persisted()
            return True
        except Exception as e:
            logger.error("add_memory error: %s", e)
            return False

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self._texts and self._index is None:
            return self._keyword_search(query, top_k)

        if self._index is None or self._index.ntotal == 0:
            return self._keyword_search(query, top_k)

        try:
            import numpy as np
            query_vec = self._model.encode(query, normalize_embeddings=True)
            distances, indices = self._index.search(
                np.array([query_vec], dtype=np.float32), min(top_k, self._index.ntotal)
            )
            results = []
            for i, idx in enumerate(indices[0]):
                if idx >= 0 and idx < len(self._texts):
                    results.append({
                        "text": self._texts[idx],
                        "metadata": self._metadata[idx] if idx < len(self._metadata) else {},
                        "score": float(1.0 / (1.0 + distances[0][i])),
                    })
            return results
        except Exception as e:
            logger.error("Semantic search error: %s", e)
            return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int = 3) -> list[dict]:
        query_lower = query.lower()
        scored = []
        for i, text in enumerate(self._texts):
            score = sum(1 for word in query_lower.split() if word in text.lower())
            if score > 0:
                scored.append({
                    "text": text,
                    "metadata": self._metadata[i] if i < len(self._metadata) else {},
                    "score": score / max(len(query_lower.split()), 1),
                })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    @property
    def stats(self) -> dict:
        vec_count = self._index.ntotal if self._index is not None else 0
        return {"vector_count": vec_count, "text_count": len(self._texts), "loaded": self._loaded}


class MemoryAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="memory",
            name="Memory Agent",
            description="Memory management and retrieval",
        )
        self.register_capability("fact_storage")
        self.register_capability("episode_recording")
        self.register_capability("semantic_search")
        self.register_capability("preference_tracking")
        self.semantic = SemanticMemory()

    async def initialize(self) -> bool:
        base_ok = await super().initialize()
        sem_ok = await self.semantic.initialize()
        return base_ok and sem_ok

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        try:
            if command in ("memory", "remember", "recall"):
                query = payload.get("query", payload.get("key", ""))
                results = self.semantic.search(query)
                if results:
                    text = "\n".join(f"- {r['text']}" for r in results)
                    await self.send_response(message.sender, {
                        "status": "success",
                        "responseText": f"I remember: {text}",
                        "results": results,
                    }, message.correlation_id)
                else:
                    await self.send_response(message.sender, {
                        "status": "success",
                        "responseText": "I don't have any memory about that.",
                    }, message.correlation_id)
            elif command == "learn_fact" or command == "store":
                category = payload.get("category", "KNOWLEDGE")
                key = payload.get("key", "")
                value = payload.get("value", payload.get("text", ""))
                if value:
                    mid = memory.learn_fact(category, key, str(value))
                    self.semantic.add_memory(str(value), {"category": category, "key": key})
                    await self.send_response(message.sender, {"status": "success", "memory_id": mid}, message.correlation_id)
                else:
                    await self.send_response(message.sender, {"status": "error", "error": "No value provided"}, message.correlation_id)
            elif command == "recall_fact":
                category = payload.get("category")
                key = payload.get("key")
                facts = memory.recall_fact(category, key)
                await self.send_response(message.sender, {
                    "status": "success", "facts": [{"category": f.category, "key": f.key, "value": f.value} for f in facts]
                }, message.correlation_id)
            elif command == "record_episode":
                session_id = payload.get("session_id", "")
                action = payload.get("action", "")
                content = payload.get("content", "")
                result = payload.get("result", "")
                eid = memory.record_episode(session_id, action, content, result)
                await self.send_response(message.sender, {"status": "success", "episode_id": eid}, message.correlation_id)
            elif command == "update_preference":
                key = payload.get("key", "")
                value = payload.get("value", "")
                mid = memory.update_preference(key, value)
                await self.send_response(message.sender, {"status": "success", "memory_id": mid}, message.correlation_id)
            else:
                await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
        except Exception as e:
            logger.error("Memory agent error: %s", e)
            await self.send_response(message.sender, {"status": "error", "error": str(e)}, message.correlation_id)
