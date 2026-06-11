from __future__ import annotations

import asyncio
import base64
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger("jarvis.automation.screen")

try:
    import mss
    import mss.tools
    HAS_MSS = True
except ImportError:
    HAS_MSS = False


class ScreenController:
    def __init__(self) -> None:
        self._capture_dir = Path.home() / ".jarvis" / "captures"
        self._capture_dir.mkdir(parents=True, exist_ok=True)

    async def screenshot(self, monitor: int = 0, region: Optional[dict] = None) -> dict:
        if not HAS_MSS:
            return {"status": "error", "error": "mss not installed. Run: pip install mss"}
        try:
            with mss.mss() as sct:
                if region:
                    mon = {"left": region["x"], "top": region["y"],
                           "width": region["width"], "height": region["height"]}
                elif monitor == 0:
                    mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                else:
                    mon = sct.monitors[monitor] if monitor < len(sct.monitors) else sct.monitors[1]

                img = sct.grab(mon)
                png_bytes = mss.tools.to_png(img.rgb, img.size)
                b64 = base64.b64encode(png_bytes).decode("utf-8")
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = self._capture_dir / filename
                with open(filepath, "wb") as f:
                    f.write(png_bytes)
                return {
                    "status": "success",
                    "base64": f"data:image/png;base64,{b64}",
                    "path": str(filepath),
                    "width": img.width,
                    "height": img.height,
                }
        except Exception as e:
            logger.error("Screenshot error: %s", e)
            return {"status": "error", "error": str(e)}

    async def ocr(self, monitor: int = 0, region: Optional[dict] = None,
                  language: str = "eng") -> dict:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return {"status": "error", "error": "OCR not available. Install: pip install pytesseract Pillow"}

        if not HAS_MSS:
            return {"status": "error", "error": "mss not installed"}

        try:
            with mss.mss() as sct:
                if region:
                    mon = {"left": region["x"], "top": region["y"],
                           "width": region["width"], "height": region["height"]}
                else:
                    mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                img = sct.grab(mon)
                pil_img = Image.frombytes("RGB", img.size, img.bgra, raw="BGRX")
                text = pytesseract.image_to_string(pil_img, lang=language)
                return {"status": "success", "text": text.strip(), "language": language}
        except Exception as e:
            return {"status": "error", "error": str(e)}
