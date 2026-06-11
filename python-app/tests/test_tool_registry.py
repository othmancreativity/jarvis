"""
JARVIS 4.5 — Tool Registry Tests
=================================
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tool_registry import ToolRegistry, registry, RiskLevel, PermissionLevel


class TestToolRegistry:
    def test_singleton(self):
        r1 = ToolRegistry()
        r2 = ToolRegistry()
        assert r1 is r2

    def test_tool_count(self):
        assert registry.count > 0

    def test_get_tool(self):
        tool = registry.get("browser.open")
        assert tool is not None
        assert tool.category == "browser"

    def test_list_categories(self):
        cats = registry.list_categories()
        assert "browser" in cats
        assert "files" in cats
        assert "system" in cats
        assert "shell" in cats

    def test_list_by_category(self):
        browser_tools = registry.list_tools(category="browser")
        assert len(browser_tools) > 0
        for t in browser_tools:
            assert t.category == "browser"

    def test_validate_input_good(self):
        tool = registry.get("browser.open")
        valid, errors = tool.validate_input({"url": "https://example.com"})
        assert valid is True
        assert len(errors) == 0

    def test_validate_input_bad_url(self):
        tool = registry.get("browser.open")
        valid, errors = tool.validate_input({"url": "not-a-url"})
        assert valid is False
        assert len(errors) > 0

    def test_validate_required_missing(self):
        tool = registry.get("browser.navigate")
        valid, errors = tool.validate_input({})
        assert valid is False
        assert any("Missing required" in e for e in errors)

    def test_search_tools(self):
        results = registry.search("screenshot")
        assert len(results) > 0
        for r in results:
            assert "screenshot" in r.name.lower() or "screenshot" in r.description.lower()

    def test_risk_levels(self):
        critical_tools = registry.get_by_risk(RiskLevel.CRITICAL)
        for t in critical_tools:
            assert t.risk_level == RiskLevel.CRITICAL

    def test_json_export(self):
        json_str = registry.to_json()
        assert '"version": "4.5.0"' in json_str
        assert "browser.open" in json_str

    def test_shell_tool_high_risk(self):
        tool = registry.get("shell.execute")
        assert tool is not None
        assert tool.risk_level == RiskLevel.HIGH
        assert tool.permission == PermissionLevel.CONFIRM

    def test_system_info_low_risk(self):
        tool = registry.get("system.info")
        assert tool is not None
        assert tool.risk_level == RiskLevel.NONE
        assert tool.permission == PermissionLevel.NONE

    def test_file_delete_high_risk(self):
        tool = registry.get("file.delete")
        assert tool is not None
        assert tool.risk_level == RiskLevel.HIGH


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
