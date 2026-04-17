"""Jarvis system identity: Pydantic model + YAML loader.

Defines *who Jarvis is* in a structured, versionable format that
feeds every system prompt.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from loguru import logger
from pydantic import BaseModel, Field


class JarvisIdentity(BaseModel):
    """Structured representation of the Jarvis system identity."""

    name: str = "Jarvis"
    role: str = "Personal AI assistant system"
    architecture: str = ""
    version: str = "0.3.0-alpha"
    description: str = ""
    capabilities: list[str] = Field(default_factory=list)
    tone: str = "Professional yet approachable"
    default_style: str = "balanced"
    safety_rules: list[str] = Field(default_factory=list)
    principles: list[str] = Field(default_factory=list)
    component_notice: str = ""
    tool_notice: str = ""
    memory_notice: str = ""

    def identity_block(self) -> str:
        """Compact identity paragraph for system prompts."""
        caps = ", ".join(self.capabilities[:5]) if self.capabilities else "general assistance"
        return (
            f"You are {self.name}, a {self.role}. "
            f"Architecture: {self.architecture}. "
            f"Key capabilities: {caps}. "
            f"Tone: {self.tone}. Style: {self.default_style}."
        )

    def safety_block(self) -> str:
        """Safety rules as a bullet list for system prompts."""
        if not self.safety_rules:
            return ""
        lines = [f"- {r}" for r in self.safety_rules]
        return "Safety rules:\n" + "\n".join(lines)

    def framing_block(self) -> str:
        """Model framing notices for system prompts."""
        parts = [self.component_notice, self.tool_notice, self.memory_notice]
        return "\n".join(p for p in parts if p)


def load_jarvis_identity(
    config_path: str | Path | None = None,
) -> JarvisIdentity:
    """Load Jarvis identity from ``config/jarvis_identity.yaml``."""
    if config_path is None:
        from settings.paths import config_dir
        config_path = config_dir() / "jarvis_identity.yaml"

    path = Path(config_path)
    if not path.exists():
        logger.warning("Jarvis identity config not found at {}; using defaults", path)
        return JarvisIdentity()

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}

        identity = raw.get("identity", {})
        behavior = raw.get("behavior", {})
        framing = raw.get("model_framing", {})

        return JarvisIdentity(
            name=identity.get("name", "Jarvis"),
            role=identity.get("role", "Personal AI assistant system"),
            architecture=identity.get("architecture", ""),
            version=identity.get("version", "0.3.0-alpha"),
            description=identity.get("description", ""),
            capabilities=raw.get("capabilities", []),
            tone=behavior.get("tone", "Professional yet approachable"),
            default_style=behavior.get("default_style", "balanced"),
            safety_rules=behavior.get("safety", []),
            principles=behavior.get("principles", []),
            component_notice=framing.get("component_notice", ""),
            tool_notice=framing.get("tool_notice", ""),
            memory_notice=framing.get("memory_notice", ""),
        )
    except Exception as exc:
        logger.error("Failed to load Jarvis identity: {}", exc)
        return JarvisIdentity()
