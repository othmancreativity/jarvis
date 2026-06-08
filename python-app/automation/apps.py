"""
JARVIS 4.5 — Application Control Module
========================================
Full application lifecycle management:
    - Open applications (cross-platform)
    - Close applications gracefully
    - Restart applications
    - Focus/bring to front
    - List running applications
    - Check if application is running
    - Get process info by app name
"""

from __future__ import annotations

import asyncio
import platform
import subprocess
import logging
import signal
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger("jarvis.automation.apps")


@dataclass
class AppProcessInfo:
    """Information about an application process."""
    name: str
    pid: int
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    status: str = "running"
    created: float = 0.0


class AppController:
    """
    Full-featured application controller.
    Cross-platform support for macOS, Linux, and Windows.
    """

    # Platform-specific app name mappings
    APP_MAP = {
        "chrome": {"darwin": "Google Chrome", "win32": "chrome", "linux": "google-chrome"},
        "firefox": {"darwin": "Firefox", "win32": "firefox", "linux": "firefox"},
        "safari": {"darwin": "Safari", "win32": None, "linux": None},
        "edge": {"darwin": "Microsoft Edge", "win32": "msedge", "linux": "microsoft-edge"},
        "code": {"darwin": "Visual Studio Code", "win32": "Code", "linux": "code"},
        "vscode": {"darwin": "Visual Studio Code", "win32": "Code", "linux": "code"},
        "terminal": {"darwin": "Terminal", "win32": "cmd", "linux": "gnome-terminal"},
        "finder": {"darwin": "Finder", "win32": "explorer", "linux": "nautilus"},
        "files": {"darwin": "Finder", "win32": "explorer", "linux": "nautilus"},
        "spotify": {"darwin": "Spotify", "win32": "Spotify", "linux": "spotify"},
        "slack": {"darwin": "Slack", "win32": "Slack", "linux": "slack"},
        "discord": {"darwin": "Discord", "win32": "Discord", "linux": "discord"},
        "zoom": {"darwin": "zoom.us", "win32": "Zoom", "linux": "zoom"},
        "teams": {"darwin": "Microsoft Teams", "win32": "Teams", "linux": "teams"},
        "obsidian": {"darwin": "Obsidian", "win32": "Obsidian", "linux": "obsidian"},
        "notes": {"darwin": "Notes", "win32": "notepad", "linux": "gedit"},
        "calculator": {"darwin": "Calculator", "win32": "calc", "linux": "gnome-calculator"},
    }

    def __init__(self):
        self._system = platform.system().lower()
        self._opened_apps: dict[str, float] = {}  # Track apps we opened

    def _resolve_name(self, app_name: str) -> str:
        """Resolve a generic app name to platform-specific name."""
        mapped = self.APP_MAP.get(app_name.lower(), {})
        if isinstance(mapped, dict):
            if self._system == "darwin":
                return mapped.get("darwin", app_name)
            elif self._system == "windows":
                return mapped.get("win32", app_name)
            else:
                return mapped.get("linux", app_name)
        return app_name

    def _get_process_by_name(self, app_name: str) -> Optional[psutil.Process]:
        """Find a process by application name."""
        if not HAS_PSUTIL:
            return None
        resolved = self._resolve_name(app_name)
        for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
            try:
                proc_name = proc.info.get("name", "")
                if resolved.lower() in proc_name.lower():
                    return proc
                cmdline = proc.info.get("cmdline") or []
                if any(resolved.lower() in arg.lower() for arg in cmdline):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    # ── Core Operations ────────────────────────────────────────────────

    async def open(self, app_name: str) -> dict:
        """Open an application by name."""
        resolved = self._resolve_name(app_name)
        try:
            if self._system == "darwin":
                subprocess.Popen(
                    ["open", "-a", resolved],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
            elif self._system == "windows":
                subprocess.Popen(
                    ["start", "", resolved],
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                )
            else:  # Linux
                subprocess.Popen(
                    [resolved],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
            self._opened_apps[app_name.lower()] = time.time()
            return {"status": "opened", "app": app_name, "resolved": resolved}
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return {"status": "error", "app": app_name, "error": str(e)}

    async def close(self, app_name: str, force: bool = False) -> dict:
        """Close an application gracefully (or force)."""
        resolved = self._resolve_name(app_name)
        try:
            if self._system == "darwin":
                if force:
                    subprocess.run(
                        ["killall", "-9", resolved],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                    )
                else:
                    subprocess.run(
                        ["osascript", "-e", f'quit app "{resolved}"'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
                    )
            elif self._system == "windows":
                subprocess.run(
                    ["taskkill", "/IM", f"{resolved}.exe", "/F" if force else "", "/T"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
                )
            else:  # Linux
                if force:
                    subprocess.run(
                        ["killall", "-9", resolved],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                    )
                else:
                    # Try graceful SIGTERM first
                    proc = self._get_process_by_name(app_name)
                    if proc:
                        proc.terminate()
                        try:
                            proc.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            proc.kill()
                    else:
                        subprocess.run(
                            ["killall", resolved],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                        )
            self._opened_apps.pop(app_name.lower(), None)
            return {"status": "closed", "app": app_name, "resolved": resolved}
        except Exception as e:
            logger.error(f"Failed to close {app_name}: {e}")
            return {"status": "error", "app": app_name, "error": str(e)}

    async def restart(self, app_name: str) -> dict:
        """Restart an application."""
        close_result = await self.close(app_name)
        if close_result["status"] in ("closed", "error"):
            await asyncio.sleep(2)  # Wait for clean shutdown
        return await self.open(app_name)

    async def focus(self, app_name: str) -> dict:
        """Bring an application window to the front."""
        resolved = self._resolve_name(app_name)
        try:
            if self._system == "darwin":
                subprocess.Popen(
                    ["osascript", "-e", f'tell application "{resolved}" to activate'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            elif self._system == "windows":
                # Use PowerShell to bring window to front
                subprocess.Popen(
                    ["powershell", "-Command",
                     f'$proc = Get-Process "{resolved}" -ErrorAction SilentlyContinue; '
                     'if ($proc) { $sig = Add-Type -MemberDefinition \'[DllImport(\\"user32.dll\\")] '
                     'public static extern bool SetForegroundWindow(IntPtr hWnd);\' -Name WinAPI -PassThru; '
                     '$sig::SetForegroundWindow($proc.MainWindowHandle) }'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            else:  # Linux - try xdotool or wmctrl
                subprocess.Popen(
                    ["xdotool", "search", "--name", resolved, "windowactivate"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            return {"status": "focused", "app": app_name, "resolved": resolved}
        except Exception as e:
            logger.error(f"Failed to focus {app_name}: {e}")
            return {"status": "error", "app": app_name, "error": str(e)}

    async def list_running(self) -> dict:
        """List all running applications."""
        try:
            if self._system == "darwin":
                result = subprocess.run(
                    ["osascript", "-e",
                     'tell application "System Events" to get name of '
                     '(processes whose background only is false)'],
                    capture_output=True, text=True, timeout=10,
                )
                apps = [a.strip() for a in result.stdout.split(",") if a.strip()]
            elif HAS_PSUTIL:
                apps = []
                seen = set()
                for proc in psutil.process_iter(["pid", "name"]):
                    try:
                        name = proc.info.get("name", "")
                        if name and name not in seen and not name.startswith("("):
                            seen.add(name)
                            apps.append(name)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                apps = sorted(apps)[:100]
            else:
                return {"status": "error", "error": "psutil not installed"}

            return {"status": "success", "apps": apps, "count": len(apps)}
        except Exception as e:
            logger.error(f"Failed to list running apps: {e}")
            return {"status": "error", "error": str(e)}

    async def is_running(self, app_name: str) -> dict:
        """Check if an application is running."""
        try:
            if HAS_PSUTIL:
                proc = self._get_process_by_name(app_name)
                if proc:
                    return {
                        "running": True,
                        "pid": proc.pid,
                        "status": proc.status() if hasattr(proc, "status") else "running",
                    }
            # Fallback to pgrep-like check
            resolved = self._resolve_name(app_name)
            result = subprocess.run(
                ["pgrep", "-f", resolved.lower()],
                capture_output=True, timeout=5,
            )
            if result.returncode == 0:
                pid = int(result.stdout.strip().split(b"\n")[0])
                return {"running": True, "pid": pid}
            return {"running": False, "pid": None}
        except Exception as e:
            return {"running": False, "pid": None, "error": str(e)}

    async def get_process_info(self, app_name: str) -> dict:
        """Get detailed process information for an app."""
        if not HAS_PSUTIL:
            return {"status": "error", "error": "psutil not installed"}

        proc = self._get_process_by_name(app_name)
        if not proc:
            return {"status": "error", "error": f"{app_name} is not running"}

        try:
            with proc.oneshot():
                info = AppProcessInfo(
                    name=proc.name(),
                    pid=proc.pid,
                    cpu_percent=proc.cpu_percent(interval=0.5),
                    memory_mb=round(proc.memory_info().rss / (1024 * 1024), 1),
                    status=proc.status(),
                    created=proc.create_time(),
                )
                return {"status": "success", "info": info.__dict__}
        except psutil.NoSuchProcess:
            return {"status": "error", "error": "Process no longer exists"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
