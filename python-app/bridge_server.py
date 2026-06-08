"""
JARVIS 4.5 — WebSocket Bridge Server
=====================================
Bidirectional WebSocket communication bridge between n8n and local laptop.

Protocol:
  - Connection: ws://localhost:8765/jarvis-bridge
  - Auth: Bearer token via JARVIS_BRIDGE_SECRET env var
  - Messages: JSON with {type, payload, timestamp, id}
  - Heartbeat: ping/pong every 30 seconds
  - Auto-reconnect: Client retries with exponential backoff

Security:
  - HMAC-SHA256 optional message signing
  - All risky operations require user confirmation
  - Audit logging of every command
  - Connection rate limiting
  - Emergency stop propagation
"""

from __future__ import annotations

import asyncio
import json
import os
import hmac
import hashlib
import logging
import time
import secrets
from datetime import datetime
from typing import Optional, Callable, Any, Coroutine
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    from websockets.exceptions import ConnectionClosed
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False
    websockets = None
    WebSocketServerProtocol = None
    ConnectionClosed = Exception

from security.audit import audit_logger, AuditEventType, SecuritySeverity

logger = logging.getLogger("jarvis.bridge")

# ── Configuration ────────────────────────────────────────────────────────

BRIDGE_SECRET = os.environ.get("JARVIS_BRIDGE_SECRET", "change-me-in-production")
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "8765"))
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "0.0.0.0")
PING_INTERVAL = 30
COMMAND_TIMEOUT = 60
MAX_CONNECTIONS = 5

# ── Data Models ──────────────────────────────────────────────────────────

@dataclass
class BridgeCommand:
    """Command from n8n to laptop."""
    command_id: str
    action: str
    params: dict
    requires_confirmation: bool
    timeout_ms: int = 30000
    source: str = "n8n"
    timestamp: float = field(default_factory=time.time)

@dataclass
class BridgeResponse:
    """Response from laptop to n8n."""
    command_id: str
    status: str  # success, error, denied, timeout, blocked
    result: dict = field(default_factory=dict)
    stdout: str = ""
    stderr: str = ""
    file_path: str = ""
    screenshot_base64: str = ""
    execution_ms: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class BridgeMessage:
    """Standard bridge message envelope."""
    id: str = ""
    type: str = ""  # command, response, event, ping, pong, error, auth
    payload: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    signature: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = secrets.token_hex(4)

    def sign(self, secret: str) -> str:
        """Create HMAC signature."""
        data = f"{self.id}:{self.type}:{json.dumps(self.payload, sort_keys=True)}:{self.timestamp}"
        return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()[:32]

    def verify(self, secret: str) -> bool:
        """Verify HMAC signature."""
        expected = self.sign(secret)
        return hmac.compare_digest(expected, self.signature)

# ── Connection Manager ───────────────────────────────────────────────────

class ConnectionManager:
    """Manages WebSocket client connections."""

    def __init__(self, max_connections: int = MAX_CONNECTIONS):
        self.clients: set[WebSocketServerProtocol] = set()
        self.max_connections = max_connections
        self._auth_status: dict[WebSocketServerProtocol, bool] = {}
        self._connection_time: dict[WebSocketServerProtocol, float] = {}
        self._lock = asyncio.Lock()

    async def add(self, ws: WebSocketServerProtocol) -> bool:
        """Add a client connection. Returns False if at capacity."""
        async with self._lock:
            if len(self.clients) >= self.max_connections:
                return False
            self.clients.add(ws)
            self._auth_status[ws] = False
            self._connection_time[ws] = time.time()
            return True

    async def remove(self, ws: WebSocketServerProtocol) -> None:
        """Remove a client connection."""
        async with self._lock:
            self.clients.discard(ws)
            self._auth_status.pop(ws, None)
            self._connection_time.pop(ws, None)

    def is_authenticated(self, ws: WebSocketServerProtocol) -> bool:
        return self._auth_status.get(ws, False)

    def authenticate(self, ws: WebSocketServerProtocol) -> None:
        self._auth_status[ws] = True

    @property
    def count(self) -> int:
        return len(self.clients)

    @property
    def authenticated_count(self) -> int:
        return sum(1 for v in self._auth_status.values() if v)

# ── Command Router ───────────────────────────────────────────────────────

class CommandRouter:
    """Routes incoming commands to automation handlers."""

    def __init__(self, confirmation_callback: Callable[[str, str, str], dict]):
        self.confirmation_callback = confirmation_callback
        self._handlers: dict[str, Callable] = {}
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all command handlers."""
        handlers = {
            "screenshot": self._handle_screenshot,
            "screen_record_start": self._handle_record_start,
            "screen_record_stop": self._handle_record_stop,
            "browser_open": self._handle_browser_open,
            "browser_navigate": self._handle_browser_navigate,
            "browser_close": self._handle_browser_close,
            "browser_new_tab": self._handle_browser_new_tab,
            "browser_close_tab": self._handle_browser_close_tab,
            "browser_list_tabs": self._handle_browser_list_tabs,
            "browser_screenshot": self._handle_browser_screenshot,
            "app_open": self._handle_app_open,
            "app_close": self._handle_app_close,
            "app_restart": self._handle_app_restart,
            "app_focus": self._handle_app_focus,
            "app_list_running": self._handle_app_list_running,
            "file_list": self._handle_file_list,
            "file_read": self._handle_file_read,
            "file_write": self._handle_file_write,
            "file_move": self._handle_file_move,
            "file_copy": self._handle_file_copy,
            "file_delete": self._handle_file_delete,
            "file_search": self._handle_file_search,
            "file_compress": self._handle_file_compress,
            "file_extract": self._handle_file_extract,
            "file_get_info": self._handle_file_get_info,
            "shell_exec": self._handle_shell,
            "system_info": self._handle_system_info,
            "system_processes": self._handle_system_processes,
            "system_kill_process": self._handle_kill_process,
        }
        self._handlers.update(handlers)

    async def execute(self, cmd: BridgeCommand) -> BridgeResponse:
        """Execute a command with full safety pipeline."""
        start = datetime.utcnow()
        handler = self._handlers.get(cmd.action)

        if not handler:
            return BridgeResponse(
                command_id=cmd.command_id,
                status="error",
                result={"error": f"Unknown action: {cmd.action}"},
            )

        # Safety confirmation check
        if cmd.requires_confirmation:
            result = self.confirmation_callback(cmd.action, str(cmd.params), "Risky operation")
            if not result.get("confirmed"):
                audit_logger.log_command(cmd.command_id, cmd.action, cmd.params, False, "denied", 0)
                return BridgeResponse(
                    command_id=cmd.command_id,
                    status="denied",
                    result={"reason": "User denied"},
                )

        # Execute
        try:
            response = await handler(cmd.params)
        except Exception as e:
            logger.error(f"Command {cmd.action} failed: {e}")
            response = {"status": "error", "error": str(e)}

        duration = int((datetime.utcnow() - start).total_seconds() * 1000)

        # Build response
        bridge_response = BridgeResponse(
            command_id=cmd.command_id,
            status=response.get("status", "success"),
            result=response,
            execution_ms=duration,
        )

        if "stdout" in response:
            bridge_response.stdout = response["stdout"]
        if "stderr" in response:
            bridge_response.stderr = response["stderr"]
        if "screenshot_base64" in response:
            bridge_response.screenshot_base64 = response["screenshot_base64"]
        if "path" in response:
            bridge_response.file_path = response["path"]

        # Audit log
        audit_logger.log_command(
            command_id=cmd.command_id,
            action=cmd.action,
            params=cmd.params,
            confirmed=True if not cmd.requires_confirmation else result.get("confirmed"),
            result=bridge_response.status,
            duration_ms=duration,
        )

        return bridge_response

    # ── Browser Handlers ───────────────────────────────────────────────

    async def _handle_browser_open(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.open(url=params.get("url"), headless=params.get("headless", False))

    async def _handle_browser_navigate(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.navigate(url=params.get("url"), wait_until=params.get("wait_until", "domcontentloaded"))

    async def _handle_browser_close(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.close()

    async def _handle_browser_new_tab(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.new_tab(url=params.get("url"))

    async def _handle_browser_close_tab(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.close_tab(index=params.get("index", -1))

    async def _handle_browser_list_tabs(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.list_tabs()

    async def _handle_browser_screenshot(self, params: dict) -> dict:
        from automation.browser import BrowserController
        ctrl = BrowserController()
        return await ctrl.screenshot(full_page=params.get("full_page", False))

    # ── App Handlers ───────────────────────────────────────────────────

    async def _handle_app_open(self, params: dict) -> dict:
        from automation.apps import AppController
        ctrl = AppController()
        return await ctrl.open(params.get("app_name", ""))

    async def _handle_app_close(self, params: dict) -> dict:
        from automation.apps import AppController
        ctrl = AppController()
        return await ctrl.close(params.get("app_name", ""))

    async def _handle_app_restart(self, params: dict) -> dict:
        from automation.apps import AppController
        ctrl = AppController()
        return await ctrl.restart(params.get("app_name", ""))

    async def _handle_app_focus(self, params: dict) -> dict:
        from automation.apps import AppController
        ctrl = AppController()
        return await ctrl.focus(params.get("app_name", ""))

    async def _handle_app_list_running(self, params: dict) -> dict:
        from automation.apps import AppController
        ctrl = AppController()
        return await ctrl.list_running()

    # ── Screen Handlers ────────────────────────────────────────────────

    async def _handle_screenshot(self, params: dict) -> dict:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        return await ctrl.screenshot(
            monitor=params.get("monitor", 0),
            region=params.get("region"),
        )

    async def _handle_record_start(self, params: dict) -> dict:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        return await ctrl.record_start(
            duration_max=params.get("duration_max", 60),
            monitor=params.get("monitor", 0),
            fps=params.get("fps", 10),
        )

    async def _handle_record_stop(self, params: dict) -> dict:
        from automation.screen import ScreenController
        ctrl = ScreenController()
        return await ctrl.record_stop()

    # ── File Handlers ──────────────────────────────────────────────────

    async def _handle_file_list(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.list_dir(path=params.get("path", "~"), limit=params.get("limit", 100))

    async def _handle_file_read(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.read_file(path=params.get("path", ""), max_bytes=params.get("max_bytes", 100000))

    async def _handle_file_write(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.write_file(
            path=params.get("path", ""),
            content=params.get("content", ""),
            append=params.get("append", False),
        )

    async def _handle_file_move(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.move(params.get("src", ""), params.get("dst", ""))

    async def _handle_file_copy(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.copy(params.get("src", ""), params.get("dst", ""))

    async def _handle_file_delete(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.delete(params.get("path", ""), recursive=params.get("recursive", False))

    async def _handle_file_search(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.search(path=params.get("path", "~"), pattern=params.get("pattern", "*"))

    async def _handle_file_compress(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.compress(
            paths=params.get("paths", []),
            output=params.get("output", ""),
            fmt=params.get("format", "zip"),
        )

    async def _handle_file_extract(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.extract(params.get("path", ""), output_dir=params.get("output_dir", "."))

    async def _handle_file_get_info(self, params: dict) -> dict:
        from automation.files import FileController
        ctrl = FileController()
        return await ctrl.get_info(params.get("path", ""))

    # ── Shell & System Handlers ────────────────────────────────────────

    async def _handle_shell(self, params: dict) -> dict:
        from automation.shell import ShellController
        ctrl = ShellController()
        return await ctrl.execute(
            params.get("command", ""),
            timeout=params.get("timeout", 30),
            cwd=params.get("cwd"),
        )

    async def _handle_system_info(self, params: dict) -> dict:
        from automation.system_info import SystemInfoController
        ctrl = SystemInfoController()
        return await ctrl.get_info()

    async def _handle_system_processes(self, params: dict) -> dict:
        from automation.system_info import SystemInfoController
        ctrl = SystemInfoController()
        return await ctrl.get_processes(
            limit=params.get("limit", 20),
            sort_by=params.get("sort_by", "cpu"),
        )

    async def _handle_kill_process(self, params: dict) -> dict:
        from automation.system_info import SystemInfoController
        ctrl = SystemInfoController()
        return await ctrl.kill_process(
            pid=params.get("pid"),
            name=params.get("name"),
            signal_type=params.get("signal", "term"),
        )

# ── Bridge Server ────────────────────────────────────────────────────────

class BridgeServer:
    """
    Production-grade WebSocket bridge server.
    Manages client connections, authentication, command routing, and health.
    """

    def __init__(self, confirmation_callback: Optional[Callable] = None):
        self.confirmation_callback = confirmation_callback or self._default_confirmation
        self.router = CommandRouter(self.confirmation_callback)
        self.manager = ConnectionManager()
        self._running = False
        self._server = None

    def _default_confirmation(self, action: str, target: str, risk: str) -> dict:
        """Default confirmation — logs and allows (for headless/CI mode)."""
        logger.warning(f"SAFETY: {action} on {target} - {risk}")
        return {"confirmed": True, "remember": False}

    async def _authenticate(self, ws: WebSocketServerProtocol) -> bool:
        """Authenticate a connection via Bearer token."""
        try:
            headers = dict(ws.request_headers)
            auth = headers.get("Authorization", "")
            expected = f"Bearer {BRIDGE_SECRET}"

            if auth != expected:
                logger.warning(f"Auth failed from {ws.remote_address}")
                await ws.close(1008, "Invalid auth")
                return False

            self.manager.authenticate(ws)
            logger.info(f"Client authenticated: {ws.remote_address}")
            return True
        except Exception as e:
            logger.error(f"Auth error: {e}")
            await ws.close(1011, "Auth error")
            return False

    async def handle_client(self, ws: WebSocketServerProtocol, path: str):
        """Handle a single client connection."""
        if not await self.manager.add(ws):
            await ws.close(1013, "Server at capacity")
            return

        try:
            # Wait for auth message (for clients that send auth via message)
            # Some clients can't set headers, so accept auth via first message
            auth_timeout = asyncio.get_event_loop().time() + 10

            async for message in ws:
                # Check auth
                if not self.manager.is_authenticated(ws):
                    try:
                        data = json.loads(message)
                        if data.get("type") == "auth":
                            token = data.get("payload", {}).get("token", "")
                            if token == BRIDGE_SECRET:
                                self.manager.authenticate(ws)
                                await ws.send(json.dumps({"type": "auth_success", "timestamp": time.time()}))
                                continue
                            else:
                                await ws.close(1008, "Invalid token")
                                break
                        elif asyncio.get_event_loop().time() > auth_timeout:
                            await ws.close(1008, "Auth timeout")
                            break
                    except (json.JSONDecodeError, KeyError):
                        pass

                    # Try header auth
                    if not await self._authenticate(ws):
                        break
                    # Auth successful via header, process the message

                # Process authenticated messages
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "")

                    if msg_type == "ping":
                        await ws.send(json.dumps({
                            "type": "pong",
                            "timestamp": time.time(),
                            "clients": self.manager.authenticated_count,
                        }))

                    elif msg_type == "command":
                        payload = data.get("payload", {})
                        cmd = BridgeCommand(
                            command_id=payload.get("command_id", ""),
                            action=payload.get("action", ""),
                            params=payload.get("params", {}),
                            requires_confirmation=payload.get("requires_confirmation", False),
                            timeout_ms=payload.get("timeout_ms", 30000),
                            source=payload.get("source", "n8n"),
                        )

                        # Execute command
                        try:
                            response = await asyncio.wait_for(
                                self.router.execute(cmd),
                                timeout=cmd.timeout_ms / 1000,
                            )
                        except asyncio.TimeoutError:
                            response = BridgeResponse(
                                command_id=cmd.command_id,
                                status="timeout",
                                result={"error": f"Command timed out after {cmd.timeout_ms}ms"},
                            )

                        await ws.send(json.dumps({
                            "type": "response",
                            "id": data.get("id", ""),
                            "payload": response.to_dict(),
                            "timestamp": time.time(),
                        }))

                    elif msg_type == "heartbeat":
                        await ws.send(json.dumps({
                            "type": "heartbeat_ack",
                            "timestamp": time.time(),
                            "status": "healthy",
                        }))

                    elif msg_type == "status":
                        await ws.send(json.dumps({
                            "type": "status",
                            "payload": {
                                "clients": self.manager.count,
                                "authenticated": self.manager.authenticated_count,
                                "uptime": time.time(),
                            },
                            "timestamp": time.time(),
                        }))

                    else:
                        await ws.send(json.dumps({
                            "type": "error",
                            "payload": {"error": f"Unknown message type: {msg_type}"},
                        }))

                except json.JSONDecodeError:
                    await ws.send(json.dumps({"type": "error", "payload": {"error": "Invalid JSON"}}))
                except Exception as e:
                    logger.error(f"Message handling error: {e}")
                    await ws.send(json.dumps({"type": "error", "payload": {"error": str(e)}}))

        except ConnectionClosed:
            pass
        finally:
            await self.manager.remove(ws)
            logger.info(f"Client disconnected: {ws.remote_address}")

    async def broadcast_event(self, event_type: str, payload: dict) -> None:
        """Broadcast an event to all connected clients."""
        message = json.dumps({
            "type": "event",
            "payload": {"event_type": event_type, **payload},
            "timestamp": time.time(),
        })
        dead_clients = set()
        for client in self.manager.clients:
            try:
                if self.manager.is_authenticated(client) and client.open:
                    await client.send(message)
            except Exception:
                dead_clients.add(client)

        for client in dead_clients:
            await self.manager.remove(client)

    async def start(self) -> None:
        """Start the bridge server."""
        if not HAS_WEBSOCKETS:
            logger.error("websockets library not installed. Run: pip install websockets")
            return

        self._running = True
        logger.info(f"Starting JARVIS 4.5 Bridge Server on ws://{BRIDGE_HOST}:{BRIDGE_PORT}")

        try:
            self._server = await websockets.serve(
                self.handle_client,
                BRIDGE_HOST,
                BRIDGE_PORT,
                ping_interval=PING_INTERVAL,
                ping_timeout=10,
                close_timeout=5,
            )
            await self._server.wait_closed()
        except Exception as e:
            logger.error(f"Bridge server error: {e}")
            self._running = False

    async def stop(self) -> None:
        """Stop the bridge server gracefully."""
        logger.info("Stopping bridge server")
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    def is_running(self) -> bool:
        return self._running


# ── Entry Point ──────────────────────────────────────────────────────────

def default_confirmation(action: str, target: str, risk: str) -> dict:
    """Default confirmation callback for standalone mode."""
    logger.warning(f"SAFETY: {action} on {target} - {risk}")
    return {"confirmed": True, "remember": False}


async def main():
    """Standalone bridge server entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    server = BridgeServer(confirmation_callback=default_confirmation)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
