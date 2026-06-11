from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Callable


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PermissionLevel(str, Enum):
    SAFE = "safe"
    NONE = "none"
    NOTIFY = "notify"
    CONFIRM_REQUIRED = "confirm_required"
    UNSAFE = "unsafe"


@dataclass
class ToolSchema:
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: list = field(default_factory=list)
    pattern: str = ""
    min_value: Any = None
    max_value: Any = None


@dataclass
class ToolDefinition:
    name: str
    description: str
    category: str
    risk_level: RiskLevel
    permission: PermissionLevel
    timeout_seconds: int = 30
    max_retries: int = 2
    input_schema: dict[str, ToolSchema] = field(default_factory=dict)
    output_schema: dict[str, ToolSchema] = field(default_factory=dict)
    handler: Optional[Callable] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "risk_level": self.risk_level.value,
            "permission": self.permission.value,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "input_schema": {k: asdict(v) for k, v in self.input_schema.items()},
            "output_schema": {k: asdict(v) for k, v in self.output_schema.items()},
            "metadata": self.metadata,
        }

    def validate_input(self, params: dict) -> tuple[bool, list[str]]:
        errors = []
        for key, schema in self.input_schema.items():
            if schema.required and key not in params:
                errors.append(f"Missing required parameter: {key}")
                continue
            value = params.get(key)
            if value is None:
                continue
            if schema.enum and value not in schema.enum:
                errors.append(f"Invalid value for {key}: {value}. Allowed: {schema.enum}")
            if schema.pattern and isinstance(value, str):
                if not re.match(schema.pattern, value):
                    errors.append(f"Invalid format for {key}: {value}")
            if schema.min_value is not None and value < schema.min_value:
                errors.append(f"{key} must be >= {schema.min_value}")
            if schema.max_value is not None and value > schema.max_value:
                errors.append(f"{key} must be <= {schema.max_value}")
        return len(errors) == 0, errors


class ToolRegistry:
    _instance: Optional[ToolRegistry] = None

    def __new__(cls) -> ToolRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: dict[str, ToolDefinition] = {}
            cls._instance._categories: dict[str, list[str]] = {}
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._register_all_tools()
            self._initialized = True

    def _register_all_tools(self) -> None:
        self.register(ToolDefinition(
            name="browser.open",
            description="Open browser and navigate to URL",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
            input_schema={
                "url": ToolSchema(type="string", description="URL to navigate to", required=False, default="about:blank"),
                "headless": ToolSchema(type="boolean", description="Run headless", required=False, default=False),
            },
        ))
        self.register(ToolDefinition(
            name="browser.navigate",
            description="Navigate to URL",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
            input_schema={
                "url": ToolSchema(type="string", description="URL", required=True),
            },
        ))
        self.register(ToolDefinition(
            name="browser.close",
            description="Close browser",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="browser.screenshot",
            description="Capture browser screenshot",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="browser.new_tab",
            description="Open new tab",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="browser.close_tab",
            description="Close a tab",
            category="browser",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="browser.list_tabs",
            description="List open tabs",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="app.open",
            description="Open an application",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="app.close",
            description="Close an application",
            category="apps",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="app.restart",
            description="Restart an application",
            category="apps",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=30,
        ))
        self.register(ToolDefinition(
            name="app.list_running",
            description="List running applications",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="file.list",
            description="List directory contents",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="file.read",
            description="Read file contents",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="file.write",
            description="Write content to a file",
            category="files",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="file.search",
            description="Search for files",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
        ))
        self.register(ToolDefinition(
            name="file.delete",
            description="Delete a file or directory",
            category="files",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="file.move",
            description="Move/rename a file",
            category="files",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="file.copy",
            description="Copy a file or directory",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=30,
        ))
        self.register(ToolDefinition(
            name="file.compress",
            description="Compress files into archive",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=60,
        ))
        self.register(ToolDefinition(
            name="file.extract",
            description="Extract archive",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=60,
        ))
        self.register(ToolDefinition(
            name="shell.execute",
            description="Execute a shell command",
            category="shell",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=60,
            max_retries=0,
        ))
        self.register(ToolDefinition(
            name="system.info",
            description="Get system information",
            category="system",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="system.processes",
            description="List running processes",
            category="system",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="system.kill_process",
            description="Kill a process",
            category="system",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM_REQUIRED,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="screen.screenshot",
            description="Capture screenshot",
            category="screen",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="screen.ocr",
            description="Extract text via OCR",
            category="screen",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=20,
        ))
        self.register(ToolDefinition(
            name="google.youtube.search",
            description="Search YouTube",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="google.gmail.search",
            description="Search Gmail",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="google.calendar.list_events",
            description="List calendar events",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
        ))
        self.register(ToolDefinition(
            name="google.translate",
            description="Translate text",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
        ))
        self.register(ToolDefinition(
            name="memory.store",
            description="Store in semantic memory",
            category="memory",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=5,
        ))
        self.register(ToolDefinition(
            name="memory.search",
            description="Search semantic memory",
            category="memory",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=5,
        ))

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool
        self._categories.setdefault(tool.category, []).append(tool.name)

    def get(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> list[ToolDefinition]:
        if category:
            return [self._tools[name] for name in self._categories.get(category, [])]
        return list(self._tools.values())

    def list_categories(self) -> list[str]:
        return list(self._categories.keys())

    def search(self, query: str) -> list[ToolDefinition]:
        q = query.lower()
        return [t for t in self._tools.values() if q in t.name.lower() or q in t.description.lower()]

    def to_json(self) -> str:
        return json.dumps({
            "version": "4.6.0",
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "categories": self._categories,
            "tools": [t.to_dict() for t in self._tools.values()],
        }, indent=2)

    @property
    def count(self) -> int:
        return len(self._tools)


registry = ToolRegistry()
