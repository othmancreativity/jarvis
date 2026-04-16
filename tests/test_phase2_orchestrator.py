"""Phase 2.8 — Orchestrator streams tokens with mocked Ollama."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from settings.loader import load_settings
from core.brain.orchestrator import ChatOrchestrator, stream_reply_chunks


def test_chat_orchestrator_streams_mocked_engine() -> None:
    settings = load_settings()
    fake_stream = iter(
        [
            {"message": {"content": "Hello"}},
            {"message": {"content": " world"}},
        ]
    )
    engine = MagicMock()
    engine.chat.return_value = fake_stream

    orch = ChatOrchestrator(settings, engine=engine)
    out = "".join(orch.stream_tokens("hi"))
    assert "Hello" in out
    assert "world" in out
    engine.chat.assert_called_once()
    assert engine.chat.call_args.kwargs.get("stream") is True


def test_stream_reply_chunks_returns_llm_route() -> None:
    settings = load_settings()
    # Long enough reply for evaluate_reply to finish in one pass (avoid escalation loop).
    long_text = "A complete assistant reply. " * 40
    mock_engine = MagicMock()
    mock_engine.chat.return_value = iter([{"message": {"content": long_text}}])

    with patch("core.brain.orchestrator.LLMEngine", return_value=mock_engine):
        dec, chunks = stream_reply_chunks(settings, "hello there")

    assert dec.kind.value == "llm"
    assert long_text in "".join(chunks)
