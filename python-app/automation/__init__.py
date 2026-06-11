from __future__ import annotations

from automation.shell import ShellController, ShellError, ShellResult
from automation.browser import BrowserController
from automation.apps import AppController
from automation.files import FileController
from automation.screen import ScreenController
from automation.system_info import SystemInfoController

__all__ = [
    "ShellController", "ShellError", "ShellResult",
    "BrowserController", "AppController", "FileController",
    "ScreenController", "SystemInfoController",
]
