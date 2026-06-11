from __future__ import annotations

import json
import logging
import shutil
import time
import zipfile
from pathlib import Path
from typing import Optional
from datetime import datetime

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.backup_manager")


class BackupError(Exception):
    pass


class BackupManager:
    """Export / import full JARVIS system state.

    Creates a .jarvis_backup.zip containing:
      - Session checkpoints (checkpoints/)
      - Vector store (vector_store/)
      - Memory database (memory.db)
      - Audit logs (audit/)
      - User config (config.yaml)
      - Successful procedures (procedures.json)
      - Preferences (preferences.json)
    """

    BACKUP_FILENAME = "jarvis_backup_{timestamp}.zip"
    MANIFEST_FILENAME = "manifest.json"

    def create_backup(self, output_dir: Optional[Path] = None) -> Path:
        output_dir = output_dir or paths.data_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = output_dir / self.BACKUP_FILENAME.format(timestamp=timestamp)

        sources = {
            "checkpoints": paths.checkpoint_dir,
            "vector_store": paths.vector_store_dir,
            "audit": paths.audit_dir,
            "memory.db": paths.memory_db,
            "config.yaml": paths.config_file,
        }

        manifest = {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "version": "4.6.0",
            "entries": [],
        }

        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for arcname, src in sources.items():
                    if not src.exists():
                        continue
                    if src.is_file():
                        zf.write(src, arcname)
                        manifest["entries"].append({"name": arcname, "size": src.stat().st_size})
                    elif src.is_dir():
                        for file_path in src.rglob("*"):
                            if file_path.is_file():
                                rel = f"{arcname}/{file_path.relative_to(src.parent)}"
                                zf.write(file_path, rel)
                                manifest["entries"].append({"name": rel, "size": file_path.stat().st_size})

                zf.writestr(self.MANIFEST_FILENAME, json.dumps(manifest, indent=2))
            logger.info("Backup created: %s", backup_path)
            return backup_path
        except Exception as e:
            raise BackupError(f"Failed to create backup: {e}") from e

    def restore_backup(self, backup_path: Path) -> dict:
        if not backup_path.exists():
            raise BackupError(f"Backup not found: {backup_path}")

        results = {"restored": [], "skipped": [], "errors": []}

        try:
            with zipfile.ZipFile(backup_path, "r") as zf:
                manifest_data = zf.read(self.MANIFEST_FILENAME)
                manifest = json.loads(manifest_data)

                target_map = {
                    "checkpoints": paths.checkpoint_dir,
                    "vector_store": paths.vector_store_dir,
                    "audit": paths.audit_dir,
                }

                for entry in manifest["entries"]:
                    name = entry["name"]
                    try:
                        if name in ("memory.db", "config.yaml"):
                            target = paths.data_dir / name
                            with zf.open(name) as src_f, open(target, "wb") as dst_f:
                                shutil.copyfileobj(src_f, dst_f)
                            results["restored"].append(name)
                        elif "/" in name:
                            prefix, rel_path = name.split("/", 1)
                            base = target_map.get(prefix)
                            if base:
                                target = base / rel_path
                                target.parent.mkdir(parents=True, exist_ok=True)
                                with zf.open(name) as src_f, open(target, "wb") as dst_f:
                                    shutil.copyfileobj(src_f, dst_f)
                                results["restored"].append(name)
                            else:
                                results["skipped"].append(name)
                        else:
                            results["skipped"].append(name)
                    except Exception as e:
                        results["errors"].append({"file": name, "error": str(e)})

            logger.info("Backup restored: %s", backup_path)
            return results
        except Exception as e:
            raise BackupError(f"Failed to restore backup: {e}") from e

    def list_backups(self, directory: Optional[Path] = None) -> list[dict]:
        directory = directory or paths.data_dir
        backups = []
        for f in sorted(directory.glob("jarvis_backup_*.zip")):
            try:
                with zipfile.ZipFile(f, "r") as zf:
                    manifest = json.loads(zf.read(self.MANIFEST_FILENAME))
                backups.append({
                    "path": str(f),
                    "created": manifest["created_at"],
                    "version": manifest["version"],
                    "entries": len(manifest["entries"]),
                    "size_bytes": f.stat().st_size,
                })
            except Exception:
                backups.append({
                    "path": str(f),
                    "error": "Could not read manifest",
                })
        return sorted(backups, key=lambda x: x.get("created", ""), reverse=True)


backup_manager = BackupManager()
