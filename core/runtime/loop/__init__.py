"""
Observe → Decide → Think → Act → Evaluate → (Escalate | Finish).

The live implementation is :class:`core.brain.orchestrator.ChatOrchestrator`
(``stream_tokens`` / ``stream_reply_chunks``). Tool **Act** steps delegate to
:class:`core.runtime.executor.facade.ToolExecutor` in later phases when skills run.
"""

from __future__ import annotations

from core.brain.orchestrator import ChatOrchestrator, stream_reply_chunks

__all__ = ["ChatOrchestrator", "stream_reply_chunks"]
