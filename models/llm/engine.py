"""Ollama HTTP client wrapper: chat + generate with retries."""

from __future__ import annotations

import time
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

import ollama
from loguru import logger

from models.llm.profiles import ModelProfile


class LLMEngineError(RuntimeError):
    """Raised when Ollama returns an error after retries."""


def _messages_to_ollama(messages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for m in messages:
        role = str(m.get("role", "user"))
        content = str(m.get("content", ""))
        out.append({"role": role, "content": content})
    return out


class LLMEngine:
    """Thin wrapper around ``ollama.Client`` with retry and streaming support."""

    def __init__(
        self,
        *,
        host: str | None = None,
        max_retries: int = 3,
        retry_delay_s: float = 0.8,
    ) -> None:
        self._client = ollama.Client(host=host) if host else ollama.Client()
        self._max_retries = max_retries
        self._retry_delay_s = retry_delay_s

    def chat(
        self,
        messages: Sequence[Mapping[str, str]],
        model: str,
        *,
        profile: ModelProfile | None = None,
        stream: bool = False,
        extra_options: Mapping[str, Any] | None = None,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        """Non-streaming chat completion (full response dict)."""
        if stream:
            return self._chat_stream(messages, model, profile=profile, extra_options=extra_options)
        return self._chat_once(messages, model, profile=profile, extra_options=extra_options)

    def _options(self, profile: ModelProfile | None, extra: Mapping[str, Any] | None) -> dict[str, Any]:
        base: dict[str, Any] = {}
        if profile is not None:
            base = {
                "temperature": profile.temperature,
                "top_p": profile.top_p,
                "num_predict": profile.max_tokens,
            }
        if extra:
            base.update(dict(extra))
        return base

    def _chat_once(
        self,
        messages: Sequence[Mapping[str, str]],
        model: str,
        *,
        profile: ModelProfile | None,
        extra_options: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        opts = self._options(profile, extra_options)
        last_err: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                return self._client.chat(
                    model=model,
                    messages=_messages_to_ollama(messages),
                    options=opts or None,
                )
            except Exception as e:
                last_err = e
                logger.warning("ollama chat attempt {} failed: {}", attempt + 1, e)
                time.sleep(self._retry_delay_s * (attempt + 1))
        raise LLMEngineError(f"Ollama chat failed after {self._max_retries} attempts: {last_err}") from last_err

    def _chat_stream(
        self,
        messages: Sequence[Mapping[str, str]],
        model: str,
        *,
        profile: ModelProfile | None,
        extra_options: Mapping[str, Any] | None,
    ) -> Iterator[dict[str, Any]]:
        opts = self._options(profile, extra_options)
        last_err: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                stream = self._client.chat(
                    model=model,
                    messages=_messages_to_ollama(messages),
                    stream=True,
                    options=opts or None,
                )
                for chunk in stream:
                    yield chunk
                return
            except Exception as e:
                last_err = e
                logger.warning("ollama stream attempt {} failed: {}", attempt + 1, e)
                time.sleep(self._retry_delay_s * (attempt + 1))
        raise LLMEngineError(f"Ollama stream failed after {self._max_retries} attempts: {last_err}") from last_err

    def generate(
        self,
        prompt: str,
        model: str,
        *,
        profile: ModelProfile | None = None,
        extra_options: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Single-turn completion (no chat history)."""
        opts = self._options(profile, extra_options)
        last_err: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                return self._client.generate(
                    model=model,
                    prompt=prompt,
                    options=opts or None,
                )
            except Exception as e:
                last_err = e
                logger.warning("ollama generate attempt {} failed: {}", attempt + 1, e)
                time.sleep(self._retry_delay_s * (attempt + 1))
        raise LLMEngineError(f"Ollama generate failed: {last_err}") from last_err


def stream_text_chunks(stream: Iterator[dict[str, Any]]) -> Iterator[str]:
    """Map Ollama stream chunks to text fragments."""
    for chunk in stream:
        msg = chunk.get("message") or {}
        piece = msg.get("content") or ""
        if piece:
            yield str(piece)
