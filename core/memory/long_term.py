"""Long-term semantic memory backed by ChromaDB.

Provides ``remember`` / ``recall`` for persistent fact storage with
semantic similarity search.  All heavy lifting is lazy — the collection
is created on first read/write.
"""

from __future__ import annotations

import hashlib
import time
from typing import Any

from loguru import logger


class LongTermMemory:
    """Persistent vector store for semantic recall.

    Parameters
    ----------
    persist_dir : str
        Directory for ChromaDB on-disk persistence.
    collection_name : str
        Name of the ChromaDB collection.
    embedding_model : str
        Sentence-transformer model for embeddings (downloaded on first use).
    """

    def __init__(
        self,
        *,
        persist_dir: str = "data/chroma",
        collection_name: str = "jarvis_memory",
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        self._persist_dir = persist_dir
        self._collection_name = collection_name
        self._embedding_model = embedding_model
        self._client: Any | None = None
        self._collection: Any | None = None

    # -- Lazy init -----------------------------------------------------------

    def _ensure_collection(self) -> Any:
        if self._collection is not None:
            return self._collection

        try:
            import chromadb
            from chromadb.config import Settings

            self._client = chromadb.Client(
                Settings(
                    persist_directory=self._persist_dir,
                    anonymized_telemetry=False,
                    is_persistent=True,
                )
            )
            self._collection = self._client.get_or_create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(
                "LongTermMemory: collection '{}' ready ({} docs)",
                self._collection_name,
                self._collection.count(),
            )
        except Exception as exc:
            logger.error("LongTermMemory: ChromaDB init failed — {}", exc)
            raise
        return self._collection

    # -- Public API ----------------------------------------------------------

    def remember(
        self,
        text: str,
        *,
        metadata: dict[str, Any] | None = None,
        doc_id: str | None = None,
    ) -> str:
        """Store *text* as a memory.  Returns the document ID."""
        col = self._ensure_collection()
        did = doc_id or hashlib.sha256(text.encode()).hexdigest()[:16]

        meta: dict[str, Any] = {
            "timestamp": time.time(),
            "source": "user",
        }
        if metadata:
            meta.update(metadata)

        # Deduplicate: skip if same ID already stored
        existing = col.get(ids=[did])
        if existing and existing["ids"]:
            logger.debug("LongTermMemory: skipping duplicate id={}", did)
            return did

        col.add(
            ids=[did],
            documents=[text],
            metadatas=[meta],
        )
        logger.debug("LongTermMemory: stored id={} ({} chars)", did, len(text))
        return did

    def recall(self, query: str, n: int = 5) -> list[dict[str, Any]]:
        """Semantic similarity search.  Returns up to *n* results.

        Each result dict has keys ``id``, ``text``, ``distance``, ``metadata``.
        """
        col = self._ensure_collection()
        if col.count() == 0:
            return []

        results = col.query(query_texts=[query], n_results=min(n, col.count()))
        out: list[dict[str, Any]] = []
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        dists = results.get("distances", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        for i, doc_id in enumerate(ids):
            out.append(
                {
                    "id": doc_id,
                    "text": docs[i] if i < len(docs) else "",
                    "distance": dists[i] if i < len(dists) else 1.0,
                    "metadata": metas[i] if i < len(metas) else {},
                }
            )
        return out

    def count(self) -> int:
        return self._ensure_collection().count()

    def clear(self) -> None:
        """Delete all documents in the collection."""
        if self._client and self._collection:
            self._client.delete_collection(self._collection_name)
            self._collection = None
            logger.info("LongTermMemory: collection '{}' cleared", self._collection_name)

    def delete(self, doc_id: str) -> None:
        col = self._ensure_collection()
        col.delete(ids=[doc_id])
