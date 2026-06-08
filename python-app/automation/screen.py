"""Screenshot and screen recording module."""

import asyncio
import base64
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    import mss
    import mss.tools
except ImportError:
    mss = None

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


class ScreenController:
    """Capture screenshots and record screen."""

    def __init__(self):
        self._recording = False
        self._record_start_time: Optional[float] = None
        self._record_output_path: Optional[str] = None
        self._capture_dir = Path.home() / ".jarvis" / "captures"
        self._capture_dir.mkdir(parents=True, exist_ok=True)

    async def screenshot(self, monitor: int = 0) -> dict:
        """Capture screenshot as base64 PNG."""
        if mss is None:
            raise ImportError("Install mss: pip install mss")

        try:
            with mss.mss() as sct:
                mon = sct.monitors[monitor] if monitor < len(sct.monitors) else sct.monitors[1]
                img = sct.grab(mon)
                png_bytes = mss.tools.to_png(img.rgb, img.size)
                b64 = base64.b64encode(png_bytes).decode("utf-8")

                # Also save to disk
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = self._capture_dir / filename
                with open(filepath, "wb") as f:
                    f.write(png_bytes)

                return {
                    "status": "success",
                    "base64": f"data:image/png;base64,{b64}",
                    "path": str(filepath),
                    "monitor": monitor,
                    "width": img.width,
                    "height": img.height,
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def record_start(self, duration_max: int = 60) -> dict:
        """Start screen recording. Requires confirmation (handled by caller)."""
        if cv2 is None or np is None:
            raise ImportError("Install opencv-python and numpy: pip install opencv-python numpy")
        if mss is None:
            raise ImportError("Install mss: pip install mss")

        if self._recording:
            return {"status": "error", "error": "Already recording"}

        self._recording = True
        self._record_start_time = time.time()
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        self._record_output_path = str(self._capture_dir / filename)

        # Start recording in background
        asyncio.create_task(self._record_loop(duration_max))

        return {
            "status": "recording_started",
            "path": self._record_output_path,
            "max_duration": duration_max,
        }

    async def _record_loop(self, duration_max: int):
        """Background recording loop."""
        if cv2 is None or np is None or mss is None:
            return

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 10.0

        with mss.mss() as sct:
            mon = sct.monitors[1]  # Primary monitor
            width = mon["width"]
            height = mon["height"]
            writer = cv2.VideoWriter(self._record_output_path, fourcc, fps, (width, height))

            try:
                while self._recording:
                    elapsed = time.time() - self._record_start_time
                    if elapsed > duration_max:
                        break

                    img = sct.grab(mon)
                    frame = np.array(img)
                    # Convert BGRA to BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    writer.write(frame)
                    await asyncio.sleep(1 / fps)

            finally:
                writer.release()
                self._recording = False

    async def record_stop(self) -> dict:
        """Stop recording and return video path."""
        if not self._recording:
            return {"status": "error", "error": "Not recording"}

        self._recording = False
        duration = time.time() - self._record_start_time if self._record_start_time else 0

        # Wait a moment for the loop to finish
        await asyncio.sleep(1)

        return {
            "status": "recording_stopped",
            "path": self._record_output_path,
            "duration_seconds": round(duration, 1),
        }
