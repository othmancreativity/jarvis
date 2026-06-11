"""
JARVIS 4.5 — Security Tests
============================
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.permissions import PermissionEngine, PermissionRequest, PermissionLevel, Decision
from security.audit import AuditLogger, AuditEventType, SecuritySeverity
from security.validator import InputValidator


class TestPermissionEngine:
    def test_deny_by_default(self):
        engine = PermissionEngine()
        req = PermissionRequest(
            request_id="test-1",
            tool_name="shell.execute",
            action="execute",
            target="ls",
            risk_level="high",
            permission_level="deny",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.DENY

    def test_allow_none_level(self):
        engine = PermissionEngine()
        req = PermissionRequest(
            request_id="test-2",
            tool_name="system.info",
            action="get_info",
            target="",
            risk_level="none",
            permission_level="none",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.ALLOW
        assert result.confirmed is True

    def test_emergency_stop_denies_all(self):
        engine = PermissionEngine()
        engine.trigger_emergency_stop()
        req = PermissionRequest(
            request_id="test-3",
            tool_name="system.info",
            action="get_info",
            target="",
            risk_level="none",
            permission_level="none",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.DENY
        assert "EMERGENCY_STOP" in result.reason
        engine.clear_emergency_stop()

    def test_whitelist(self):
        engine = PermissionEngine()
        engine.whitelist.add("file.read", "read", duration_seconds=300)
        req = PermissionRequest(
            request_id="test-4",
            tool_name="file.read",
            action="read",
            target="test.txt",
            risk_level="none",
            permission_level="whitelist",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.ALLOW
        assert result.confirmed is True

    def test_stats_tracking(self):
        engine = PermissionEngine()
        engine.reset_stats()
        req1 = PermissionRequest(request_id="t1", tool_name="a", action="b", target="c", risk_level="none", permission_level="none")
        req2 = PermissionRequest(request_id="t2", tool_name="a", action="b", target="c", risk_level="high", permission_level="deny")
        engine.check_permission(req1)
        engine.check_permission(req2)
        stats = engine.get_stats()
        assert stats["total_requests"] == 2
        assert stats["allowed"] == 1
        assert stats["denied"] == 1


class TestAuditLogger:
    def test_log_entry(self, tmp_path):
        logger = AuditLogger(log_dir=tmp_path)
        logger.log(
            event_type=AuditEventType.COMMAND,
            action="test_action",
            target="test_target",
            decision="allow",
        )
        recent = logger.read_recent(n=1)
        assert len(recent) == 1
        assert recent[0]["action"] == "test_action"

    def test_chain_hash(self, tmp_path):
        logger = AuditLogger(log_dir=tmp_path)
        logger.log(event_type=AuditEventType.COMMAND, action="a1", target="t1", decision="allow")
        logger.log(event_type=AuditEventType.COMMAND, action="a2", target="t2", decision="allow")
        valid, count, broken = logger.verify_chain()
        assert valid is True
        assert count == 2

    def test_emergency_stop_log(self, tmp_path):
        logger = AuditLogger(log_dir=tmp_path)
        logger.log_emergency_stop("test_user")
        recent = logger.read_recent(n=1)
        assert recent[0]["event_type"] == "emergency_stop"
        assert recent[0]["severity"] == "critical"


class TestInputValidator:
    def test_sanitize_string(self):
        result = InputValidator.sanitize_string("hello\x00world")
        assert "\x00" not in result
        assert result == "helloworld"

    def test_validate_path_traversal(self):
        is_valid, path, error = InputValidator.validate_path("../../../etc/passwd")
        assert is_valid is False
        assert error is not None

    def test_validate_safe_path(self):
        is_valid, path, error = InputValidator.validate_path("~/documents/file.txt")
        assert is_valid is True
        assert error is None

    def test_validate_url(self):
        is_valid, error = InputValidator.validate_url("https://google.com")
        assert is_valid is True
        assert error is None

    def test_validate_blocked_url(self):
        is_valid, error = InputValidator.validate_url("http://localhost:8080")
        assert is_valid is False

    def test_validate_shell_command(self):
        is_valid, error = InputValidator.validate_shell_command("rm -rf /")
        assert is_valid is False

    def test_validate_safe_command(self):
        is_valid, error = InputValidator.validate_shell_command("ls -la")
        assert is_valid is True

    def test_truncate_output(self):
        long_text = "x" * 20000
        result = InputValidator.truncate_output(long_text, max_length=100)
        assert len(result) <= 150
        assert "truncated" in result

    def test_validate_json_size(self):
        is_valid, error = InputValidator.validate_json_size({f"key_{i}": "value" for i in range(200)})
        assert is_valid is False
        assert "max keys" in error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
