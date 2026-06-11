from __future__ import annotations

import asyncio
import logging
import platform
from datetime import datetime

logger = logging.getLogger("jarvis.automation.system")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class SystemInfoController:
    async def get_info(self) -> dict:
        result = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor() or "Unknown",
                "python_version": platform.python_version(),
            }
        }
        if HAS_PSUTIL:
            try:
                mem = psutil.virtual_memory()
                result["memory"] = {
                    "total_gb": round(mem.total / (1024**3), 2),
                    "available_gb": round(mem.available / (1024**3), 2),
                    "used_gb": round(mem.used / (1024**3), 2),
                    "used_percent": mem.percent,
                }
                result["cpu"] = {
                    "physical_cores": psutil.cpu_count(logical=False) or 0,
                    "logical_cores": psutil.cpu_count(logical=True) or 0,
                    "usage_percent": psutil.cpu_percent(interval=0.5),
                }
                disks = []
                for part in psutil.disk_partitions(all=False):
                    try:
                        usage = psutil.disk_usage(part.mountpoint)
                        disks.append({
                            "device": part.device,
                            "mountpoint": part.mountpoint,
                            "total_gb": round(usage.total / (1024**3), 2),
                            "free_gb": round(usage.free / (1024**3), 2),
                            "used_percent": round(usage.used / usage.total * 100, 1),
                        })
                    except PermissionError:
                        continue
                result["disks"] = disks
            except Exception as e:
                result["error"] = str(e)
        else:
            result["note"] = "Install psutil for detailed info"
        return {"status": "success", **result}

    async def get_processes(self, limit: int = 20, sort_by: str = "cpu") -> dict:
        if not HAS_PSUTIL:
            return {"status": "error", "error": "psutil not installed"}
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                mem_mb = round(proc.info["memory_info"].rss / (1024 * 1024), 1) if proc.info.get("memory_info") else 0
                processes.append({
                    "pid": proc.info["pid"],
                    "name": proc.info["name"] or "",
                    "cpu_percent": proc.info["cpu_percent"] or 0.0,
                    "memory_mb": mem_mb,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda p: p.get(sort_by, 0), reverse=(sort_by != "name"))
        return {"status": "success", "processes": processes[:limit], "count": len(processes[:limit])}

    async def kill_process(self, pid: int = None, name: str = None,
                           signal_type: str = "term") -> dict:
        if not HAS_PSUTIL:
            return {"status": "error", "error": "psutil not installed"}
        import signal
        sig = signal.SIGKILL if signal_type == "kill" else signal.SIGTERM
        killed = []
        try:
            if pid:
                proc = psutil.Process(pid)
                proc.send_signal(sig)
                killed.append({"pid": pid, "name": proc.name()})
            elif name:
                for proc in psutil.process_iter(["pid", "name"]):
                    if name.lower() in (proc.info.get("name") or "").lower():
                        proc.send_signal(sig)
                        killed.append({"pid": proc.pid, "name": proc.info.get("name")})
            return {"status": "success", "killed": killed, "count": len(killed)}
        except Exception as e:
            return {"status": "error", "error": str(e)}
