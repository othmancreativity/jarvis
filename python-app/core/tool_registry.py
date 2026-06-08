"""
JARVIS 4.5 — Complete Tool Registry
====================================
Source of truth for all available operations across all services.
Every tool has: name, description, risk level, input/output schemas,
permission requirements, validation rules, timeout, retry settings.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional, Callable
from datetime import datetime


class RiskLevel(str, Enum):
    """Risk classification for operations."""
    NONE = "none"           # No risk (e.g., read-only info)
    LOW = "low"             # Minor system changes
    MEDIUM = "medium"       # Moderate impact operations
    HIGH = "high"           # Significant system changes
    CRITICAL = "critical"   # Destructive or security-sensitive


class PermissionLevel(str, Enum):
    """Permission requirements for operations."""
    NONE = "none"           # No permission needed
    NOTIFY = "notify"       # Logged but auto-allowed
    CONFIRM = "confirm"     # Requires user confirmation
    WHITELIST = "whitelist" # Requires pre-authorization
    DENY = "deny"           # Always denied


@dataclass
class ToolSchema:
    """Schema definition for tool input/output."""
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: list = field(default_factory=list)
    pattern: str = ""       # Regex pattern for string validation
    min_value: Any = None
    max_value: Any = None


@dataclass
class ToolDefinition:
    """Complete definition of a tool/operation."""
    name: str
    description: str
    category: str                           # browser, files, shell, google, etc.
    risk_level: RiskLevel
    permission: PermissionLevel
    timeout_seconds: int = 30
    max_retries: int = 2
    input_schema: dict[str, ToolSchema] = field(default_factory=dict)
    output_schema: dict[str, ToolSchema] = field(default_factory=dict)
    handler: Optional[Callable] = None      # Set at runtime
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to dictionary (excludes handler)."""
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
        """Validate input parameters against schema. Returns (is_valid, errors)."""
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
    """
    Central registry for all JARVIS tools and operations.
    Thread-safe singleton that provides tool discovery, validation, and routing.
    """

    _instance: Optional[ToolRegistry] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: dict[str, ToolDefinition] = {}
            cls._instance._categories: dict[str, list[str]] = {}
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._register_all_tools()
            self._initialized = True

    def _register_all_tools(self):
        """Register all built-in tools."""
        # ── Browser Tools ──────────────────────────────────────────────────
        self.register(ToolDefinition(
            name="browser.open",
            description="Open Chrome browser and optionally navigate to URL",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
            input_schema={
                "url": ToolSchema(type="string", description="URL to navigate to", required=False, default="about:blank", pattern=r"^https?://.*$"),
                "headless": ToolSchema(type="boolean", description="Run in headless mode", required=False, default=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "url": ToolSchema(type="string", description="Current URL"),
                "title": ToolSchema(type="string", description="Page title"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.navigate",
            description="Navigate to URL in existing browser",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
            input_schema={
                "url": ToolSchema(type="string", description="URL to navigate to", required=True, pattern=r"^https?://.*$"),
                "wait_until": ToolSchema(type="string", description="When to consider navigation complete", required=False, default="domcontentloaded", enum=["load", "domcontentloaded", "networkidle"]),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "url": ToolSchema(type="string", description="Current URL"),
                "title": ToolSchema(type="string", description="Page title"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.close",
            description="Close the browser",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={},
            output_schema={"status": ToolSchema(type="string", description="Operation status")},
        ))

        self.register(ToolDefinition(
            name="browser.screenshot",
            description="Capture browser screenshot as base64 PNG",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
            input_schema={
                "full_page": ToolSchema(type="boolean", description="Capture full page", required=False, default=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "base64": ToolSchema(type="string", description="Base64-encoded PNG"),
                "format": ToolSchema(type="string", description="Image format"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.scroll",
            description="Scroll the page",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "direction": ToolSchema(type="string", description="Scroll direction", required=True, enum=["up", "down", "left", "right"]),
                "amount": ToolSchema(type="integer", description="Pixels to scroll", required=False, default=500, min_value=1, max_value=10000),
            },
            output_schema={"status": ToolSchema(type="string", description="Operation status")},
        ))

        self.register(ToolDefinition(
            name="browser.get_page_info",
            description="Get page title, URL, and meta description",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={},
            output_schema={
                "title": ToolSchema(type="string", description="Page title"),
                "url": ToolSchema(type="string", description="Page URL"),
                "description": ToolSchema(type="string", description="Meta description"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.new_tab",
            description="Open a new browser tab",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "url": ToolSchema(type="string", description="URL for new tab", required=False, default="about:blank"),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "tab_count": ToolSchema(type="integer", description="Total number of tabs"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.close_tab",
            description="Close the current or specified tab",
            category="browser",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=10,
            input_schema={
                "index": ToolSchema(type="integer", description="Tab index to close", required=False, default=-1),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "tab_count": ToolSchema(type="integer", description="Remaining tabs"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.list_tabs",
            description="List all open tabs",
            category="browser",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={},
            output_schema={
                "tabs": ToolSchema(type="array", description="List of tabs with title and URL"),
                "count": ToolSchema(type="integer", description="Number of tabs"),
            },
        ))

        self.register(ToolDefinition(
            name="browser.download",
            description="Download a file from the browser",
            category="browser",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=60,
            input_schema={
                "url": ToolSchema(type="string", description="URL of file to download", required=True),
                "filename": ToolSchema(type="string", description="Target filename", required=False, default=""),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="Download path"),
                "size": ToolSchema(type="integer", description="File size in bytes"),
            },
        ))

        # ── Application Tools ──────────────────────────────────────────────
        self.register(ToolDefinition(
            name="app.open",
            description="Open an application by name",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "app_name": ToolSchema(type="string", description="Application name", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "app": ToolSchema(type="string", description="Resolved app name"),
            },
        ))

        self.register(ToolDefinition(
            name="app.close",
            description="Close an application",
            category="apps",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=10,
            input_schema={
                "app_name": ToolSchema(type="string", description="Application name", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "app": ToolSchema(type="string", description="Application name"),
            },
        ))

        self.register(ToolDefinition(
            name="app.restart",
            description="Restart an application",
            category="apps",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=30,
            input_schema={
                "app_name": ToolSchema(type="string", description="Application name", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "app": ToolSchema(type="string", description="Application name"),
            },
        ))

        self.register(ToolDefinition(
            name="app.focus",
            description="Focus/bring an application window to front",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "app_name": ToolSchema(type="string", description="Application name", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "app": ToolSchema(type="string", description="Application name"),
            },
        ))

        self.register(ToolDefinition(
            name="app.list_running",
            description="List all running applications",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={},
            output_schema={
                "apps": ToolSchema(type="array", description="List of running applications"),
                "count": ToolSchema(type="integer", description="Number of applications"),
            },
        ))

        self.register(ToolDefinition(
            name="app.is_running",
            description="Check if an application is running",
            category="apps",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "app_name": ToolSchema(type="string", description="Application name", required=True),
            },
            output_schema={
                "running": ToolSchema(type="boolean", description="Whether the app is running"),
                "pid": ToolSchema(type="integer", description="Process ID if running", required=False),
            },
        ))

        # ── File Tools ─────────────────────────────────────────────────────
        self.register(ToolDefinition(
            name="file.list",
            description="List directory contents",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "path": ToolSchema(type="string", description="Directory path", required=False, default="~"),
                "limit": ToolSchema(type="integer", description="Max entries to return", required=False, default=100, min_value=1, max_value=1000),
            },
            output_schema={
                "path": ToolSchema(type="string", description="Resolved path"),
                "files": ToolSchema(type="array", description="List of file entries"),
                "count": ToolSchema(type="integer", description="Number of entries"),
            },
        ))

        self.register(ToolDefinition(
            name="file.read",
            description="Read file contents",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "path": ToolSchema(type="string", description="File path", required=True),
                "max_bytes": ToolSchema(type="integer", description="Max bytes to read", required=False, default=100000, min_value=1, max_value=10485760),
            },
            output_schema={
                "path": ToolSchema(type="string", description="File path"),
                "content": ToolSchema(type="string", description="File content"),
                "truncated": ToolSchema(type="boolean", description="Whether content was truncated"),
                "size": ToolSchema(type="integer", description="File size"),
            },
        ))

        self.register(ToolDefinition(
            name="file.write",
            description="Write content to a file",
            category="files",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=15,
            input_schema={
                "path": ToolSchema(type="string", description="File path", required=True),
                "content": ToolSchema(type="string", description="Content to write", required=True),
                "append": ToolSchema(type="boolean", description="Append instead of overwrite", required=False, default=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="File path"),
                "bytes_written": ToolSchema(type="integer", description="Bytes written"),
            },
        ))

        self.register(ToolDefinition(
            name="file.move",
            description="Move/rename a file or directory",
            category="files",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=15,
            input_schema={
                "src": ToolSchema(type="string", description="Source path", required=True),
                "dst": ToolSchema(type="string", description="Destination path", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "src": ToolSchema(type="string", description="Source path"),
                "dst": ToolSchema(type="string", description="Destination path"),
            },
        ))

        self.register(ToolDefinition(
            name="file.copy",
            description="Copy a file or directory",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=30,
            input_schema={
                "src": ToolSchema(type="string", description="Source path", required=True),
                "dst": ToolSchema(type="string", description="Destination path", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "src": ToolSchema(type="string", description="Source path"),
                "dst": ToolSchema(type="string", description="Destination path"),
            },
        ))

        self.register(ToolDefinition(
            name="file.delete",
            description="Delete a file or directory",
            category="files",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=15,
            input_schema={
                "path": ToolSchema(type="string", description="Path to delete", required=True),
                "recursive": ToolSchema(type="boolean", description="Delete directories recursively", required=False, default=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="Deleted path"),
            },
        ))

        self.register(ToolDefinition(
            name="file.search",
            description="Search for files matching a pattern",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=30,
            input_schema={
                "path": ToolSchema(type="string", description="Directory to search in", required=False, default="~"),
                "pattern": ToolSchema(type="string", description="Search pattern (glob)", required=True),
                "recursive": ToolSchema(type="boolean", description="Search recursively", required=False, default=True),
            },
            output_schema={
                "matches": ToolSchema(type="array", description="Matching file paths"),
                "count": ToolSchema(type="integer", description="Number of matches"),
            },
        ))

        self.register(ToolDefinition(
            name="file.compress",
            description="Compress files into an archive",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=60,
            input_schema={
                "paths": ToolSchema(type="array", description="List of paths to compress", required=True),
                "output": ToolSchema(type="string", description="Output archive path", required=True),
                "format": ToolSchema(type="string", description="Archive format", required=False, default="zip", enum=["zip", "tar", "tar.gz"]),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="Archive path"),
                "size": ToolSchema(type="integer", description="Archive size"),
            },
        ))

        self.register(ToolDefinition(
            name="file.extract",
            description="Extract an archive",
            category="files",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=60,
            input_schema={
                "path": ToolSchema(type="string", description="Archive path", required=True),
                "output_dir": ToolSchema(type="string", description="Extraction directory", required=False, default="."),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "output_dir": ToolSchema(type="string", description="Extraction directory"),
                "files": ToolSchema(type="array", description="Extracted files"),
            },
        ))

        self.register(ToolDefinition(
            name="file.get_info",
            description="Get file metadata (size, modified time, permissions)",
            category="files",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "path": ToolSchema(type="string", description="File path", required=True),
            },
            output_schema={
                "path": ToolSchema(type="string", description="File path"),
                "size": ToolSchema(type="integer", description="File size"),
                "modified": ToolSchema(type="string", description="Last modified time"),
                "is_dir": ToolSchema(type="boolean", description="Whether it's a directory"),
                "permissions": ToolSchema(type="string", description="File permissions"),
            },
        ))

        # ── Screen Tools ───────────────────────────────────────────────────
        self.register(ToolDefinition(
            name="screen.screenshot",
            description="Capture a screenshot",
            category="screen",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
            input_schema={
                "monitor": ToolSchema(type="integer", description="Monitor index", required=False, default=0, min_value=0),
                "region": ToolSchema(type="object", description="Region to capture {x, y, w, h}", required=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "base64": ToolSchema(type="string", description="Base64-encoded PNG"),
                "path": ToolSchema(type="string", description="Saved file path"),
                "width": ToolSchema(type="integer", description="Image width"),
                "height": ToolSchema(type="integer", description="Image height"),
            },
        ))

        self.register(ToolDefinition(
            name="screen.record_start",
            description="Start screen recording",
            category="screen",
            risk_level=RiskLevel.MEDIUM,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=10,
            input_schema={
                "duration_max": ToolSchema(type="integer", description="Max recording duration in seconds", required=False, default=60, min_value=1, max_value=300),
                "monitor": ToolSchema(type="integer", description="Monitor index", required=False, default=0),
                "fps": ToolSchema(type="integer", description="Frames per second", required=False, default=10, min_value=1, max_value=60),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="Recording file path"),
                "max_duration": ToolSchema(type="integer", description="Max duration"),
            },
        ))

        self.register(ToolDefinition(
            name="screen.record_stop",
            description="Stop screen recording",
            category="screen",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={},
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "path": ToolSchema(type="string", description="Recording file path"),
                "duration_seconds": ToolSchema(type="number", description="Actual duration"),
            },
        ))

        self.register(ToolDefinition(
            name="screen.ocr",
            description="Perform OCR on screen or region to extract text",
            category="screen",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=20,
            input_schema={
                "monitor": ToolSchema(type="integer", description="Monitor index", required=False, default=0),
                "region": ToolSchema(type="object", description="Region {x, y, w, h}", required=False),
                "language": ToolSchema(type="string", description="OCR language", required=False, default="eng"),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "text": ToolSchema(type="string", description="Extracted text"),
                "confidence": ToolSchema(type="number", description="OCR confidence"),
            },
        ))

        # ── Shell Tools ────────────────────────────────────────────────────
        self.register(ToolDefinition(
            name="shell.execute",
            description="Execute a shell command with safety checks",
            category="shell",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=60,
            max_retries=0,
            input_schema={
                "command": ToolSchema(type="string", description="Shell command", required=True),
                "timeout": ToolSchema(type="integer", description="Timeout in seconds", required=False, default=30, min_value=1, max_value=300),
                "cwd": ToolSchema(type="string", description="Working directory", required=False, default=""),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "returncode": ToolSchema(type="integer", description="Exit code"),
                "stdout": ToolSchema(type="string", description="Standard output"),
                "stderr": ToolSchema(type="string", description="Standard error"),
            },
        ))

        # ── System Tools ───────────────────────────────────────────────────
        self.register(ToolDefinition(
            name="system.info",
            description="Get comprehensive system information",
            category="system",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={},
            output_schema={
                "platform": ToolSchema(type="string", description="OS platform"),
                "processor": ToolSchema(type="string", description="CPU info"),
                "ram_total_gb": ToolSchema(type="number", description="Total RAM in GB"),
                "ram_used_gb": ToolSchema(type="number", description="Used RAM in GB"),
                "cpu_percent": ToolSchema(type="number", description="CPU usage %"),
                "disk_free_gb": ToolSchema(type="number", description="Free disk space in GB"),
            },
        ))

        self.register(ToolDefinition(
            name="system.processes",
            description="List running processes",
            category="system",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "limit": ToolSchema(type="integer", description="Max processes to return", required=False, default=20),
                "sort_by": ToolSchema(type="string", description="Sort field", required=False, default="cpu", enum=["cpu", "memory", "name", "pid"]),
            },
            output_schema={
                "processes": ToolSchema(type="array", description="Process list"),
                "count": ToolSchema(type="integer", description="Number of processes"),
            },
        ))

        self.register(ToolDefinition(
            name="system.kill_process",
            description="Kill a process by PID or name",
            category="system",
            risk_level=RiskLevel.HIGH,
            permission=PermissionLevel.CONFIRM,
            timeout_seconds=10,
            input_schema={
                "pid": ToolSchema(type="integer", description="Process ID", required=False),
                "name": ToolSchema(type="string", description="Process name", required=False),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "killed": ToolSchema(type="array", description="List of killed processes"),
            },
        ))

        # ── Google Service Tools (API wrappers) ───────────────────────────
        self.register(ToolDefinition(
            name="google.youtube.search",
            description="Search YouTube videos",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "query": ToolSchema(type="string", description="Search query", required=True),
                "max_results": ToolSchema(type="integer", description="Max results", required=False, default=5, min_value=1, max_value=50),
            },
            output_schema={
                "videos": ToolSchema(type="array", description="Video results"),
                "count": ToolSchema(type="integer", description="Number of results"),
            },
        ))

        self.register(ToolDefinition(
            name="google.drive.list",
            description="List files in Google Drive",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "page_size": ToolSchema(type="integer", description="Max files", required=False, default=10, min_value=1, max_value=100),
                "query": ToolSchema(type="string", description="Search query", required=False, default=""),
            },
            output_schema={
                "files": ToolSchema(type="array", description="File list"),
                "count": ToolSchema(type="integer", description="Number of files"),
            },
        ))

        self.register(ToolDefinition(
            name="google.gmail.search",
            description="Search emails in Gmail",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "q": ToolSchema(type="string", description="Gmail search query", required=False, default=""),
                "max_results": ToolSchema(type="integer", description="Max results", required=False, default=10),
            },
            output_schema={
                "messages": ToolSchema(type="array", description="Email list"),
                "count": ToolSchema(type="integer", description="Number of emails"),
            },
        ))

        self.register(ToolDefinition(
            name="google.calendar.list_events",
            description="List calendar events",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "calendar_id": ToolSchema(type="string", description="Calendar ID", required=False, default="primary"),
                "max_results": ToolSchema(type="integer", description="Max events", required=False, default=10),
            },
            output_schema={
                "events": ToolSchema(type="array", description="Event list"),
                "count": ToolSchema(type="integer", description="Number of events"),
            },
        ))

        self.register(ToolDefinition(
            name="google.translate",
            description="Translate text",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=10,
            input_schema={
                "text": ToolSchema(type="string", description="Text to translate", required=True),
                "target_language": ToolSchema(type="string", description="Target language code", required=True),
                "source_language": ToolSchema(type="string", description="Source language code", required=False, default=""),
            },
            output_schema={
                "translated_text": ToolSchema(type="string", description="Translated text"),
                "detected_source": ToolSchema(type="string", description="Detected source language"),
            },
        ))

        self.register(ToolDefinition(
            name="google.contacts.list",
            description="List Google Contacts",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "page_size": ToolSchema(type="integer", description="Max contacts", required=False, default=10),
            },
            output_schema={
                "contacts": ToolSchema(type="array", description="Contact list"),
                "count": ToolSchema(type="integer", description="Number of contacts"),
            },
        ))

        self.register(ToolDefinition(
            name="google.docs.create",
            description="Create a Google Doc",
            category="google",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
            input_schema={
                "title": ToolSchema(type="string", description="Document title", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "document_id": ToolSchema(type="string", description="Document ID"),
                "url": ToolSchema(type="string", description="Document URL"),
            },
        ))

        self.register(ToolDefinition(
            name="google.sheets.read",
            description="Read values from a Google Sheet",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "spreadsheet_id": ToolSchema(type="string", description="Spreadsheet ID", required=True),
                "range": ToolSchema(type="string", description="Cell range (e.g., Sheet1!A1:C10)", required=True),
            },
            output_schema={
                "values": ToolSchema(type="array", description="Cell values"),
                "range": ToolSchema(type="string", description="Actual range read"),
            },
        ))

        self.register(ToolDefinition(
            name="google.sheets.write",
            description="Write values to a Google Sheet",
            category="google",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
            input_schema={
                "spreadsheet_id": ToolSchema(type="string", description="Spreadsheet ID", required=True),
                "range": ToolSchema(type="string", description="Cell range", required=True),
                "values": ToolSchema(type="array", description="2D array of values", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "updated_cells": ToolSchema(type="integer", description="Number of cells updated"),
            },
        ))

        self.register(ToolDefinition(
            name="google.tasks.list",
            description="List Google Tasks",
            category="google",
            risk_level=RiskLevel.NONE,
            permission=PermissionLevel.NONE,
            timeout_seconds=15,
            input_schema={
                "tasklist_id": ToolSchema(type="string", description="Task list ID", required=False, default="@default"),
                "show_completed": ToolSchema(type="boolean", description="Include completed tasks", required=False, default=True),
            },
            output_schema={
                "tasks": ToolSchema(type="array", description="Task list"),
                "count": ToolSchema(type="integer", description="Number of tasks"),
            },
        ))

        self.register(ToolDefinition(
            name="google.slides.create",
            description="Create a Google Slides presentation",
            category="google",
            risk_level=RiskLevel.LOW,
            permission=PermissionLevel.NOTIFY,
            timeout_seconds=15,
            input_schema={
                "title": ToolSchema(type="string", description="Presentation title", required=True),
            },
            output_schema={
                "status": ToolSchema(type="string", description="Operation status"),
                "presentation_id": ToolSchema(type="string", description="Presentation ID"),
                "url": ToolSchema(type="string", description="Presentation URL"),
            },
        ))

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool definition."""
        self._tools[tool.name] = tool
        self._categories.setdefault(tool.category, []).append(tool.name)

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> list[ToolDefinition]:
        """List all tools, optionally filtered by category."""
        if category:
            return [self._tools[name] for name in self._categories.get(category, [])]
        return list(self._tools.values())

    def list_categories(self) -> list[str]:
        """List all tool categories."""
        return list(self._categories.keys())

    def get_by_risk(self, risk_level: RiskLevel) -> list[ToolDefinition]:
        """Get all tools with a specific risk level."""
        return [t for t in self._tools.values() if t.risk_level == risk_level]

    def search(self, query: str) -> list[ToolDefinition]:
        """Search tools by name or description."""
        query = query.lower()
        return [t for t in self._tools.values() if query in t.name.lower() or query in t.description.lower()]

    def to_json(self) -> str:
        """Export full registry to JSON."""
        return json.dumps({
            "version": "4.5.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "categories": self._categories,
            "tools": [t.to_dict() for t in self._tools.values()],
        }, indent=2)

    @property
    def count(self) -> int:
        """Total number of registered tools."""
        return len(self._tools)


# Singleton instance
registry = ToolRegistry()
