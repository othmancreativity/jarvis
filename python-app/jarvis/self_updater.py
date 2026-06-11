from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import aiohttp
import aiofiles
from packaging.version import Version, InvalidVersion

logger = logging.getLogger("jarvis.self_updater")

try:
    import pyproject_parser
    HAS_PP = False
except ImportError:
    HAS_PP = False


@dataclass
class ReleaseInfo:
    version: str
    download_url: str
    checksum: Optional[str] = None
    release_notes: str = ""


class SelfUpdater:
    """Compares current version with latest GitHub release and updates.

    Downloads the release zip, verifies checksum, replaces files, and
    restarts the application.
    """

    GITHUB_REPO = "othmancreativity/jarvis"
    GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"

    def __init__(self) -> None:
        self._current_version: Optional[str] = None
        self._load_current_version()

    def _load_current_version(self) -> None:
        pyproj = Path(__file__).parent.parent / "pyproject.toml"
        if pyproj.exists():
            try:
                import tomllib
                data = tomllib.loads(pyproj.read_text(encoding="utf-8"))
                self._current_version = data.get("project", {}).get("version", "0.0.0")
            except Exception:
                self._current_version = "0.0.0"
        else:
            self._current_version = "0.0.0"

    @property
    def current_version(self) -> str:
        return self._current_version or "0.0.0"

    async def check_for_updates(self) -> Optional[ReleaseInfo]:
        url = self.GITHUB_API.format(repo=self.GITHUB_REPO)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    tag = data.get("tag_name", "").lstrip("v")
                    if not tag:
                        return None

                    try:
                        latest = Version(tag)
                        current = Version(self.current_version)
                        if latest <= current:
                            return None
                    except InvalidVersion:
                        return None

                    assets = data.get("assets", [])
                    download_url = ""
                    checksum = ""
                    for asset in assets:
                        name = asset.get("name", "")
                        if name.endswith(".zip"):
                            download_url = asset["browser_download_url"]
                        elif name.endswith(".sha256"):
                            checksum_url = asset["browser_download_url"]
                            async with session.get(checksum_url, timeout=10) as cs_resp:
                                checksum = (await cs_resp.text()).strip()

                    if not download_url:
                        download_url = data.get("zipball_url", "")

                    return ReleaseInfo(
                        version=tag,
                        download_url=download_url,
                        checksum=checksum,
                        release_notes=data.get("body", ""),
                    )
        except Exception as e:
            logger.error("Update check failed: %s", e)
            return None

    async def download_update(self, release: ReleaseInfo,
                               target_dir: Optional[Path] = None) -> Optional[Path]:
        target_dir = target_dir or Path.home() / ".jarvis" / "updates"
        target_dir.mkdir(parents=True, exist_ok=True)
        zip_path = target_dir / f"jarvis-{release.version}.zip"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(release.download_url, timeout=120) as resp:
                    if resp.status != 200:
                        logger.error("Download failed: HTTP %s", resp.status)
                        return None
                    async with aiofiles.open(zip_path, "wb") as f:
                        await f.write(await resp.read())
        except Exception as e:
            logger.error("Download failed: %s", e)
            return None

        if release.checksum:
            sha256 = hashlib.sha256()
            sha256.update(zip_path.read_bytes())
            if sha256.hexdigest() != release.checksum:
                logger.error("Checksum mismatch")
                return None

        return zip_path

    def apply_update(self, zip_path: Path) -> bool:
        app_dir = Path(__file__).parent.parent
        backup_dir = app_dir.parent / ".jarvis_backup"
        backup_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Backup current files
            for item in app_dir.iterdir():
                if item.name in ("__pycache__", ".pytest_cache", ".jarvis_backup"):
                    continue
                dst = backup_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dst)

            # Extract update
            extract_dir = zip_path.parent / f"extracted_{zip_path.stem}"
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            # Copy files (skip pyproject-specific)
            for item in extract_dir.iterdir():
                for sub in item.rglob("*"):
                    if sub.is_file() and sub.suffix in (".py", ".toml", ".txt", ".json", ".yaml", ".md"):
                        rel = sub.relative_to(item)
                        target = app_dir / rel
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(sub, target)

            shutil.rmtree(extract_dir, ignore_errors=True)
            logger.info("Update applied successfully")
            return True
        except Exception as e:
            logger.error("Update apply failed: %s", e)
            return False

    def restart(self) -> None:
        logger.info("Restarting JARVIS...")
        python = sys.executable
        script = Path(__file__).parent.parent / "main.py"
        if script.exists():
            import subprocess
            subprocess.Popen([python, str(script)], shell=True)
        sys.exit(0)


self_updater = SelfUpdater()
