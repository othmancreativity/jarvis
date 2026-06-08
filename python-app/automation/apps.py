"""Application control module — open and close applications."""

import asyncio
import platform
import subprocess
from typing import Optional


class AppController:
    """Open and close applications on the local system."""

    # Common app name mappings
    APP_MAP = {
        "chrome": {"darwin": "Google Chrome", "win32": "chrome", "linux": "google-chrome"},
        "firefox": {"darwin": "Firefox", "win32": "firefox", "linux": "firefox"},
        "safari": {"darwin": "Safari", "win32": None, "linux": None},
        "code": {"darwin": "Visual Studio Code", "win32": "Code", "linux": "code"},
        "terminal": {"darwin": "Terminal", "win32": "cmd", "linux": "gnome-terminal"},
        "finder": {"darwin": "Finder", "win32": "explorer", "linux": "nautilus"},
        "spotify": {"darwin": "Spotify", "win32": "Spotify", "linux": "spotify"},
        "slack": {"darwin": "Slack", "win32": "Slack", "linux": "slack"},
        "discord": {"darwin": "Discord", "win32": "Discord", "linux": "discord"},
    }

    def _resolve_name(self, app_name: str) -> str:
        """Resolve a generic app name to platform-specific name."""
        system = platform.system().lower()
        mapped = self.APP_MAP.get(app_name.lower(), {})
        if isinstance(mapped, dict):
            if system == "darwin":
                return mapped.get("darwin", app_name)
            elif system == "windows":
                return mapped.get("win32", app_name)
            else:
                return mapped.get("linux", app_name)
        return app_name

    async def open(self, app_name: str) -> dict:
        """Open an application by name."""
        resolved = self._resolve_name(app_name)
        system = platform.system().lower()

        try:
            if system == "darwin":
                subprocess.Popen(["open", "-a", resolved], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif system == "windows":
                subprocess.Popen(["start", "", resolved], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([resolved], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "opened", "app": app_name, "resolved": resolved}
        except Exception as e:
            return {"status": "error", "app": app_name, "error": str(e)}

    async def close(self, app_name: str) -> dict:
        """Close an application."""
        resolved = self._resolve_name(app_name)
        system = platform.system().lower()

        try:
            if system == "darwin":
                subprocess.Popen(["osascript", "-e", f'quit app "{resolved}"'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif system == "windows":
                subprocess.Popen(["taskkill", "/IM", f"{resolved}.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(["killall", resolved], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "closed", "app": app_name, "resolved": resolved}
        except Exception as e:
            return {"status": "error", "app": app_name, "error": str(e)}

    async def list_running(self) -> dict:
        """List running applications."""
        try:
            if platform.system().lower() == "darwin":
                result = subprocess.run(["osascript", "-e", 'tell application "System Events" to get name of (processes whose background only is false)'],
                                        capture_output=True, text=True, timeout=10)
                apps = [a.strip() for a in result.stdout.split(",") if a.strip()]
            else:
                import psutil
                apps = list(set(p.name() for p in psutil.process_iter(["name"]) if p.info["name"]))
            return {"status": "success", "apps": apps[:50]}
        except Exception as e:
            return {"status": "error", "error": str(e)}
