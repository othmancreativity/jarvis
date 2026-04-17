"""Phase 2.8 — Orchestrator streams tokens with mocked Ollama."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from settings.loader import load_settings
from core.brain.orchestrator import ChatOrchestrator, stream_reply_chunks


def test_chat_orchestrator_streams_mocked_engine() -> None:
    settings = load_settings()
    # Long enough reply so evaluation doesn't trigger escalation
    reply_text = "Hello world. This is a complete and helpful response to your greeting."
    fake_stream = iter(
        [
            {"message": {"content": reply_text}},
        ]
    )
    engine = MagicMock()
    engine.chat.return_value = fake_stream

    orch = ChatOrchestrator(settings, engine=engine)
    out = "".join(orch.stream_tokens("hi"))
    assert reply_text in out
    # Engine should be called at least once (may escalate for short replies)
    assert engine.chat.call_count >= 1
    # First call must be streaming
    first_call = engine.chat.call_args_list[0]
    assert first_call.kwargs.get("stream") is True


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
