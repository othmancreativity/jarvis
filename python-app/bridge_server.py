from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Callable

from security.audit import audit_logger, AuditEventType, SecuritySeverity
from config import config

logger = logging.getLogger("jarvis.bridge")

try:
    from websockets.server import WebSocketServerProtocol
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False
    WebSocketServerProtocol = None


@dataclass
class BridgeCommand:
    command_id: str
    action: str
    params: dict
    requires_confirmation: bool
    timeout_ms: int = 30000
    source: str = "n8n"
    timestamp: float = field(default_factory=time.time)


@dataclass
class BridgeResponse:
    command_id: str
    status: str
    result: dict = field(default_factory=dict)
    execution_ms: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "command_id": self.command_id,
            "status": self.status,
            "result": self.result,
            "execution_ms": self.execution_ms,
        }


class BridgeServer:
    def __init__(self, confirmation_callback: Optional[Callable] = None) -> None:
        self.confirmation_callback = confirmation_callback or self._default_confirmation
        self._running = False
        self._server = None
        self._clients: set = set()

    def _default_confirmation(self, action: str, target: str, risk: str) -> dict:
        logger.warning("SAFETY: %s on %s - %s", action, target, risk)
        return {"confirmed": True}

    async def handle_client(self, ws, path: str) -> None:
        self._clients.add(ws)
        logger.info("Bridge client connected")
        try:
            async for message in ws:
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "")

                    if msg_type == "ping":
                        await ws.send(json.dumps({"type": "pong"}))
                    elif msg_type == "command":
                        payload = data.get("payload", {})
                        cmd = BridgeCommand(
                            command_id=payload.get("command_id", ""),
                            action=payload.get("action", ""),
                            params=payload.get("params", {}),
                            requires_confirmation=payload.get("requires_confirmation", False),
                            timeout_ms=payload.get("timeout_ms", 30000),
                        )

                        start = datetime.utcnow()
                        if cmd.requires_confirmation:
                            result = self.confirmation_callback(cmd.action, str(cmd.params), "Remote command")
                            if not result.get("confirmed"):
                                resp = BridgeResponse(command_id=cmd.command_id, status="denied")
                                await ws.send(json.dumps({"type": "response", "payload": resp.to_dict()}))
                                continue

                        try:
                            from automation.browser import BrowserController
                            from automation.apps import AppController
                            from automation.shell import ShellController
                            from automation.files import FileController
                            from automation.system_info import SystemInfoController

                            handlers = {
                                "screenshot": lambda p: BrowserController().screenshot(**p),
                                "browser_open": lambda p: BrowserController().open(**p),
                                "browser_navigate": lambda p: BrowserController().navigate(p.get("url", "")),
                                "browser_close": lambda p: BrowserController().close(),
                                "app_open": lambda p: AppController().open(p.get("app_name", "")),
                                "app_close": lambda p: AppController().close(p.get("app_name", "")),
                                "app_list_running": lambda p: AppController().list_running(),
                                "file_list": lambda p: FileController().list_dir(p.get("path", "~")),
                                "file_read": lambda p: FileController().read_file(p.get("path", "")),
                                "shell_exec": lambda p: ShellController().execute(p.get("command", "")),
                                "system_info": lambda p: SystemInfoController().get_info(),
                            }

                            handler = handlers.get(cmd.action)
                            if handler:
                                result = await handler(cmd.params)
                            else:
                                result = {"status": "error", "error": f"Unknown action: {cmd.action}"}

                        except Exception as e:
                            result = {"status": "error", "error": str(e)}

                        duration = int((datetime.utcnow() - start).total_seconds() * 1000)
                        resp = BridgeResponse(
                            command_id=cmd.command_id,
                            status=result.get("status", "success"),
                            result=result,
                            execution_ms=duration,
                        )
                        await ws.send(json.dumps({"type": "response", "payload": resp.to_dict()}))
                    else:
                        await ws.send(json.dumps({"type": "error", "payload": {"error": f"Unknown type: {msg_type}"}}))
                except json.JSONDecodeError:
                    await ws.send(json.dumps({"type": "error", "payload": {"error": "Invalid JSON"}}))
        except Exception:
            pass
        finally:
            self._clients.discard(ws)
            logger.info("Bridge client disconnected")

    async def start(self) -> None:
        if not HAS_WEBSOCKETS:
            logger.error("websockets not installed")
            return
        self._running = True
        import websockets
        self._server = await websockets.serve(
            self.handle_client,
            config.bridge_host,
            config.bridge_port,
            ping_interval=30,
            ping_timeout=10,
        )
        logger.info("Bridge server started on ws://%s:%s", config.bridge_host, config.bridge_port)
        await self._server.wait_closed()

    async def stop(self) -> None:
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()


async def main():
    logging.basicConfig(level=logging.INFO)
    server = BridgeServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
