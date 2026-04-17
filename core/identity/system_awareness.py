"""System awareness: controlled view of the environment for LLM context.

Provides summarised, allow-listed information about the system —
never raw filesystem dumps, secrets, or unrestricted host introspection.
"""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Any

from loguru import logger


class SystemAwareness:
    """Controlled system context for prompt injection.

    All methods return summarised strings safe for inclusion in LLM
    system prompts.  No secrets, no raw paths outside allow-listed roots.
    """

    def __init__(
        self,
        *,
        project_root: Path | None = None,
        gpu_summary: str = "NVIDIA RTX 3050 6 GB VRAM",
    ) -> None:
        if project_root is None:
            from settings.paths import PROJECT_ROOT
            project_root = PROJECT_ROOT
        self._root = project_root
        self._gpu = gpu_summary

    # -- Environment ---------------------------------------------------------

    def environment_summary(self) -> str:
        """OS class, Python version, GPU tier — no secrets."""
        return (
            f"OS: {platform.system()} {platform.release()}, "
            f"Python: {platform.python_version()}, "
            f"GPU: {self._gpu}"
        )

    # -- Project view --------------------------------------------------------

    def project_summary(self, max_depth: int = 2) -> str:
        """Allow-listed directory tree (shallow, no hidden files)."""
        lines: list[str] = [f"Project: {self._root.name}/"]
        self._walk(self._root, lines, depth=0, max_depth=max_depth)
        return "\n".join(lines[:40])  # cap output

    def _walk(self, path: Path, lines: list[str], depth: int, max_depth: int) -> None:
        if depth >= max_depth:
            return
        skip = {".git", ".venv", "venv", "__pycache__", "node_modules", ".cache", "data", "logs"}
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        except PermissionError:
            return
        for entry in entries:
            if entry.name.startswith(".") or entry.name in skip:
                continue
            prefix = "  " * (depth + 1)
            if entry.is_dir():
                lines.append(f"{prefix}{entry.name}/")
                self._walk(entry, lines, depth + 1, max_depth)
            else:
                lines.append(f"{prefix}{entry.name}")

    # -- Tool availability ---------------------------------------------------

    def tools_summary(self, tool_names: list[str] | None = None) -> str:
        """One-line-per-tool summary for system prompt."""
        if not tool_names:
            return "Tools: not yet loaded (Phase 5)"
        lines = [f"  - {name}" for name in tool_names[:15]]
        return "Available tools:\n" + "\n".join(lines)

    # -- Combined for prompt builder -----------------------------------------

    def full_context(self, tool_names: list[str] | None = None) -> str:
        """Full system awareness block for the System Prompt Builder."""
        parts = [
            self.environment_summary(),
            self.tools_summary(tool_names),
        ]
        return "\n".join(parts)
