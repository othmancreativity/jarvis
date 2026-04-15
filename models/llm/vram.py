"""Serialize access to a single heavy Ollama model at a time (best-effort)."""

from __future__ import annotations

import threading
import time
from typing import Callable


class VramGuard:
    """Track active model id; optional hook before swap (e.g. unload — Ollama manages VRAM)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._active: str | None = None

    @property
    def active_model(self) -> str | None:
        return self._active

    def prepare(self, model_id: str, *, on_swap: Callable[[str | None, str], None] | None = None) -> None:
        """Mark intent to use ``model_id``; call ``on_swap(old, new)`` if model changes."""
        with self._lock:
            old = self._active
            if old != model_id:
                if on_swap:
                    on_swap(old, model_id)
                self._active = model_id
                # Tiny pause so GPU can release (tunable)
                time.sleep(0.05)
