"""User profiling: adaptive memory for learned preferences and patterns.

Stored as a JSON file keyed by user/session ID.  Provides priors for
the Decision Layer (language bias, task patterns, response style).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from loguru import logger


class UserProfile:
    """Per-user adaptive profile: preferences, patterns, and stats.

    Parameters
    ----------
    user_id : str
        Unique user identifier (or session fallback).
    profiles_dir : str | Path
        Directory where profile JSON files are stored.
    """

    def __init__(
        self,
        user_id: str = "default",
        profiles_dir: str | Path = "data/profiles",
    ) -> None:
        self._user_id = user_id
        self._dir = Path(profiles_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._path = self._dir / f"{user_id}.json"
        self._data: dict[str, Any] = self._load()

    # -- Persistence ---------------------------------------------------------

    def _default_profile(self) -> dict[str, Any]:
        return {
            "user_id": self._user_id,
            "version": 1,
            "created_at": time.time(),
            "updated_at": time.time(),

            # Preferences
            "preferred_language": "ar",  # ar | en | auto
            "response_style": "balanced",  # concise | balanced | detailed
            "formality": "casual",  # formal | casual | warm
            "technical_level": "intermediate",  # beginner | intermediate | expert

            # Adaptive counters (feed Decision Layer priors)
            "task_counts": {
                "chat": 0,
                "code": 0,
                "research": 0,
                "action": 0,
            },
            "total_interactions": 0,
            "avg_message_length": 0.0,
            "preferred_mode": "normal",  # fast | normal | deep

            # Failure / success patterns
            "recent_failures": 0,
            "success_streak": 0,
        }

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.debug("UserProfile: loaded profile for '{}'", self._user_id)
                return data
            except Exception as exc:
                logger.warning("UserProfile: failed to load '{}': {}", self._path, exc)
        return self._default_profile()

    def save(self) -> None:
        self._data["updated_at"] = time.time()
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("UserProfile: failed to save: {}", exc)

    # -- Getters -------------------------------------------------------------

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def preferred_language(self) -> str:
        return self._data.get("preferred_language", "ar")

    @property
    def response_style(self) -> str:
        return self._data.get("response_style", "balanced")

    @property
    def formality(self) -> str:
        return self._data.get("formality", "casual")

    @property
    def technical_level(self) -> str:
        return self._data.get("technical_level", "intermediate")

    @property
    def preferred_mode(self) -> str:
        return self._data.get("preferred_mode", "normal")

    @property
    def total_interactions(self) -> int:
        return self._data.get("total_interactions", 0)

    @property
    def task_counts(self) -> dict[str, int]:
        return self._data.get("task_counts", {})

    @property
    def is_code_heavy(self) -> bool:
        counts = self.task_counts
        total = sum(counts.values())
        if total < 5:
            return False
        return counts.get("code", 0) / total > 0.4

    @property
    def recent_failures(self) -> int:
        return self._data.get("recent_failures", 0)

    # -- Updaters ------------------------------------------------------------

    def record_interaction(self, intent: str, message_length: int) -> None:
        """Update counters after a turn."""
        self._data["total_interactions"] = self._data.get("total_interactions", 0) + 1

        counts = self._data.setdefault("task_counts", {})
        counts[intent] = counts.get(intent, 0) + 1

        # Running average of message length
        n = self._data["total_interactions"]
        prev_avg = self._data.get("avg_message_length", 0.0)
        self._data["avg_message_length"] = prev_avg + (message_length - prev_avg) / n

        self.save()

    def record_success(self) -> None:
        self._data["success_streak"] = self._data.get("success_streak", 0) + 1
        self._data["recent_failures"] = max(0, self._data.get("recent_failures", 0) - 1)
        self.save()

    def record_failure(self) -> None:
        self._data["recent_failures"] = self._data.get("recent_failures", 0) + 1
        self._data["success_streak"] = 0
        self.save()

    def update(self, **fields: Any) -> None:
        """Update arbitrary profile fields."""
        allowed = {
            "preferred_language", "response_style", "formality",
            "technical_level", "preferred_mode",
        }
        for k, v in fields.items():
            if k in allowed:
                self._data[k] = v
        self.save()

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    def reset(self) -> None:
        self._data = self._default_profile()
        self.save()
