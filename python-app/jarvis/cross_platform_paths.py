from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Optional

try:
    from platformdirs import user_config_dir, user_data_dir, user_cache_dir, user_log_dir
    HAS_PLATFORMDIRS = True
except ImportError:
    HAS_PLATFORMDIRS = False


class CrossPlatformPaths:
    """Abstract application paths using platformdirs.

    Provides cross-platform paths for config, data, cache, and logs.
    Also maps common application names to their executable paths.
    """

    APP_NAME = "jarvis"
    APP_AUTHOR = "JARVIS"

    def __init__(self) -> None:
        self._system = platform.system().lower()

    @property
    def config_dir(self) -> Path:
        if HAS_PLATFORMDIRS:
            return Path(user_config_dir(self.APP_NAME, self.APP_AUTHOR))
        return Path.home() / ".jarvis"

    @property
    def data_dir(self) -> Path:
        if HAS_PLATFORMDIRS:
            return Path(user_data_dir(self.APP_NAME, self.APP_AUTHOR))
        return Path.home() / ".jarvis" / "data"

    @property
    def cache_dir(self) -> Path:
        if HAS_PLATFORMDIRS:
            return Path(user_cache_dir(self.APP_NAME, self.APP_AUTHOR))
        return Path.home() / ".jarvis" / "cache"

    @property
    def log_dir(self) -> Path:
        if HAS_PLATFORMDIRS:
            return Path(user_log_dir(self.APP_NAME, self.APP_AUTHOR))
        return Path.home() / ".jarvis" / "logs"

    @property
    def checkpoint_dir(self) -> Path:
        return self.data_dir / "checkpoints"

    @property
    def vector_store_dir(self) -> Path:
        return self.data_dir / "vector_store"

    @property
    def audit_dir(self) -> Path:
        return self.data_dir / "audit"

    @property
    def config_file(self) -> Path:
        return self.config_dir / "config.yaml"

    @property
    def memory_db(self) -> Path:
        return self.data_dir / "memory.db"

    def ensure_dirs(self) -> None:
        for d in [self.config_dir, self.data_dir, self.cache_dir, self.log_dir,
                  self.checkpoint_dir, self.vector_store_dir, self.audit_dir]:
            d.mkdir(parents=True, exist_ok=True)

    APP_MAP: dict[str, dict[str, Optional[str]]] = {
        "chrome": {"win32": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    "darwin": "/Applications/Google Chrome.app",
                    "linux": "google-chrome"},
        "firefox": {"win32": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                     "darwin": "/Applications/Firefox.app",
                     "linux": "firefox"},
        "vscode": {"win32": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                    "darwin": "/Applications/Visual Studio Code.app",
                    "linux": "code"},
        "terminal": {"win32": "cmd.exe",
                      "darwin": "/Applications/Utilities/Terminal.app",
                      "linux": "gnome-terminal"},
        "explorer": {"win32": "explorer.exe",
                      "darwin": "Finder",
                      "linux": "nautilus"},
        "notepad": {"win32": "notepad.exe",
                     "darwin": "TextEdit",
                     "linux": "gedit"},
        "calculator": {"win32": "calc.exe",
                        "darwin": "Calculator",
                        "linux": "gnome-calculator"},
        "spotify": {"win32": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
                     "darwin": "/Applications/Spotify.app",
                     "linux": "spotify"},
        "slack": {"win32": r"C:\Users\%USERNAME%\AppData\Local\slack\slack.exe",
                   "darwin": "/Applications/Slack.app",
                   "linux": "slack"},
    }

    def resolve_app(self, name: str) -> Optional[str]:
        entry = self.APP_MAP.get(name.lower())
        if not entry:
            return name
        path = entry.get(self._system if self._system == "darwin" else
                         ("win32" if self._system == "windows" else "linux"))
        if not path:
            return name
        if "%USERNAME%" in path:
            path = path.replace("%USERNAME%", os.environ.get("USERNAME", "user"))
            if not Path(path).exists():
                return name
        return path


paths = CrossPlatformPaths()
