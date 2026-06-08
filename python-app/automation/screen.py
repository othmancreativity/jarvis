"""
JARVIS 4.5 — Screen Operations Module
======================================
Full screen capture and analysis:
    - Screenshot capture (monitor, region)
    - Screen recording with configurable FPS
    - OCR text extraction (requires pytesseract)
    - UI element detection (future: computer vision)
    - Mouse position tracking
    - Color sampling
"""

from __future__ import annotations

import asyncio
import base64
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
from dataclasses import dataclass

try:
    import mss
    import mss.tools
    HAS_MSS = True
except ImportError:
    HAS_MSS = False
    mss = None

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    cv2 = None
    np = None

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    Image = None

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    pytesseract = None

logger = logging.getLogger("jarvis.automation.screen")


@dataclass
class Region:
    """Screen region definition."""
    x: int
    y: int
    width: int
    height: int


class ScreenController:
    """
    Full-featured screen capture and analysis controller.
    Supports screenshots, recording, OCR, and region capture.
    """

    def __init__(self):
        self._recording = False
        self._record_start_time: Optional[float] = None
        self._record_output_path: Optional[str] = None
        self._record_task: Optional[asyncio.Task] = None
        self._capture_dir = Path.home() / ".jarvis" / "captures"
        self._capture_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_mss(self):
        """Ensure mss is available."""
        if not HAS_MSS:
            raise ImportError("Install mss: pip install mss")

    def _ensure_cv2(self):
        """Ensure opencv is available."""
        if not HAS_CV2:
            raise ImportError("Install opencv-python: pip install opencv-python")

    def _get_filename(self, prefix: str, ext: str) -> str:
        """Generate a timestamped filename."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{ts}.{ext}"

    # ── Screenshot ─────────────────────────────────────────────────────

    async def screenshot(self, monitor: int = 0, region: Optional[dict] = None) -> dict:
        """
        Capture a screenshot.

        Args:
            monitor: Monitor index (0 = primary/all)
            region: Optional dict with x, y, width, height
        """
        try:
            self._ensure_mss()

            with mss.mss() as sct:
                if region:
                    # Capture specific region
                    r = Region(**region)
                    mon = {"left": r.x, "top": r.y, "width": r.width, "height": r.height}
                elif monitor == 0:
                    # Capture primary monitor (index 1 in mss, 0 is all)
                    mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                else:
                    mon = sct.monitors[monitor] if monitor < len(sct.monitors) else sct.monitors[1]

                img = sct.grab(mon)
                png_bytes = mss.tools.to_png(img.rgb, img.size)
                b64 = base64.b64encode(png_bytes).decode("utf-8")

                filename = self._get_filename("screenshot", "png")
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
                    "format": "png",
                }
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Screen Recording ───────────────────────────────────────────────

    async def record_start(self, duration_max: int = 60, monitor: int = 0, fps: int = 10) -> dict:
        """Start screen recording."""
        try:
            self._ensure_mss()
            self._ensure_cv2()

            if self._recording:
                return {"status": "error", "error": "Already recording"}

            self._recording = True
            self._record_start_time = time.time()
            filename = self._get_filename("recording", "mp4")
            self._record_output_path = str(self._capture_dir / filename)

            self._record_task = asyncio.create_task(
                self._record_loop(duration_max, monitor, fps)
            )

            return {
                "status": "recording_started",
                "path": self._record_output_path,
                "max_duration": duration_max,
                "fps": fps,
            }
        except ImportError as e:
            return {"status": "error", "error": str(e)}
        except Exception as e:
            self._recording = False
            logger.error(f"Record start error: {e}")
            return {"status": "error", "error": str(e)}

    async def _record_loop(self, duration_max: int, monitor: int, fps: int):
        """Background recording loop."""
        if not HAS_MSS or not HAS_CV2 or not np:
            return

        try:
            with mss.mss() as sct:
                mon = sct.monitors[monitor] if monitor < len(sct.monitors) else sct.monitors[1]
                width = mon["width"]
                height = mon["height"]

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(self._record_output_path, fourcc, fps, (width, height))

                try:
                    while self._recording:
                        elapsed = time.time() - self._record_start_time
                        if elapsed > duration_max:
                            break

                        img = sct.grab(mon)
                        frame = np.array(img)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                        writer.write(frame)
                        await asyncio.sleep(1 / fps)
                finally:
                    writer.release()
                    self._recording = False
        except Exception as e:
            logger.error(f"Recording loop error: {e}")
            self._recording = False

    async def record_stop(self) -> dict:
        """Stop screen recording."""
        if not self._recording:
            return {"status": "error", "error": "Not recording"}

        self._recording = False
        duration = time.time() - self._record_start_time if self._record_start_time else 0

        if self._record_task:
            try:
                await asyncio.wait_for(self._record_task, timeout=5)
            except asyncio.TimeoutError:
                self._record_task.cancel()
            except Exception as e:
                logger.error(f"Error stopping recording: {e}")

        await asyncio.sleep(0.5)  # Wait for file to flush

        return {
            "status": "recording_stopped",
            "path": self._record_output_path,
            "duration_seconds": round(duration, 1),
        }

    # ── OCR ────────────────────────────────────────────────────────────

    async def ocr(self, monitor: int = 0, region: Optional[dict] = None,
                  language: str = "eng") -> dict:
        """
        Perform OCR on screen or region to extract text.
        Requires pytesseract and tesseract-ocr.
        """
        if not HAS_TESSERACT:
            return {
                "status": "error",
                "error": "OCR not available. Install: pip install pytesseract && apt-get install tesseract-ocr",
            }

        try:
            self._ensure_mss()

            with mss.mss() as sct:
                if region:
                    r = Region(**region)
                    mon = {"left": r.x, "top": r.y, "width": r.width, "height": r.height}
                elif monitor == 0:
                    mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                else:
                    mon = sct.monitors[monitor] if monitor < len(sct.monitors) else sct.monitors[1]

                img = sct.grab(mon)

                if HAS_PIL:
                    pil_img = Image.frombytes("RGB", img.size, img.bgra, raw="BGRX")
                    text = pytesseract.image_to_string(pil_img, lang=language)
                    data = pytesseract.image_to_data(pil_img, lang=language, output_type=pytesseract.Output.DICT)

                    # Calculate average confidence
                    confidences = [int(c) for c in data["conf"] if int(c) > 0]
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                else:
                    # Use mss raw data
                    png = mss.tools.to_png(img.rgb, img.size)
                    # Would need to save and OCR - simplified
                    text = ""
                    avg_confidence = 0

                return {
                    "status": "success",
                    "text": text.strip(),
                    "confidence": round(avg_confidence, 1),
                    "language": language,
                }
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Mouse Position ─────────────────────────────────────────────────

    async def get_mouse_position(self) -> dict:
        """Get current mouse cursor position."""
        try:
            if HAS_MSS:
                with mss.mss() as sct:
                    # mss doesn't directly give mouse position
                    # Use alternative methods per platform
                    import platform
                    system = platform.system()
                    if system == "Darwin":
                        result = await asyncio.create_subprocess_shell(
                            "osascript -e 'tell application \"System Events\" to get position of first mouse'",
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE,
                        )
                        stdout, _ = await result.communicate()
                        pos = stdout.decode().strip()
                        return {"status": "success", "position": pos}
                    elif system == "Linux":
                        result = await asyncio.create_subprocess_shell(
                            "xdotool getmouselocation",
                            stdout=asyncio.subprocess.PIPE,
                        )
                        stdout, _ = await result.communicate()
                        return {"status": "success", "position": stdout.decode().strip()}
            return {"status": "error", "error": "Mouse position detection not available"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Color Sampling ─────────────────────────────────────────────────

    async def sample_color(self, x: int, y: int, monitor: int = 0) -> dict:
        """Sample the color at a specific screen coordinate."""
        try:
            self._ensure_mss()

            with mss.mss() as sct:
                region = {"left": x, "top": y, "width": 1, "height": 1}
                img = sct.grab(region)
                pixel = img.pixels[0]
                r, g, b = pixel[2], pixel[1], pixel[0]  # BGRA order
                hex_color = f"#{r:02x}{g:02x}{b:02x}"

                return {
                    "status": "success",
                    "x": x,
                    "y": y,
                    "rgb": {"r": r, "g": g, "b": b},
                    "hex": hex_color,
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}
