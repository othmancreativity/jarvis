from __future__ import annotations

import asyncio
import glob
import logging
import os
import shutil
from pathlib import Path
from typing import Optional

from security.validator import InputValidator

logger = logging.getLogger("jarvis.automation.files")


class FileController:
    MAX_READ_SIZE = 10 * 1024 * 1024
    MAX_SEARCH_RESULTS = 500

    def _expand_path(self, path: str) -> str:
        return os.path.abspath(os.path.expanduser(path or "~"))

    async def list_dir(self, path: str = "~", limit: int = 100) -> dict:
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": "Path does not exist"}
            if not os.path.isdir(abs_path):
                return {"status": "error", "error": "Not a directory"}
            entries = []
            for entry in sorted(os.listdir(abs_path))[:limit]:
                full = os.path.join(abs_path, entry)
                try:
                    stat = os.stat(full)
                    entries.append({
                        "name": entry, "is_dir": os.path.isdir(full),
                        "size": stat.st_size, "modified": stat.st_mtime,
                    })
                except OSError:
                    continue
            return {"status": "success", "path": abs_path, "files": entries, "count": len(entries)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def read_file(self, path: str, max_bytes: int = 100000) -> dict:
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": "File not found"}
            if os.path.isdir(abs_path):
                return {"status": "error", "error": "Is a directory"}
            size = os.path.getsize(abs_path)
            if size > max_bytes:
                return {"status": "error", "error": f"File too large ({size} bytes)"}
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_bytes)
            return {"status": "success", "path": abs_path, "content": content, "size": size}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def write_file(self, path: str, content: str, append: bool = False) -> dict:
        try:
            abs_path = self._expand_path(path)
            Path(abs_path).parent.mkdir(parents=True, exist_ok=True)
            mode = "a" if append else "w"
            with open(abs_path, mode, encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "path": abs_path, "bytes_written": len(content)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def delete(self, path: str, recursive: bool = False) -> dict:
        try:
            abs_path = self._expand_path(path)
            if not os.path.exists(abs_path):
                return {"status": "error", "error": "Path does not exist"}
            if os.path.isdir(abs_path):
                if recursive:
                    shutil.rmtree(abs_path)
                else:
                    return {"status": "error", "error": "Is a directory. Use recursive=True"}
            else:
                os.remove(abs_path)
            return {"status": "success", "path": abs_path}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def search(self, path: str = "~", pattern: str = "*") -> dict:
        try:
            abs_path = self._expand_path(path)
            matches = sorted(glob.glob(os.path.join(abs_path, "**", pattern), recursive=True))
            matches = matches[:self.MAX_SEARCH_RESULTS]
            results = []
            for m in matches:
                try:
                    stat = os.stat(m)
                    results.append({"path": m, "is_dir": os.path.isdir(m), "size": stat.st_size})
                except OSError:
                    continue
            return {"status": "success", "matches": results, "count": len(results)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def move(self, src: str, dst: str) -> dict:
        try:
            shutil.move(self._expand_path(src), self._expand_path(dst))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def copy(self, src: str, dst: str) -> dict:
        try:
            src_path = self._expand_path(src)
            dst_path = self._expand_path(dst)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
