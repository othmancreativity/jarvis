"""
JARVIS 4.5 — System Information Module
=======================================
Comprehensive system monitoring:
    - Platform and hardware info
    - CPU usage and details
    - Memory usage
    - Disk usage
    - Network interfaces
    - Running processes with filtering
    - Battery status
    - Temperature sensors (if available)
"""

from __future__ import annotations

import platform
import asyncio
import logging
from datetime import datetime
from typing import Optional, Any
from dataclasses import dataclass, field

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None

logger = logging.getLogger("jarvis.automation.system")


@dataclass
class CPUInfo:
    """CPU information."""
    physical_cores: int = 0
    logical_cores: int = 0
    current_freq_mhz: float = 0.0
    max_freq_mhz: float = 0.0
    usage_percent: float = 0.0
    usage_per_core: list[float] = field(default_factory=list)


@dataclass
class MemoryInfo:
    """Memory information."""
    total_gb: float = 0.0
    available_gb: float = 0.0
    used_gb: float = 0.0
    used_percent: float = 0.0
    swap_total_gb: float = 0.0
    swap_used_gb: float = 0.0


@dataclass
class DiskInfo:
    """Disk information."""
    device: str = ""
    mountpoint: str = ""
    filesystem: str = ""
    total_gb: float = 0.0
    used_gb: float = 0.0
    free_gb: float = 0.0
    used_percent: float = 0.0


@dataclass
class ProcessInfo:
    """Process information."""
    pid: int = 0
    name: str = ""
    status: str = ""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    memory_percent: float = 0.0
    created: str = ""
    cmdline: str = ""
    username: str = ""


class SystemInfoController:
    """
    Comprehensive system information controller.
    Provides detailed hardware, OS, and process information.
    """

    def __init__(self):
        self._has_psutil = HAS_PSUTIL

    async def get_info(self) -> dict:
        """Get comprehensive system information."""
        result = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor() or "Unknown",
                "architecture": platform.architecture()[0],
                "node": platform.node(),
                "python_version": platform.python_version(),
            }
        }

        if self._has_psutil:
            result.update(self._get_psutil_info())
        else:
            result["note"] = "Install psutil for detailed system info: pip install psutil"

        return {"status": "success", **result}

    def _get_psutil_info(self) -> dict:
        """Get detailed info via psutil."""
        info = {}

        # CPU
        try:
            cpu_freq = psutil.cpu_freq()
            info["cpu"] = {
                "physical_cores": psutil.cpu_count(logical=False) or 0,
                "logical_cores": psutil.cpu_count(logical=True) or 0,
                "current_freq_mhz": cpu_freq.current if cpu_freq else 0,
                "max_freq_mhz": cpu_freq.max if cpu_freq else 0,
                "usage_percent": psutil.cpu_percent(interval=0.5),
                "usage_per_core": psutil.cpu_percent(percpu=True),
            }
        except Exception as e:
            info["cpu"] = {"error": str(e)}

        # Memory
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            info["memory"] = {
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "used_percent": mem.percent,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
            }
        except Exception as e:
            info["memory"] = {"error": str(e)}

        # Disk
        try:
            disks = []
            for part in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    disks.append({
                        "device": part.device,
                        "mountpoint": part.mountpoint,
                        "filesystem": part.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "used_percent": round(usage.used / usage.total * 100, 1),
                    })
                except PermissionError:
                    continue
            info["disks"] = disks
        except Exception as e:
            info["disks"] = [{"error": str(e)}]

        # Boot time
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()
            info["boot_time"] = boot_time
        except Exception:
            pass

        # Battery
        try:
            battery = psutil.sensors_battery()
            if battery:
                info["battery"] = {
                    "percent": battery.percent,
                    "is_charging": battery.power_plugged,
                    "time_left_seconds": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
                }
        except Exception:
            pass

        return info

    async def get_processes(self, limit: int = 20, sort_by: str = "cpu") -> dict:
        """Get list of running processes."""
        if not self._has_psutil:
            return {"status": "error", "error": "psutil not installed"}

        try:
            processes = []
            for proc in psutil.process_iter([
                "pid", "name", "status", "cpu_percent", "memory_info",
                "memory_percent", "create_time", "cmdline", "username"
            ]):
                try:
                    info = proc.info
                    mem_mb = 0
                    if info.get("memory_info"):
                        mem_mb = round(info["memory_info"].rss / (1024 * 1024), 1)

                    cmd = ""
                    if info.get("cmdline"):
                        cmd = " ".join(info["cmdline"][:5])

                    created = ""
                    if info.get("create_time"):
                        created = datetime.fromtimestamp(info["create_time"]).isoformat()

                    processes.append({
                        "pid": info.get("pid", 0),
                        "name": info.get("name", ""),
                        "status": info.get("status", ""),
                        "cpu_percent": info.get("cpu_percent", 0.0) or 0.0,
                        "memory_mb": mem_mb,
                        "memory_percent": round(info.get("memory_percent") or 0, 1),
                        "created": created,
                        "cmdline": cmd[:100],
                        "username": info.get("username", ""),
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort
            sort_keys = {
                "cpu": lambda p: p["cpu_percent"],
                "memory": lambda p: p["memory_mb"],
                "name": lambda p: p["name"].lower(),
                "pid": lambda p: p["pid"],
            }
            reverse = sort_by in ("cpu", "memory")
            processes.sort(key=sort_keys.get(sort_by, sort_keys["cpu"]), reverse=reverse)

            return {
                "status": "success",
                "processes": processes[:limit],
                "count": len(processes[:limit]),
                "total_system_processes": len(list(psutil.pids())),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def get_process_by_pid(self, pid: int) -> dict:
        """Get detailed info about a specific process."""
        if not self._has_psutil:
            return {"status": "error", "error": "psutil not installed"}

        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                info = {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "exe": proc.exe(),
                    "cmdline": proc.cmdline(),
                    "status": proc.status(),
                    "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
                    "cpu_percent": proc.cpu_percent(interval=0.5),
                    "memory_mb": round(proc.memory_info().rss / (1024 * 1024), 1),
                    "memory_percent": round(proc.memory_percent(), 2),
                    "num_threads": proc.num_threads(),
                    "num_fds": proc.num_fds() if hasattr(proc, "num_fds") else None,
                    "io_counters": dict(proc.io_counters()._asdict()) if hasattr(proc, "io_counters") else None,
                }
                return {"status": "success", "process": info}
        except psutil.NoSuchProcess:
            return {"status": "error", "error": f"Process {pid} not found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def kill_process(self, pid: Optional[int] = None, name: Optional[str] = None,
                           signal_type: str = "term") -> dict:
        """Kill a process by PID or name."""
        if not self._has_psutil:
            return {"status": "error", "error": "psutil not installed"}

        killed = []
        sig = signal.SIGKILL if signal_type == "kill" else signal.SIGTERM

        try:
            if pid:
                proc = psutil.Process(pid)
                proc.send_signal(sig)
                killed.append({"pid": pid, "name": proc.name(), "signal": signal_type})
            elif name:
                for proc in psutil.process_iter(["pid", "name"]):
                    try:
                        if name.lower() in (proc.info.get("name") or "").lower():
                            proc.send_signal(sig)
                            killed.append({"pid": proc.pid, "name": proc.info.get("name"), "signal": signal_type})
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            else:
                return {"status": "error", "error": "Must provide pid or name"}

            return {"status": "success", "killed": killed, "count": len(killed)}
        except Exception as e:
            return {"status": "error", "error": str(e)}
