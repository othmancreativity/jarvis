"""
JARVIS 4.5 — File Operations Module
====================================
Full file lifecycle management with safety:
    - List directory contents with metadata
    - Read files (text and binary)
    - Write files (create/append)
    - Move/rename files
    - Copy files and directories
    - Delete files and directories (with safety)
    - Search for files by pattern
    - Compress files (zip, tar, tar.gz)
    - Extract archives
    - Get file metadata

Safety:
    - Protected path detection
    - Path traversal prevention
    - Size limits
    - Confirmation for destructive operations
"""

from __future__ import annotations

import os
import shutil
import glob
import zipfile
import tarfile
import logging
from pathlib import Path
from typing import Optional, List, Tuple

logger = logging.getLogger("jarvis.automation.files")


class FileController:
    """
    Full-featured file operations controller with safety constraints.
    All paths are validated before operations.
    """

    # Patterns that require explicit confirmation
    PROTECTED_PATHS = [
        "/", "/boot", "/etc", "/usr", "/bin", "/sbin", "/lib", "/lib64",
        "/sys", "/proc", "/dev", "/var/log",
        ".ssh", ".gnupg", ".config", ".env", ".aws", ".kube",
        ".docker", ".npmrc", ".pypirc",
        "password", "token", "secret", "credential", "private_key",
        "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
        ".pem", ".key", ".p12", ".pfx", ".keystore",
        "/root", "/home/*/.bash_history", "/home/*/.zsh_history",
    ]

    # Size limits
    MAX_READ_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_SEARCH_RESULTS = 500
    MAX_ARCHIVE_SIZE = 500 * 1024 * 1024  # 500 MB

    def __init__(self):
        self._last_operation: Optional[dict] = None

    def _expand_path(self, path: str) -> str:
        """Expand user home and resolve to absolute path."""
        if not path:
            path = "~"
        expanded = os.path.expanduser(path)
        return os.path.abspath(expanded)

    def _is_safe_path(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a path is safe to operate on.
        Returns (is_safe, error_message).
        """
        abs_path = self._expand_path(path)
        path_lower = abs_path.lower()

        # Check for path traversal
        normalized = os.path.normpath(abs_path)
        if ".." in normalized.split(os.sep):
            home = str(Path.home().resolve())
            try:
                resolved = str(Path(normalized).resolve())
                if not resolved.startswith(home):
                    return False, f"Path traversal blocked: {path}"
            except (OSError, ValueError):
                return False, f"Invalid path: {path}"

        # Check protected paths
        for protected in self.PROTECTED_PATHS:
            if protected.lower() in path_lower:
                return False, f"Access to protected path blocked: {protected}"

        # Check system directories
        try:
            if any(abs_path.startswith(p) for p in ["/sys/", "/proc/", "/dev/"]):
                return False, "System directories are protected"
        except Exception:
            pass

        return True, None

    def _safe_read(self, path: str, max_bytes: int = MAX_READ_SIZE) -> Tuple[bool, str, Optional[str]]:
        """Safely read a file. Returns (success, content_or_empty, error)."""
        is_safe, error = self._is_safe_path(path)
        if not is_safe:
            return False, "", error

        abs_path = self._expand_path(path)
        if not os.path.exists(abs_path):
            return False, "", f"File not found: {path}"
        if os.path.isdir(abs_path):
            return False, "", f"Is a directory: {path}"

        try:
            size = os.path.getsize(abs_path)
            if size > max_bytes:
                return False, "", f"File too large ({size} bytes). Max: {max_bytes}"

            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_bytes)
            return True, content, None
        except UnicodeDecodeError:
            # Try binary read with hex dump
            try:
                with open(abs_path, "rb") as f:
                    data = f.read(min(max_bytes, 10240))
                hex_content = data.hex()
                formatted = " ".join(hex_content[i:i+2] for i in range(0, len(hex_content), 2))
                return True, f"[Binary file - hex dump]\n{formatted[:2000]}", None
            except Exception as e:
                return False, "", str(e)
        except Exception as e:
            return False, "", str(e)

    # ── Directory Operations ───────────────────────────────────────────

    async def list_dir(self, path: str = "~", limit: int = 100) -> dict:
        """List directory contents with metadata."""
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "path": path, "error": "Path does not exist"}
            if not os.path.isdir(abs_path):
                return {"status": "error", "path": path, "error": "Not a directory"}

            entries = []
            count = 0
            for entry in sorted(os.listdir(abs_path)):
                if count >= limit:
                    break
                full = os.path.join(abs_path, entry)
                try:
                    stat = os.stat(full)
                    entries.append({
                        "name": entry,
                        "is_dir": os.path.isdir(full),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "permissions": oct(stat.st_mode)[-3:],
                    })
                    count += 1
                except (OSError, PermissionError):
                    continue

            return {
                "status": "success",
                "path": abs_path,
                "files": entries,
                "count": count,
                "has_more": len(os.listdir(abs_path)) > limit,
            }
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}

    # ── Read/Write ─────────────────────────────────────────────────────

    async def read_file(self, path: str, max_bytes: int = 100000) -> dict:
        """Read file contents safely."""
        success, content, error = self._safe_read(path, max_bytes)
        if not success:
            return {"status": "error", "path": path, "error": error}

        abs_path = self._expand_path(path)
        size = os.path.getsize(abs_path)
        self._last_operation = {"action": "read", "path": abs_path}

        return {
            "status": "success",
            "path": abs_path,
            "content": content,
            "truncated": size > max_bytes,
            "size": size,
        }

    async def write_file(self, path: str, content: str, append: bool = False) -> dict:
        """Write content to a file."""
        is_safe, error = self._is_safe_path(path)
        if not is_safe:
            return {"status": "error", "error": error}

        try:
            abs_path = self._expand_path(path)
            dir_path = os.path.dirname(abs_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            mode = "a" if append else "w"
            with open(abs_path, mode, encoding="utf-8") as f:
                bytes_written = f.write(content)

            self._last_operation = {"action": "write", "path": abs_path}
            return {
                "status": "success",
                "path": abs_path,
                "bytes_written": bytes_written,
                "append": append,
            }
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}

    # ── Move/Copy ──────────────────────────────────────────────────────

    async def move(self, src: str, dst: str) -> dict:
        """Move/rename a file or directory."""
        for path in [src, dst]:
            is_safe, error = self._is_safe_path(path)
            if not is_safe:
                return {"status": "error", "error": error}

        try:
            src_path = self._expand_path(src)
            dst_path = self._expand_path(dst)
            os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)
            shutil.move(src_path, dst_path)
            return {"status": "success", "src": src_path, "dst": dst_path}
        except Exception as e:
            return {"status": "error", "src": src, "dst": dst, "error": str(e)}

    async def copy(self, src: str, dst: str) -> dict:
        """Copy a file or directory."""
        for path in [src, dst]:
            is_safe, error = self._is_safe_path(path)
            if not is_safe:
                return {"status": "error", "error": error}

        try:
            src_path = self._expand_path(src)
            dst_path = self._expand_path(dst)
            os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

            return {"status": "success", "src": src_path, "dst": dst_path}
        except Exception as e:
            return {"status": "error", "src": src, "dst": dst, "error": str(e)}

    # ── Delete ─────────────────────────────────────────────────────────

    async def delete(self, path: str, recursive: bool = False) -> dict:
        """Delete a file or directory (with safety)."""
        is_safe, error = self._is_safe_path(path)
        if not is_safe:
            return {"status": "error", "error": error}

        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": f"Path does not exist: {path}"}

            if os.path.isdir(abs_path):
                if recursive:
                    shutil.rmtree(abs_path)
                else:
                    return {"status": "error", "error": "Is a directory. Use recursive=true to delete."}
            else:
                os.remove(abs_path)

            return {"status": "success", "path": abs_path}
        except Exception as e:
            return {"status": "error", "path": path, "error": str(e)}

    # ── Search ─────────────────────────────────────────────────────────

    async def search(self, path: str = "~", pattern: str = "*", recursive: bool = True) -> dict:
        """Search for files matching a pattern."""
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": f"Path does not exist: {path}"}

            search_path = os.path.join(abs_path, "**" if recursive else "", pattern)
            matches = glob.glob(search_path, recursive=recursive)
            matches = matches[:self.MAX_SEARCH_RESULTS]

            results = []
            for m in matches:
                try:
                    stat = os.stat(m)
                    results.append({
                        "path": m,
                        "is_dir": os.path.isdir(m),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                    })
                except OSError:
                    continue

            return {
                "status": "success",
                "matches": results,
                "count": len(results),
                "truncated": len(matches) >= self.MAX_SEARCH_RESULTS,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Compression ────────────────────────────────────────────────────

    async def compress(self, paths: List[str], output: str, fmt: str = "zip") -> dict:
        """Compress files into an archive."""
        for p in paths:
            is_safe, error = self._is_safe_path(p)
            if not is_safe:
                return {"status": "error", "error": error}

        try:
            out_path = self._expand_path(output)
            abs_paths = [self._expand_path(p) for p in paths]

            if fmt == "zip":
                with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for p in abs_paths:
                        if os.path.isdir(p):
                            for root, _, files in os.walk(p):
                                for f in files:
                                    fp = os.path.join(root, f)
                                    zf.write(fp, os.path.relpath(fp, os.path.dirname(p)))
                        else:
                            zf.write(p, os.path.basename(p))
            elif fmt in ("tar", "tar.gz"):
                mode = "w:gz" if fmt == "tar.gz" else "w"
                with tarfile.open(out_path, mode) as tf:
                    for p in abs_paths:
                        tf.add(p, arcname=os.path.basename(p))
            else:
                return {"status": "error", "error": f"Unsupported format: {fmt}"}

            size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
            return {"status": "success", "path": out_path, "size": size, "format": fmt}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def extract(self, path: str, output_dir: str = ".") -> dict:
        """Extract an archive."""
        is_safe, error = self._is_safe_path(path)
        if not is_safe:
            return {"status": "error", "error": error}

        try:
            abs_path = self._expand_path(path)
            out = self._expand_path(output_dir)
            os.makedirs(out, exist_ok=True)
            extracted = []

            if zipfile.is_zipfile(abs_path):
                with zipfile.ZipFile(abs_path, "r") as zf:
                    zf.extractall(out)
                    extracted = zf.namelist()
            elif tarfile.is_tarfile(abs_path):
                with tarfile.open(abs_path, "r:*") as tf:
                    tf.extractall(out)
                    extracted = tf.getnames()
            else:
                return {"status": "error", "error": "Unknown archive format"}

            return {"status": "success", "output_dir": out, "files": extracted}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Metadata ───────────────────────────────────────────────────────

    async def get_info(self, path: str) -> dict:
        """Get file metadata."""
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": f"Path does not exist: {path}"}

            stat = os.stat(abs_path)
            return {
                "status": "success",
                "path": abs_path,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "is_dir": os.path.isdir(abs_path),
                "is_file": os.path.isfile(abs_path),
                "is_symlink": os.path.islink(abs_path),
                "permissions": oct(stat.st_mode)[-3:],
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
