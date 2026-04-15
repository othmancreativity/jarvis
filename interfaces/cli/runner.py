"""Minimal interactive CLI until Phase 4."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from rich.console import Console
from rich.panel import Panel

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


def run_cli(settings: "AppSettings") -> None:
    console = Console()
    title = f"{settings.jarvis.name} - CLI (Phase 2 orchestrator)"
    console.print(Panel.fit(f"[bold green]{title}[/]", border_style="cyan"))
    console.print(
        "Type a message, or [bold]/exit[/] to quit. "
        "Rich layout and skills land in Phase 4.\n"
    )

    from core.bootstrap import get_chat_service

    service = get_chat_service(settings)

    while True:
        try:
            line = console.input("[bold]› [/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/]")
            break
        if not line:
            continue
        if line.lower() in ("/exit", "/quit", ":q"):
            break

        decision, chunks = service.stream_reply(line)
        reply = "".join(chunks)
        logger.debug("route={} model={}", decision.kind.value, decision.model)
        console.print(Panel(reply.rstrip(), title="Assistant", border_style="green"))


__all__ = ["run_cli"]
