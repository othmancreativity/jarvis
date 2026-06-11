"""
JARVIS 4.5 — Wake Word Detection
==================================
Lightweight wake word system. Supports:
    - Keyboard shortcut trigger (Ctrl+Shift+J)
    - Text-based activation via message bus
    - Optional Porcupine integration for voice wake word

Design: The wake word system must be extremely lightweight.
It does NOT keep a heavy model running. Instead it uses:
    1. A global hotkey listener (pynput)
    2. A UDP listener for remote activation
    3. Optional: Porcupine for actual voice wake word
"""

from __future__ import annotations

import logging
import asyncio
import threading
import socket
import time
from typing import Optional, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("jarvis.wake_word")


class WakeMethod(str, Enum):
    """Methods for waking JARVIS."""
    HOTKEY = "hotkey"
    UDP = "udp"
    VOICE = "voice"
    MANUAL = "manual"


@dataclass
class WakeEvent:
    """A wake event."""
    method: WakeMethod
    timestamp: float
    source: str = "unknown"


class WakeWordSystem:
    """
    Lightweight wake word detection system.
    Uses multiple activation methods to minimize resource usage.
    """

    UDP_PORT = 19876
    TRIGGER_PHRASES = ["jarvis", "hey jarvis", "ok jarvis", "wake up"]

    def __init__(self):
        self._callbacks: list[Callable[[WakeEvent], None]] = []
        self._running = False
        self._hotkey_thread: Optional[threading.Thread] = None
        self._udp_thread: Optional[threading.Thread] = None
        self._task: Optional[asyncio.Task] = None

    def on_wake(self, callback: Callable[[WakeEvent], None]) -> None:
        """Register a callback for wake events."""
        self._callbacks.append(callback)

    def _notify(self, event: WakeEvent) -> None:
        """Notify all wake listeners."""
        for cb in self._callbacks:
            try:
                cb(event)
            except Exception as e:
                logger.error(f"Wake callback error: {e}")

    def start(self) -> None:
        """Start the wake word system."""
        self._running = True
        logger.info("Wake word system starting...")

        # Start hotkey listener
        self._hotkey_thread = threading.Thread(target=self._hotkey_listener, daemon=True)
        self._hotkey_thread.start()

        # Start UDP listener
        self._udp_thread = threading.Thread(target=self._udp_listener, daemon=True)
        self._udp_thread.start()

        logger.info("Wake word system active. Press Ctrl+Shift+J or send UDP to port 19876")

    def stop(self) -> None:
        """Stop the wake word system."""
        self._running = False
        logger.info("Wake word system stopped")

    def trigger(self, method: WakeMethod = WakeMethod.MANUAL, source: str = "manual") -> None:
        """Manually trigger wake."""
        event = WakeEvent(method=method, timestamp=time.time(), source=source)
        logger.info(f"Wake triggered via {method.value}")
        self._notify(event)

    def check_text_trigger(self, text: str) -> bool:
        """Check if text contains a wake phrase."""
        text_lower = text.lower().strip()
        return any(phrase in text_lower for phrase in self.TRIGGER_PHRASES)

    def _hotkey_listener(self) -> None:
        """Listen for global hotkey (Ctrl+Shift+J)."""
        try:
            from pynput import keyboard

            def on_hotkey():
                self.trigger(WakeMethod.HOTKEY, "keyboard")

            hotkey = keyboard.HotKey(
                keyboard.HotKey.parse("<ctrl>+<shift>+j"),
                on_hotkey,
            )

            with keyboard.Listener(
                on_press=hotkey.press,
                on_release=hotkey.release,
            ) as listener:
                while self._running:
                    listener.join(timeout=1)

        except ImportError:
            logger.debug("pynput not installed, hotkey wake disabled")
        except Exception as e:
            logger.error(f"Hotkey listener error: {e}")

    def _udp_listener(self) -> None:
        """Listen for UDP wake packets."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(1.0)
            sock.bind(("0.0.0.0", self.UDP_PORT))

            while self._running:
                try:
                    data, addr = sock.recvfrom(1024)
                    message = data.decode("utf-8").strip()
                    if message.lower() in self.TRIGGER_PHRASES:
                        self.trigger(WakeMethod.UDP, f"{addr[0]}:{addr[1]}")
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.debug(f"UDP listener error: {e}")

            sock.close()
        except Exception as e:
            logger.error(f"UDP listener error: {e}")


# Singleton
wake_system = WakeWordSystem()
