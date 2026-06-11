from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import asyncio

from core.jarvis_core import Session, IntentResult
from jarvis.cancellation_token import CancellationTokenSource


class TestSession:
    def test_session_creation(self):
        session = Session(id="test123")
        assert session.id == "test123"
        assert session.message_count == 0
        assert len(session.context) == 0

    def test_add_context(self):
        session = Session(id="test")
        session.add_context("user", "hello")
        assert len(session.context) == 1
        assert session.context[0]["role"] == "user"
        assert session.context[0]["content"] == "hello"
        assert session.message_count == 1

    def test_context_trimming(self):
        session = Session(id="test", max_context=3)
        session.add_context("system", "system msg")
        session.add_context("user", "msg1")
        session.add_context("user", "msg2")
        session.add_context("user", "msg3")
        assert len(session.context) <= 3

    def test_context_preserves_system(self):
        session = Session(id="test", max_context=3)
        session.add_context("system", "you are jarvis")
        session.add_context("user", "a")
        session.add_context("user", "b")
        session.add_context("user", "c")
        system_msgs = [c for c in session.context if c.get("role") == "system"]
        assert len(system_msgs) >= 1

    def test_touch(self):
        session = Session(id="test")
        old = session.last_activity
        time.sleep(0.01)
        session.touch()
        assert session.last_activity > old

    def test_to_dict(self):
        session = Session(id="test")
        session.add_context("user", "hi")
        d = session.to_dict()
        assert d["id"] == "test"
        assert d["message_count"] == 1
        assert len(d["context"]) == 1


class TestIntentResult:
    def test_creation(self):
        ir = IntentResult(intent="browser", confidence=0.9, target_agent="browser", params={"url": "x"})
        assert ir.intent == "browser"
        assert ir.confidence == 0.9

    def test_default_params(self):
        ir = IntentResult(intent="chat", confidence=0.5, target_agent="general")
        assert ir.params == {}


class TestCancellationToken:
    @pytest.mark.asyncio
    async def test_cancel(self):
        cts = CancellationTokenSource()
        token = cts.token
        assert not token.is_cancellation_requested
        cts.cancel()
        assert token.is_cancellation_requested

    def test_cancel_throws(self):
        cts = CancellationTokenSource()
        cts.cancel()
        with pytest.raises(asyncio.CancelledError):
            cts.token.throw_if_cancellation_requested()

    def test_linked_tokens(self):
        cts1 = CancellationTokenSource()
        cts2 = CancellationTokenSource()
        cts1.link(cts2)
        cts2.cancel()
        assert cts1.is_cancellation_requested

    def test_reset(self):
        cts = CancellationTokenSource()
        cts.cancel()
        assert cts.is_cancellation_requested
        cts.reset()
        assert not cts.is_cancellation_requested

    def test_linked_token_propagation(self):
        cts1 = CancellationTokenSource()
        cts2 = CancellationTokenSource()
        cts3 = CancellationTokenSource()
        cts1.link(cts2)
        cts2.link(cts3)
        cts3.cancel()
        assert cts1.is_cancellation_requested
        assert cts2.is_cancellation_requested

    def test_register_callback(self):
        cts = CancellationTokenSource()
        called = False
        def cb():
            nonlocal called
            called = True
        cts.register(cb)
        cts.cancel()
        assert called

    def test_double_cancel_no_error(self):
        cts = CancellationTokenSource()
        cts.cancel()
        cts.cancel()
        assert cts.is_cancellation_requested
