from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.local_llm")

try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False
    ollama = None


@dataclass
class LLMCacheEntry:
    prompt: str
    response: str
    timestamp: float = field(default_factory=time.time)

    @property
    def age(self) -> float:
        return time.time() - self.timestamp


class LocalLLM:
    """Integration with Ollama for local LLM inference.

    Automatically switches to local model when Groq API fails or
    network is unavailable. Caches common responses to reduce latency.
    """

    DEFAULT_MODEL = "llama3.2:3b"
    FALLBACK_MODEL = "llama3.2:1b"
    CACHE_TTL = 3600  # 1 hour
    CACHE_MAX_SIZE = 100

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self._model: str = model
        self._fallback_model: str = self.FALLBACK_MODEL
        self._available: bool = False
        self._cache: dict[str, LLMCacheEntry] = {}
        self._cache_dir: Path = paths.cache_dir / "llm_cache.json"
        self._load_cache()

    async def check_availability(self) -> bool:
        if not HAS_OLLAMA:
            self._available = False
            return False
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: ollama.list()
            )
            self._available = True
            return True
        except Exception:
            self._available = False
            return False

    @property
    def is_available(self) -> bool:
        return self._available

    async def generate(self, messages: list[dict], temperature: float = 0.3,
                       max_tokens: int = 2000, use_fallback: bool = False) -> Optional[str]:
        if not self._available and not use_fallback:
            return None

        prompt_text = json.dumps(messages, sort_keys=True)
        cache_key = hashlib.sha256(prompt_text.encode()).hexdigest()

        cached = self._check_cache(cache_key)
        if cached:
            return cached

        model = self._fallback_model if use_fallback else self._model
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: ollama.chat(
                    model=model,
                    messages=messages,
                    options={"temperature": temperature, "num_predict": max_tokens},
                )
            )
            text = response.get("message", {}).get("content", "")
            self._update_cache(cache_key, prompt_text, text)
            return text
        except Exception as e:
            logger.error("Local LLM generate error: %s", e)
            if not use_fallback:
                return await self.generate(messages, temperature, max_tokens, use_fallback=True)
            return None

    async def streaming_generate(self, messages: list[dict], temperature: float = 0.3,
                                  max_tokens: int = 2000):
        if not self._available:
            return
        try:
            stream = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: list(ollama.chat(
                    model=self._model,
                    messages=messages,
                    stream=True,
                    options={"temperature": temperature, "num_predict": max_tokens},
                ))
            )
            for chunk in stream:
                yield chunk.get("message", {}).get("content", "")
        except Exception as e:
            logger.error("Local LLM streaming error: %s", e)

    def _check_cache(self, key: str) -> Optional[str]:
        entry = self._cache.get(key)
        if entry and entry.age < self.CACHE_TTL:
            return entry.response
        if entry:
            del self._cache[key]
        return None

    def _update_cache(self, key: str, prompt: str, response: str) -> None:
        self._cache[key] = LLMCacheEntry(prompt=prompt, response=response)
        if len(self._cache) > self.CACHE_MAX_SIZE:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest]

    def _load_cache(self) -> None:
        if self._cache_dir.exists():
            try:
                data = json.loads(self._cache_dir.read_text(encoding="utf-8"))
                for k, v in data.items():
                    self._cache[k] = LLMCacheEntry(**v)
            except Exception:
                pass

    def _save_cache(self) -> None:
        try:
            self._cache_dir.parent.mkdir(parents=True, exist_ok=True)
            data = {k: {"prompt": v.prompt, "response": v.response, "timestamp": v.timestamp}
                    for k, v in self._cache.items()}
            self._cache_dir.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass


local_llm = LocalLLM()
