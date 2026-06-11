from __future__ import annotations

import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Callable, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("jarvis.plugin_manager")


@dataclass
class PluginInfo:
    name: str
    version: str
    description: str
    module: Any = None
    tools: list[Callable] = field(default_factory=list)
    tasks: list[Callable] = field(default_factory=list)
    hooks: dict[str, Callable] = field(default_factory=dict)


class PluginManager:
    """Dynamic plugin system for JARVIS.

    Scans the plugins/ directory (and optionally entry points from
    pyproject.toml), imports Python modules, and registers
    tools/tasks/hooks with the core system.
    """

    def __init__(self, plugin_dirs: Optional[list[Path]] = None) -> None:
        self._plugins: dict[str, PluginInfo] = {}
        self._plugin_dirs: list[Path] = plugin_dirs or [
            Path(__file__).parent.parent / "plugins"
        ]
        self._tool_registry: dict[str, Callable] = {}

    @property
    def plugins(self) -> dict[str, PluginInfo]:
        return dict(self._plugins)

    def discover(self) -> list[str]:
        found: list[str] = []
        for plugin_dir in self._plugin_dirs:
            if not plugin_dir.exists():
                continue
            sys.path.insert(0, str(plugin_dir.parent))
            for path in sorted(plugin_dir.glob("*.py")):
                if path.name.startswith("_") and not path.name == "__init__.py":
                    continue
                name = path.stem
                if name in self._plugins:
                    continue
                try:
                    spec = importlib.util.spec_from_file_location(name, str(path))
                    if not spec or not spec.loader:
                        continue
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    info = self._extract_plugin_info(name, module)
                    self._plugins[name] = info
                    found.append(name)
                    logger.info("Loaded plugin: %s v%s", name, info.version)
                except Exception as e:
                    logger.error("Failed to load plugin %s: %s", name, e)
            sys.path.pop(0)
        return found

    def _extract_plugin_info(self, name: str, module: Any) -> PluginInfo:
        info = PluginInfo(
            name=getattr(module, "__plugin_name__", name),
            version=getattr(module, "__version__", "0.1.0"),
            description=getattr(module, "__description__", ""),
            module=module,
        )
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, "_plugin_tool"):
                info.tools.append(attr)
                self._tool_registry[attr.__name__] = attr
            if callable(attr) and hasattr(attr, "_plugin_task"):
                info.tasks.append(attr)
            if callable(attr) and hasattr(attr, "_plugin_hook"):
                hook_name = getattr(attr, "_plugin_hook")
                info.hooks[hook_name] = attr
        return info

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tool_registry.get(name)

    def list_tools(self) -> list[str]:
        return list(self._tool_registry.keys())

    def execute_hook(self, hook_name: str, *args: Any, **kwargs: Any) -> list[Any]:
        results = []
        for pinfo in self._plugins.values():
            hook = pinfo.hooks.get(hook_name)
            if hook:
                try:
                    results.append(hook(*args, **kwargs))
                except Exception as e:
                    logger.error("Plugin hook %s error in %s: %s", hook_name, pinfo.name, e)
        return results


plugin_manager = PluginManager()


def plugin_tool(func: Callable) -> Callable:
    """Decorator: mark a function as a plugin tool."""
    func._plugin_tool = True
    return func


def plugin_task(func: Callable) -> Callable:
    """Decorator: mark a function as a plugin task."""
    func._plugin_task = True
    return func


def plugin_hook(name: str):
    """Decorator: mark a function as a plugin hook."""
    def decorator(func: Callable) -> Callable:
        func._plugin_hook = name
        return func
    return decorator
