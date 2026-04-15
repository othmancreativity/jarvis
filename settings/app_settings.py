"""Pydantic models for ``config/settings.yaml`` validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JarvisBlock(BaseModel):
    name: str = "Jarvis"
    language: list[str] = Field(default_factory=lambda: ["ar", "en"])
    wake_word: str = "hey_jarvis"


class ModelsBlock(BaseModel):
    default_llm: str = "qwen2.5:7b"
    code_llm: str = "qwen2.5-coder:7b"
    fast_llm: str = "gemma3:4b"
    deep_llm: str = "qwen3:8b"
    vision_llm: str = "llava:7b"


class WebInterface(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8080


class CliInterface(BaseModel):
    rich_markup: bool = True


class TelegramInterface(BaseModel):
    enabled: bool = False
    polling_timeout: int = 30


class GuiInterface(BaseModel):
    toolkit: str = "pyqt6"  # pyqt6 | tkinter


class InterfacesBlock(BaseModel):
    web: WebInterface = Field(default_factory=WebInterface)
    cli: CliInterface = Field(default_factory=CliInterface)
    telegram: TelegramInterface = Field(default_factory=TelegramInterface)
    gui: GuiInterface = Field(default_factory=GuiInterface)


class PathsBlock(BaseModel):
    data: str = "data"
    logs: str = "logs"
    chroma: str = "data/chroma"
    sqlite: str = "data/jarvis.db"


class HardwareBlock(BaseModel):
    gpu_vram_limit_gb: float = 5.5
    use_half_precision: bool = True
    max_ollama_concurrent: int = 1


class LoggingBlock(BaseModel):
    level: str = "INFO"


class AppSettings(BaseModel):
    jarvis: JarvisBlock = Field(default_factory=JarvisBlock)
    models: ModelsBlock = Field(default_factory=ModelsBlock)
    interfaces: InterfacesBlock = Field(default_factory=InterfacesBlock)
    paths: PathsBlock = Field(default_factory=PathsBlock)
    hardware: HardwareBlock = Field(default_factory=HardwareBlock)
    logging: LoggingBlock = Field(default_factory=LoggingBlock)

    def resolved_paths(self, root: Any) -> dict[str, Any]:
        """Return absolute Path objects for key dirs (``root`` = project root Path)."""
        from pathlib import Path as P

        r = P(root)
        return {
            "data": r / self.paths.data,
            "logs": r / self.paths.logs,
            "chroma": r / self.paths.chroma,
            "sqlite": r / self.paths.sqlite,
        }
