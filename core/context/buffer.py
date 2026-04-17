"""Context Buffer: multimodal input staging before execution.

Accepts text, files, images, and audio *references*; provides a merged
snapshot for the runtime Observe step and lightweight metadata for the
Decision Layer.  **No heavy models run here** — transcription, vision,
and embeddings happen downstream in Act/Think.
"""

from __future__ import annotations

import mimetypes
import os
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from loguru import logger


class InputType(str, Enum):
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    AUDIO = "audio"


@dataclass
class BufferItem:
    """One staged input in the buffer."""

    input_id: str
    input_type: InputType
    content: str  # text content or file path
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def summary(self, max_len: int = 120) -> str:
        """One-line human summary for Observe."""
        if self.input_type == InputType.TEXT:
            preview = self.content[:max_len].replace("\n", " ")
            return f"[text] {preview}"
        name = Path(self.content).name if self.content else "unknown"
        size = self.metadata.get("size_bytes", "?")
        return f"[{self.input_type.value}] {name} ({size} bytes)"


class ContextBuffer:
    """Ephemeral session staging for multimodal inputs.

    Parameters
    ----------
    ttl_seconds : float
        Idle TTL before stale items are evicted (0 = no eviction).
    max_items : int
        Hard cap on buffered items.
    """

    def __init__(self, *, ttl_seconds: float = 600, max_items: int = 20) -> None:
        self._items: list[BufferItem] = []
        self._ttl = ttl_seconds
        self._max_items = max_items

    # -- Enqueue -------------------------------------------------------------

    def add_text(self, text: str) -> str:
        """Stage a text input.  Returns the ``input_id``."""
        return self._add(InputType.TEXT, text, metadata={"char_count": len(text)})

    def add_file(self, path: str | Path) -> str:
        """Stage a file reference with lightweight metadata."""
        p = Path(path)
        meta = self._file_metadata(p)
        itype = self._classify_file(p)
        return self._add(itype, str(p), metadata=meta)

    def add_image(self, path: str | Path) -> str:
        """Stage an image reference."""
        p = Path(path)
        meta = self._file_metadata(p)
        meta["is_image"] = True
        return self._add(InputType.IMAGE, str(p), metadata=meta)

    def add_audio(self, path: str | Path) -> str:
        """Stage an audio reference (no transcription here)."""
        p = Path(path)
        meta = self._file_metadata(p)
        return self._add(InputType.AUDIO, str(p), metadata=meta)

    def _add(self, itype: InputType, content: str, metadata: dict[str, Any]) -> str:
        self._evict_stale()
        if len(self._items) >= self._max_items:
            removed = self._items.pop(0)
            logger.debug("ContextBuffer: evicted oldest item {}", removed.input_id)

        iid = uuid.uuid4().hex[:10]
        item = BufferItem(input_id=iid, input_type=itype, content=content, metadata=metadata)
        self._items.append(item)
        logger.debug("ContextBuffer: added {} ({})", iid, itype.value)
        return iid

    # -- Lightweight metadata ------------------------------------------------

    @staticmethod
    def _file_metadata(p: Path) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "filename": p.name,
            "extension": p.suffix.lower(),
            "mime": mimetypes.guess_type(str(p))[0] or "application/octet-stream",
        }
        if p.exists():
            meta["size_bytes"] = p.stat().st_size
        return meta

    @staticmethod
    def _classify_file(p: Path) -> InputType:
        ext = p.suffix.lower()
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"):
            return InputType.IMAGE
        if ext in (".wav", ".mp3", ".ogg", ".flac", ".m4a", ".webm"):
            return InputType.AUDIO
        return InputType.FILE

    # -- Snapshot for Observe ------------------------------------------------

    def snapshot(self) -> list[BufferItem]:
        """Return a copy of all buffered items (for Observe to read)."""
        self._evict_stale()
        return list(self._items)

    def merged_summary(self) -> str:
        """Compact text summary of all buffered inputs for the Decision Layer."""
        if not self._items:
            return ""
        lines = [item.summary() for item in self._items]
        return "Buffered inputs:\n" + "\n".join(f"  {i+1}. {l}" for i, l in enumerate(lines))

    def modality_flags(self) -> dict[str, bool]:
        """Quick modality check for Decision Layer."""
        types = {item.input_type for item in self._items}
        return {
            "has_text": InputType.TEXT in types,
            "has_file": InputType.FILE in types,
            "has_image": InputType.IMAGE in types,
            "has_audio": InputType.AUDIO in types,
        }

    def text_content(self) -> str:
        """Merge all text items into one string (for simple single-text turns)."""
        return "\n".join(
            item.content for item in self._items if item.input_type == InputType.TEXT
        )

    # -- Lifecycle -----------------------------------------------------------

    def clear(self) -> None:
        """Clear all buffered items (after execute / turn completion)."""
        count = len(self._items)
        self._items.clear()
        if count:
            logger.debug("ContextBuffer: cleared {} items", count)

    def remove(self, input_id: str) -> bool:
        """Remove a specific item by ID."""
        for i, item in enumerate(self._items):
            if item.input_id == input_id:
                self._items.pop(i)
                return True
        return False

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    # -- TTL eviction --------------------------------------------------------

    def _evict_stale(self) -> None:
        if self._ttl <= 0:
            return
        cutoff = time.time() - self._ttl
        before = len(self._items)
        self._items = [item for item in self._items if item.timestamp >= cutoff]
        evicted = before - len(self._items)
        if evicted:
            logger.debug("ContextBuffer: evicted {} stale items", evicted)
