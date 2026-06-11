#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path

import click

from core.jarvis_core import JarvisCore
from config import config
from jarvis.backup_manager import backup_manager
from jarvis.self_updater import self_updater
from memory.memory_system import memory

logger = logging.getLogger("jarvis.cli")


@click.group()
@click.version_option(version="4.6.0", prog_name="jarvis")
def cli():
    """JARVIS 4.6 - AI Operating Assistant CLI"""


@cli.command()
@click.argument("text", nargs=-1, required=True)
def send(text):
    """Send a command to JARVIS and get a response."""
    command = " ".join(text)
    click.echo(f"Sending: {command}")

    async def _run():
        core = JarvisCore()
        await core.initialize()
        response = await core.process_input(command)
        click.echo(f"\nJARVIS: {response}")
        await core.stop()

    asyncio.run(_run())


@cli.group()
def backup():
    """Manage JARVIS backups."""


@backup.command(name="create")
def backup_create():
    """Create a full system backup."""
    click.echo("Creating backup...")
    try:
        path = backup_manager.create_backup()
        click.echo(f"Backup created: {path}")
    except Exception as e:
        click.echo(f"Backup failed: {e}", err=True)


@backup.command(name="restore")
@click.argument("path", type=click.Path(exists=True))
def backup_restore(path):
    """Restore from a backup file."""
    click.echo(f"Restoring from: {path}")
    try:
        results = backup_manager.restore_backup(Path(path))
        click.echo(f"Restored: {len(results['restored'])} files")
        if results["errors"]:
            for err in results["errors"]:
                click.echo(f"  Error: {err}", err=True)
    except Exception as e:
        click.echo(f"Restore failed: {e}", err=True)


@cli.command()
def status():
    """Show JARVIS system status."""
    click.echo("=== JARVIS 4.6 Status ===")
    click.echo(f"Model: {config.model}")
    click.echo(f"Language: {config.language}")
    click.echo(f"Bridge port: {config.bridge_port}")

    mem_stats = memory.get_stats()
    click.echo(f"Memory working size: {mem_stats.get('working_size', 'N/A')}")
    click.echo(f"Memory DB: {mem_stats.get('db_path', 'N/A')}")

    try:
        import psutil
        proc = psutil.Process()
        click.echo(f"Memory usage: {proc.memory_info().rss / 1024 / 1024:.1f} MB")
        click.echo(f"CPU usage: {proc.cpu_percent(interval=0.5)}%")
    except ImportError:
        pass


@cli.group()
def config_cmd():
    """View or modify JARVIS configuration."""


@config_cmd.command(name="get")
@click.argument("key", required=False)
def config_get(key):
    """Get a configuration value."""
    if key:
        value = getattr(config, key, None)
        if value is not None:
            click.echo(f"{key}: {value}")
        else:
            click.echo(f"Unknown key: {key}", err=True)
    else:
        for k, v in config.__dict__.items():
            if not k.startswith("_"):
                click.echo(f"{k}: {v}")


@config_cmd.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration value (runtime only)."""
    if hasattr(config, key):
        field_type = type(getattr(config, key))
        try:
            cast_value = field_type(value)
            setattr(config, key, cast_value)
            click.echo(f"Set {key} = {cast_value}")
        except ValueError:
            click.echo(f"Cannot convert '{value}' to {field_type.__name__}", err=True)
    else:
        click.echo(f"Unknown key: {key}", err=True)


@cli.command()
def update():
    """Check for and apply updates."""
    click.echo("Checking for updates...")

    async def _check():
        release = await self_updater.check_for_updates()
        if release:
            click.echo(f"New version available: {release.version}")
            click.echo(f"Download URL: {release.download_url}")
            if click.confirm("Download and apply update?"):
                zip_path = await self_updater.download_update(release)
                if zip_path:
                    click.echo("Applying update...")
                    if self_updater.apply_update(zip_path):
                        click.echo("Update applied. Restarting...")
                        self_updater.restart()
                    else:
                        click.echo("Update failed", err=True)
                else:
                    click.echo("Download failed", err=True)
        else:
            click.echo("You are on the latest version.")

    asyncio.run(_check())


if __name__ == "__main__":
    cli()
