from __future__ import annotations

import pytest

from core.tool_registry import registry, ToolRegistry, ToolDefinition, RiskLevel, PermissionLevel, ToolSchema


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
        categories = registry.list_categories()
        assert "browser" in categories
        assert "files" in categories
        assert "shell" in categories

    def test_list_by_category(self):
        browser_tools = registry.list_tools("browser")
        assert len(browser_tools) > 0
        assert all(t.category == "browser" for t in browser_tools)

    def test_validate_input_good(self):
        tool = ToolDefinition(
            name="test.tool",
            description="Test",
            category="test",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.SAFE,
            input_schema={
                "name": ToolSchema(type="string", description="Name", required=True),
            },
        )
        valid, errors = tool.validate_input({"name": "hello"})
        assert valid
        assert errors == []

    def test_validate_required_missing(self):
        tool = ToolDefinition(
            name="test.tool",
            description="Test",
            category="test",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.SAFE,
            input_schema={
                "name": ToolSchema(type="string", description="Name", required=True),
            },
        )
        valid, errors = tool.validate_input({})
        assert not valid
        assert len(errors) == 1

    def test_search_tools(self):
        results = registry.search("browser")
        assert len(results) > 0

    def test_to_json(self):
        json_str = registry.to_json()
        assert '"version": "4.6.0"' in json_str
        assert '"categories"' in json_str
        assert '"tools"' in json_str

    def test_shell_tool_high_risk(self):
        tool = registry.get("shell.execute")
        assert tool is not None
        assert tool.risk_level == RiskLevel.HIGH
        assert tool.permission == PermissionLevel.CONFIRM_REQUIRED

    def test_system_info_low_risk(self):
        tool = registry.get("system.info")
        assert tool is not None
        assert tool.risk_level == RiskLevel.NONE

    def test_file_delete_high_risk(self):
        tool = registry.get("file.delete")
        assert tool is not None
        assert tool.risk_level == RiskLevel.HIGH

    def test_register_custom_tool(self):
        new_tool = ToolDefinition(
            name="custom.test",
            description="Custom tool",
            category="custom",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.SAFE,
        )
        registry.register(new_tool)
        retrieved = registry.get("custom.test")
        assert retrieved is not None
        assert retrieved.name == "custom.test"
