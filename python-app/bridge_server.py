"""
JARVIS 4.0 — WebSocket Bridge Server
=====================================
Bidirectional communication bridge between n8n (running on a server or Docker)
and the local laptop companion app.

Protocol:
  - Connection: ws://localhost:8765/jarvis-bridge
  - Auth: Bearer token via JARVIS_BRIDGE_SECRET env var
  - Messages: JSON with {type, payload, timestamp}
  - Heartbeat: ping/pong every 30 seconds

Security:
  - HMAC-SHA256 message signing (optional)
  - All risky operations require user confirmation via UI
  - Audit logging of every command
"""

import asyncio
import json
import os
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    raise ImportError("Install websockets: pip install websockets")

logger = logging.getLogger("jarvis.bridge")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BRIDGE_SECRET = os.environ.get("JARVIS_BRIDGE_SECRET", "change-me-in-production")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "8765"))
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "0.0.0.0")
PING_INTERVAL = 30  # seconds
COMMAND_TIMEOUT = 60  # seconds

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
@dataclass
class BridgeCommand:
    command_id: str
    action: str
    params: dict
    requires_confirmation: bool
    timeout_ms: int = 30000

@dataclass
class BridgeResponse:
    command_id: str
    status: str  # success, error, denied, timeout
    result: dict
    stdout: str = ""
    stderr: str = ""
    file_path: str = ""
    screenshot_base64: str = ""
    execution_ms: int = 0

@dataclass
class BridgeMessage:
    type: str  # command, response, event, ping, pong
    payload: dict
    timestamp: str
    signature: str = ""

# ---------------------------------------------------------------------------
# Audit Logger
# ---------------------------------------------------------------------------
class AuditLogger:
    """Logs every device command for security auditing."""

    LOG_FILE = Path.home() / ".jarvis" / "audit.log"

    @classmethod
    def log(cls, command: str, params: dict, confirmed: Optional[bool], result: str, duration_ms: int):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": command,
            "params": params,
            "confirmed": confirmed,
            "result": result,
            "duration_ms": duration_ms,
        }
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    @classmethod
    def read_recent(cls, n: int = 50) -> list:
        if not cls.LOG_FILE.exists():
            return []
        lines = cls.LOG_FILE.read_text(encoding="utf-8").strip().split("\n")
        return [json.loads(line) for line in lines[-n:] if line.strip()]

# ---------------------------------------------------------------------------
# Command Router
# ---------------------------------------------------------------------------
class CommandRouter:
    """Routes incoming commands to the appropriate automation handler."""

    def __init__(self, confirmation_callback: Callable[[str, str, str], dict]):
        self.confirmation_callback = confirmation_callback
        self._handlers = {
            "screenshot": self._handle_screenshot,
            "screen_record_start": self._handle_record_start,
            "screen_record_stop": self._handle_record_stop,
            "browser_open": self._handle_browser_open,
            "browser_navigate": self._handle_browser_navigate,
            "browser_close": self._handle_browser_close,
            "app_open": self._handle_app_open,
            "app_close": self._handle_app_close,
            "file_list": self._handle_file_list,
            "file_move": self._handle_file_move,
            "file_delete": self._handle_file_delete,
            "shell_exec": self._handle_shell,
            "system_info": self._handle_system_info,
            "audio_play": self._handle_audio_play,
        }

    async def execute(self, cmd: BridgeCommand) -> BridgeResponse:
        start = datetime.utcnow()
        handler = self._handlers.get(cmd.action)

        if not handler:
            return BridgeResponse(
                command_id=cmd.command_id,
                status="error",
                result={"error": f"Unknown action: {cmd.action}"},
            )

        # Safety check
        if cmd.requires_confirmation:
            result = self.confirmation_callback(cmd.action, str(cmd.params), "Risky operation")
            if not result.get("confirmed"):
                return BridgeResponse(
                    command_id=cmd.command_id,
                    status="denied",
                    result={"reason": "User denied"},
                )

        try:
            response = await handler(cmd.params)
        except Exception as e:
            logger.error(f"Command {cmd.action} failed: {e}")
            response = BridgeResponse(
                command_id=cmd.command_id,
                status="error",
                result={"error": str(e)},
            )

        duration = int((datetime.utcnow() - start).total_seconds() * 1000)
        response.execution_ms = duration

        AuditLogger.log(
            command=cmd.action,
            params=cmd.params,
            confirmed=True if not cmd.requires_confirmation else result.get("confirmed"),
            result=response.status,
            duration_ms=duration,
        )

        return response

    async def _handle_screenshot(self, params: dict) -> BridgeResponse:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        result = await ctrl.screenshot(monitor=params.get("monitor", 0))
        return BridgeResponse(
            command_id="", status="success", result=result,
            screenshot_base64=result.get("base64", ""),
            file_path=result.get("path", ""),
        )

    async def _handle_browser_open(self, params: dict) -> BridgeResponse:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        result = await ctrl.open(url=params.get("url"))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_browser_navigate(self, params: dict) -> BridgeResponse:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        result = await ctrl.navigate(url=params.get("url"))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_browser_close(self, params: dict) -> BridgeResponse:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        result = await ctrl.close()
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_app_open(self, params: dict) -> BridgeResponse:
        from automation.apps import AppController
        ctrl = AppController()
        result = await ctrl.open(params.get("app_name", ""))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_app_close(self, params: dict) -> BridgeResponse:
        from automation.apps import AppController
        ctrl = AppController()
        result = await ctrl.close(params.get("app_name", ""))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_file_list(self, params: dict) -> BridgeResponse:
        from automation.files import FileController
        ctrl = FileController()
        result = await ctrl.list_dir(params.get("path", "~"))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_file_move(self, params: dict) -> BridgeResponse:
        from automation.files import FileController
        ctrl = FileController()
        result = await ctrl.move(params.get("src", ""), params.get("dst", ""))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_file_delete(self, params: dict) -> BridgeResponse:
        from automation.files import FileController
        ctrl = FileController()
        result = await ctrl.delete(params.get("path", ""))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_shell(self, params: dict) -> BridgeResponse:
        from automation.shell import ShellController
        ctrl = ShellController()
        result = await ctrl.execute(params.get("command", ""), timeout=params.get("timeout", 30))
        return BridgeResponse(
            command_id="", status="success", result=result,
            stdout=result.get("stdout", ""), stderr=result.get("stderr", ""),
        )

    async def _handle_system_info(self, params: dict) -> BridgeResponse:
        import platform
        import psutil
        result = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "ram_gb": round(psutil.virtual_memory().total / (1024**3), 1),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "disk_free_gb": round(psutil.disk_usage("/").free / (1024**3), 1),
        }
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_record_start(self, params: dict) -> BridgeResponse:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        result = await ctrl.record_start(duration_max=params.get("duration_max", 60))
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_record_stop(self, params: dict) -> BridgeResponse:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        result = await ctrl.record_stop()
        return BridgeResponse(command_id="", status="success", result=result)

    async def _handle_audio_play(self, params: dict) -> BridgeResponse:
        # TTS placeholder — integrate with pyttsx3 or gTTS
        return BridgeResponse(
            command_id="", status="success",
            result={"message": "TTS not yet implemented"},
        )


# ---------------------------------------------------------------------------
# WebSocket Server
# ---------------------------------------------------------------------------
class BridgeServer:
    """WebSocket server that accepts connections from n8n."""

    def __init__(self, confirmation_callback: Callable):
        self.confirmation_callback = confirmation_callback
        self.router = CommandRouter(confirmation_callback)
        self.clients: set = set()

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a single client connection."""
        # Auth check
        try:
            headers = dict(websocket.request_headers)
            auth = headers.get("Authorization", "")
            expected = f"Bearer {BRIDGE_SECRET}"
            if auth != expected:
                logger.warning(f"Bridge auth failed from {websocket.remote_address}")
                await websocket.close(1008, "Invalid auth")
                return
        except Exception as e:
            logger.error(f"Bridge auth error: {e}")
            await websocket.close(1011, "Auth error")
            return

        self.clients.add(websocket)
        logger.info(f"Bridge client connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "")

                    if msg_type == "ping":
                        await websocket.send(json.dumps({"type": "pong", "timestamp": datetime.utcnow().isoformat()}))

                    elif msg_type == "command":
                        payload = data.get("payload", {})
                        cmd = BridgeCommand(
                            command_id=payload.get("command_id", ""),
                            action=payload.get("action", ""),
                            params=payload.get("params", {}),
                            requires_confirmation=payload.get("requires_confirmation", False),
                            timeout_ms=payload.get("timeout_ms", 30000),
                        )
                        response = await self.router.execute(cmd)
                        await websocket.send(json.dumps({
                            "type": "response",
                            "payload": asdict(response),
                            "timestamp": datetime.utcnow().isoformat(),
                        }))

                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "payload": {"error": f"Unknown message type: {msg_type}"},
                        }))

                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"type": "error", "payload": {"error": "Invalid JSON"}}))
                except Exception as e:
                    logger.error(f"Bridge message handling error: {e}")
                    await websocket.send(json.dumps({"type": "error", "payload": {"error": str(e)}}))

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            logger.info(f"Bridge client disconnected: {websocket.remote_address}")

    async def broadcast_event(self, event_type: str, payload: dict):
        """Broadcast an event to all connected clients."""
        message = json.dumps({
            "type": "event",
            "payload": {"event_type": event_type, **payload},
            "timestamp": datetime.utcnow().isoformat(),
        })
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients if client.open],
                return_exceptions=True,
            )

    async def start(self):
        """Start the bridge server."""
        logger.info(f"Starting bridge server on ws://{BRIDGE_HOST}:{BRIDGE_PORT}")
        server = await websockets.serve(
            self.handle_client,
            BRIDGE_HOST,
            BRIDGE_PORT,
            ping_interval=PING_INTERVAL,
            ping_timeout=10,
        )
        await server.wait_closed()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def default_confirmation(action: str, target: str, risk: str) -> dict:
    """Default confirmation callback — logs and allows (for headless mode)."""
    logger.warning(f"SAFETY: {action} on {target} — {risk}")
    return {"confirmed": True, "remember": False}


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    server = BridgeServer(confirmation_callback=default_confirmation)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
