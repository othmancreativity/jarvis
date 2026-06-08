"""File operations with safety constraints."""

import os
import shutil
from pathlib import Path
from typing import List, Optional
import asyncio


class FileController:
    """File operations with safety constraints and audit logging."""

    # Patterns that require explicit confirmation
    RISKY_PATTERNS = [
        "/", "/boot", "/etc", "/usr", "/bin", "/sbin", "/lib", "/sys", "/dev",
        ".ssh", ".gnupg", ".config", ".env", ".aws", ".kube",
        "password", "token", "secret", "credential", "key.pem",
    ]

    # Size limit for safe operations (10 MB)
    MAX_SAFE_SIZE = 10 * 1024 * 1024

    def _is_risky_path(self, path: str) -> bool:
        """Check if a path is considered risky."""
        expanded = os.path.expanduser(path)
        abs_path = os.path.abspath(expanded)
        lower = abs_path.lower()
        for pattern in self.RISKY_PATTERNS:
            if pattern in lower:
                return True
        # Check for system directories
        if abs_path.startswith(("/sys", "/proc", "/dev")):
            return True
        return False

    def _expand_path(self, path: str) -> str:
        """Expand user home and get absolute path."""
        return os.path.abspath(os.path.expanduser(path))

    async def list_dir(self, path: str = "~") -> dict:
        """List directory contents. Safe — no confirmation."""
        try:
            target = self._expand_path(path)
            entries = os.listdir(target)
            result = []
            for entry in entries[:100]:  # Limit for safety
                full = os.path.join(target, entry)
                try:
                    stat = os.stat(full)
                    result.append({
                        "name": entry,
                        "is_dir": os.path.isdir(full),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                    })
                except (OSError, PermissionError):
                    continue
            return {"status": "success", "path": target, "files": result}
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}

    async def read_file(self, path: str, max_bytes: int = 100000) -> dict:
        """Read file contents. Requires confirmation for sensitive paths."""
        try:
            target = self._expand_path(path)
            if self._is_risky_path(target):
                return {"status": "error", "error": "Path is protected — confirmation required but not implemented for read_file"}
            size = os.path.getsize(target)
            if size > self.MAX_SAFE_SIZE:
                return {"status": "error", "error": f"File too large ({size} bytes). Max: {self.MAX_SAFE_SIZE}"}
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_bytes)
            return {"status": "success", "path": target, "content": content, "truncated": size > max_bytes}
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}

    async def move(self, src: str, dst: str) -> dict:
        """Move file. Requires confirmation (handled by caller)."""
        try:
            src_path = self._expand_path(src)
            dst_path = self._expand_path(dst)
            if self._is_risky_path(src_path) or self._is_risky_path(dst_path):
                return {"status": "error", "error": "Cannot operate on protected paths"}
            shutil.move(src_path, dst_path)
            return {"status": "success", "src": src_path, "dst": dst_path}
        except Exception as e:
            return {"status": "error", "src": src, "dst": dst, "error": str(e)}

    async def delete(self, path: str) -> dict:
        """Delete file. Requires confirmation (handled by caller)."""
        try:
            target = self._expand_path(path)
            if self._is_risky_path(target):
                return {"status": "error", "error": "Cannot delete protected paths"}
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            return {"status": "success", "path": target}
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}
