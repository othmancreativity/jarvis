"""FastAPI app: REST ``/chat`` and WebSocket streaming."""

from __future__ import annotations

import json
import logging
from typing import Any, TYPE_CHECKING

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from core.bootstrap import get_chat_service
from settings.logging import setup_logging

if TYPE_CHECKING:
    from settings.app_settings import AppSettings

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Incoming chat payload for ``/chat``."""

    message: str = Field(..., min_length=1, description="User message text.")


class ChatResponse(BaseModel):
    """Non-streaming JSON response."""

    reply: str
    model: str
    route: str
    reason: str


def create_app(settings: "AppSettings | None" = None) -> FastAPI:
    """Build and return the ASGI application."""
    from settings.loader import load_settings

    resolved = settings or load_settings()
    setup_logging(level=resolved.logging.level)
    app = FastAPI(title="Jarvis", version="0.1.0")
    service = get_chat_service(resolved)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Liveness probe."""
        return {"status": "ok", "name": "Jarvis"}

    @app.post("/chat", response_model=ChatResponse)
    def chat(req: ChatRequest) -> JSONResponse:
        """Return a full assistant reply (buffered, non-streaming)."""
        decision, chunks = service.stream_reply(req.message)
        reply = "".join(chunks)
        body = ChatResponse(
            reply=reply,
            model=decision.model,
            route=decision.kind.value,
            reason=decision.reason,
        )
        return JSONResponse(content=body.model_dump())

    @app.post("/chat/stream")
    def chat_stream(req: ChatRequest) -> StreamingResponse:
        """Stream the assistant reply as UTF-8 plain text."""

        def gen() -> Any:
            _decision, chunks = service.stream_reply(req.message)
            for part in chunks:
                yield part

        return StreamingResponse(gen(), media_type="text/plain; charset=utf-8")

    @app.websocket("/ws/chat")
    async def ws_chat(ws: WebSocket) -> None:
        """Stream tokens over WebSocket (JSON text frames)."""
        await ws.accept()
        try:
            raw = await ws.receive_text()
            payload: dict[str, Any] = json.loads(raw)
            message = str(payload.get("message", "")).strip()
            if not message:
                await ws.send_text(
                    json.dumps({"type": "error", "detail": "empty message"}, ensure_ascii=False)
                )
                await ws.close()
                return

            decision, chunks = service.stream_reply(message)
            await ws.send_text(
                json.dumps(
                    {
                        "type": "meta",
                        "model": decision.model,
                        "route": decision.kind.value,
                        "reason": decision.reason,
                    },
                    ensure_ascii=False,
                )
            )
            for part in chunks:
                if part:
                    await ws.send_text(json.dumps({"type": "token", "text": part}, ensure_ascii=False))
            await ws.send_text(json.dumps({"type": "done"}, ensure_ascii=False))
        except WebSocketDisconnect:
            logger.info("WebSocket client disconnected")
        except Exception:
            logger.exception("WebSocket handler error")
            try:
                await ws.send_text(json.dumps({"type": "error", "detail": "internal"}, ensure_ascii=False))
            except Exception:
                pass
            await ws.close()

    return app


app = create_app()
