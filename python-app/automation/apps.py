from __future__ import annotations

import asyncio
import logging
import platform
import subprocess
from typing import Optional

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.automation.apps")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class AppController:
    def __init__(self) -> None:
        self._system = platform.system().lower()
        self._opened_apps: dict[str, float] = {}

    def _resolve_name(self, app_name: str) -> str:
        resolved = paths.resolve_app(app_name)
        return resolved or app_name

    async def open(self, app_name: str) -> dict:
        resolved = self._resolve_name(app_name)
        try:
            if self._system == "windows":
                subprocess.Popen(["start", "", resolved], shell=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self._system == "darwin":
                subprocess.Popen(["open", "-a", resolved],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([resolved],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._opened_apps[app_name.lower()] = __import__('time').time()
            return {"status": "opened", "app": app_name, "resolved": resolved}
        except Exception as e:
            logger.error("Failed to open %s: %s", app_name, e)
            return {"status": "error", "app": app_name, "error": str(e)}

    async def close(self, app_name: str, force: bool = False) -> dict:
        resolved = self._resolve_name(app_name)
        try:
            if self._system == "windows":
                subprocess.run(["taskkill", "/IM", f"{resolved}.exe", "/F" if force else ""],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            elif self._system == "darwin":
                subprocess.run(["killall"] + (["-9"] if force else []) + [resolved],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            else:
                subprocess.run(["killall"] + (["-9"] if force else []) + [resolved],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            self._opened_apps.pop(app_name.lower(), None)
            return {"status": "closed", "app": app_name}
        except Exception as e:
            return {"status": "error", "app": app_name, "error": str(e)}

    async def list_running(self) -> dict:
        if HAS_PSUTIL:
            apps = sorted(set(
                p.info["name"] for p in psutil.process_iter(["name"])
                if p.info["name"]
            ))[:100]
            return {"status": "success", "apps": apps, "count": len(apps)}
        return {"status": "error", "error": "psutil not installed"}

    async def is_running(self, app_name: str) -> dict:
        if HAS_PSUTIL:
            for proc in psutil.process_iter(["name"]):
                try:
                    if proc.info["name"] and app_name.lower() in proc.info["name"].lower():
                        return {"running": True, "pid": proc.pid}
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        return {"running": False}
