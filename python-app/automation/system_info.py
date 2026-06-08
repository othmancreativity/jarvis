"""System information module."""

import platform
import asyncio


try:
    import psutil
except ImportError:
    psutil = None


class SystemInfoController:
    """Gather system information."""

    async def get_info(self) -> dict:
        """Get comprehensive system information."""
        result = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "Unknown",
            "architecture": platform.architecture()[0],
            "node": platform.node(),
        }

        if psutil:
            result.update({
                "cpu_count_physical": psutil.cpu_count(logical=False),
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "cpu_freq_mhz": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "ram_percent": psutil.virtual_memory().percent,
                "disk_total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
                "disk_free_gb": round(psutil.disk_usage("/").free / (1024**3), 2),
                "disk_percent": psutil.disk_usage("/").percent,
                "boot_time": psutil.boot_time(),
            })

        return {"status": "success", **result}

    async def get_processes(self, limit: int = 20) -> dict:
        """Get list of running processes."""
        if not psutil:
            return {"status": "error", "error": "psutil not installed"}

        processes = []
        for proc in sorted(
            psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]),
            key=lambda p: p.info.get("cpu_percent", 0) or 0,
            reverse=True,
        )[:limit]:
            processes.append(proc.info)

        return {"status": "success", "processes": processes}
