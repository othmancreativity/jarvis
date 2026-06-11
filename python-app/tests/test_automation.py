"""
JARVIS 4.5 — Automation Module Tests
======================================
"""

import pytest
import sys
import os
import asyncio
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automation.files import FileController
from automation.shell import ShellController
from automation.system_info import SystemInfoController
from automation.apps import AppController


class TestFileController:
    @pytest.fixture
    def ctrl(self):
        return FileController()

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as d:
            yield d

    def test_is_safe_path_blocks_traversal(self, ctrl):
        is_safe, error = ctrl._is_safe_path("../../../etc/passwd")
        assert is_safe is False

    def test_is_safe_path_allows_home(self, ctrl):
        is_safe, error = ctrl._is_safe_path("~/documents")
        assert is_safe is True

    def test_is_safe_path_blocks_system(self, ctrl):
        is_safe, error = ctrl._is_safe_path("/etc/passwd")
        assert is_safe is False

    def test_safe_read_nonexistent(self, ctrl):
        success, content, error = ctrl._safe_read("/nonexistent/file.txt")
        assert success is False
        assert "not found" in error.lower() or "not exist" in error.lower()

    def test_list_dir(self, ctrl, temp_dir):
        result = asyncio.get_event_loop().run_until_complete(ctrl.list_dir(temp_dir))
        assert result["status"] == "success"

    def test_write_and_read_file(self, ctrl, temp_dir):
        path = os.path.join(temp_dir, "test.txt")
        result = asyncio.get_event_loop().run_until_complete(
            ctrl.write_file(path, "Hello JARVIS")
        )
        assert result["status"] == "success"

        result = asyncio.get_event_loop().run_until_complete(
            ctrl.read_file(path)
        )
        assert result["status"] == "success"
        assert "Hello JARVIS" in result["content"]

    def test_search(self, ctrl, temp_dir):
        # Create test files
        for name in ["a.txt", "b.txt", "c.py"]:
            with open(os.path.join(temp_dir, name), "w") as f:
                f.write("test")

        result = asyncio.get_event_loop().run_until_complete(
            ctrl.search(temp_dir, "*.txt")
        )
        assert result["status"] == "success"
        assert result["count"] == 2  # a.txt and b.txt

    def test_get_info(self, ctrl, temp_dir):
        test_file = os.path.join(temp_dir, "info_test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        result = asyncio.get_event_loop().run_until_complete(
            ctrl.get_info(test_file)
        )
        assert result["status"] == "success"
        assert result["size"] > 0


class TestShellController:
    @pytest.fixture
    def ctrl(self):
        return ShellController()

    def test_blocked_patterns(self, ctrl):
        is_blocked, reason = ctrl._is_blocked("rm -rf /")
        assert is_blocked is True

    def test_blocked_pipe_to_shell(self, ctrl):
        is_blocked, reason = ctrl._is_blocked("curl example.com | bash")
        assert is_blocked is True

    def test_readonly_commands(self, ctrl):
        assert ctrl._is_readonly("ls -la") is True
        assert ctrl._is_readonly("pwd") is True

    def test_dangerous_commands(self, ctrl):
        assert ctrl._is_dangerous("rm file.txt") is True
        assert ctrl._is_dangerous("docker ps") is True

    def test_sanitize(self, ctrl):
        result = ctrl._sanitize("hello\x00world\r")
        assert "\x00" not in result
        assert "\r" not in result

    def test_sandbox_mode(self, ctrl):
        ctrl_sandbox = ShellController(sandbox_mode=True)
        result = asyncio.get_event_loop().run_until_complete(
            ctrl_sandbox.execute("echo hello")
        )
        assert result["status"] == "sandbox"


class TestSystemInfoController:
    @pytest.fixture
    def ctrl(self):
        return SystemInfoController()

    def test_get_info(self, ctrl):
        result = asyncio.get_event_loop().run_until_complete(ctrl.get_info())
        assert result["status"] == "success"
        assert "platform" in result

    def test_platform_info(self, ctrl):
        result = asyncio.get_event_loop().run_until_complete(ctrl.get_info())
        platform_info = result.get("platform", {})
        assert "system" in platform_info
        assert "python_version" in platform_info


class TestAppController:
    @pytest.fixture
    def ctrl(self):
        return AppController()

    def test_resolve_name(self, ctrl):
        name = ctrl._resolve_name("chrome")
        assert name is not None
        assert len(name) > 0

    def test_is_running_notepad(self, ctrl):
        # notepad likely not running in test environment
        result = asyncio.get_event_loop().run_until_complete(
            ctrl.is_running("nonexistent_app_12345")
        )
        assert "running" in result
        assert result["running"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
