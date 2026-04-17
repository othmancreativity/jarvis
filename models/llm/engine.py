"""Ollama HTTP client wrapper: chat + generate with exponential backoff, timing, and streaming."""

from __future__ import annotations

import time
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import ollama
from loguru import logger

from models.llm.profiles import ModelProfile


class LLMEngineError(RuntimeError):
    """Raised when Ollama returns an error after retries."""


@dataclass
class CallMetrics:
    """Timing and stats for a single LLM call."""

    model: str = ""
    elapsed_s: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    attempts: int = 1
    streaming: bool = False


def _messages_to_ollama(messages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for m in messages:
        role = str(m.get("role", "user"))
        content = str(m.get("content", ""))
        out.append({"role": role, "content": content})
    return out


class LLMEngine:
    """Thin wrapper around ``ollama.Client`` with exponential retry and streaming support.

    Parameters
    ----------
    host : str | None
        Ollama server URL (default: localhost:11434).
    max_retries : int
        Maximum number of attempts before raising.
    base_delay_s : float
        Base delay for exponential backoff (delay = base * 2^attempt).
    max_delay_s : float
        Cap on backoff delay to avoid excessive waits.
    timeout_s : float
        Per-request timeout in seconds.
    """

    def __init__(
        self,
        *,
        host: str | None = None,
        max_retries: int = 3,
        base_delay_s: float = 0.5,
        max_delay_s: float = 10.0,
        timeout_s: float = 120.0,
    ) -> None:
        self._client = ollama.Client(host=host, timeout=timeout_s) if host else ollama.Client(timeout=timeout_s)
        self._max_retries = max_retries
        self._base_delay = base_delay_s
        self._max_delay = max_delay_s
        self._last_metrics: CallMetrics | None = None

    @property
    def last_metrics(self) -> CallMetrics | None:
        """Metrics from the most recent call (for observability)."""
        return self._last_metrics

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with cap."""
        return min(self._base_delay * (2 ** attempt), self._max_delay)

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

    def _extract_metrics(self, response: dict[str, Any], model: str, attempts: int, t0: float, streaming: bool) -> CallMetrics:
        """Extract timing + token counts from Ollama response."""
        elapsed = time.monotonic() - t0
        return CallMetrics(
            model=model,
            elapsed_s=round(elapsed, 3),
            prompt_tokens=response.get("prompt_eval_count", 0),
            completion_tokens=response.get("eval_count", 0),
            attempts=attempts,
            streaming=streaming,
        )

    # -- Chat ----------------------------------------------------------------

    def chat(
        self,
        messages: Sequence[Mapping[str, str]],
        model: str,
        *,
        profile: ModelProfile | None = None,
        stream: bool = False,
        extra_options: Mapping[str, Any] | None = None,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        """Chat completion — streaming or buffered."""
        if stream:
            return self._chat_stream(messages, model, profile=profile, extra_options=extra_options)
        return self._chat_once(messages, model, profile=profile, extra_options=extra_options)

    def _chat_once(
        self,
        messages: Sequence[Mapping[str, str]],
        model: str,
        *,
        profile: ModelProfile | None,
        extra_options: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        opts = self._options(profile, extra_options)
        prepared = _messages_to_ollama(messages)
        last_err: Exception | None = None
        t0 = time.monotonic()

        for attempt in range(self._max_retries):
            try:
                result = self._client.chat(
                    model=model,
                    messages=prepared,
                    options=opts or None,
                )
                self._last_metrics = self._extract_metrics(result, model, attempt + 1, t0, False)
                logger.debug(
                    "chat model={} tokens={}+{} elapsed={:.2f}s attempts={}",
                    model,
                    self._last_metrics.prompt_tokens,
                    self._last_metrics.completion_tokens,
                    self._last_metrics.elapsed_s,
                    self._last_metrics.attempts,
                )
                return result
            except Exception as e:
                last_err = e
                delay = self._backoff_delay(attempt)
                logger.warning("ollama chat attempt {}/{} failed: {} (retry in {:.1f}s)", attempt + 1, self._max_retries, e, delay)
                if attempt < self._max_retries - 1:
                    time.sleep(delay)

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
        prepared = _messages_to_ollama(messages)
        last_err: Exception | None = None
        t0 = time.monotonic()

        for attempt in range(self._max_retries):
            try:
                stream = self._client.chat(
                    model=model,
                    messages=prepared,
                    stream=True,
                    options=opts or None,
                )
                last_chunk: dict[str, Any] = {}
                for chunk in stream:
                    last_chunk = chunk
                    yield chunk
                # Extract metrics from final chunk
                self._last_metrics = self._extract_metrics(last_chunk, model, attempt + 1, t0, True)
                return
            except Exception as e:
                last_err = e
                delay = self._backoff_delay(attempt)
                logger.warning("ollama stream attempt {}/{} failed: {} (retry in {:.1f}s)", attempt + 1, self._max_retries, e, delay)
                if attempt < self._max_retries - 1:
                    time.sleep(delay)

        raise LLMEngineError(f"Ollama stream failed after {self._max_retries} attempts: {last_err}") from last_err

    # -- Generate ------------------------------------------------------------

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
        t0 = time.monotonic()

        for attempt in range(self._max_retries):
            try:
                result = self._client.generate(
                    model=model,
                    prompt=prompt,
                    options=opts or None,
                )
                self._last_metrics = self._extract_metrics(result, model, attempt + 1, t0, False)
                return result
            except Exception as e:
                last_err = e
                delay = self._backoff_delay(attempt)
                logger.warning("ollama generate attempt {}/{} failed: {} (retry in {:.1f}s)", attempt + 1, self._max_retries, e, delay)
                if attempt < self._max_retries - 1:
                    time.sleep(delay)

        raise LLMEngineError(f"Ollama generate failed: {last_err}") from last_err

    # -- Health check --------------------------------------------------------

    def is_available(self) -> bool:
        """Quick liveness check — returns False if Ollama is unreachable."""
        try:
            self._client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """Return list of locally available model tags."""
        try:
            response = self._client.list()
            models = response.get("models", [])
            return [m.get("name", "") for m in models if m.get("name")]
        except Exception:
            return []


def stream_text_chunks(stream: Iterator[dict[str, Any]]) -> Iterator[str]:
    """Map Ollama stream chunks to text fragments."""
    for chunk in stream:
        msg = chunk.get("message") or {}
        piece = msg.get("content") or ""
        if piece:
            yield str(piece)
