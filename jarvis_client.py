#!/usr/bin/env python3
"""
JARVIS - Local Desktop Voice Assistant
Production-grade, local-first Voice Assistant with real-time waveform visualization,
local STT/TTS pipeline, and n8n integration.

Architecture:
  - GUI: CustomTkinter (main thread)
  - Audio In: sounddevice InputStream (callback thread)
  - Audio Out: sounddevice OutputStream (callback thread)
  - STT: faster-whisper (ThreadPoolExecutor)
  - TTS: edge-tts (asyncio worker thread)
  - n8n Bridge: aiohttp (asyncio worker thread)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import queue
import sys
import tempfile
import threading
import time
import uuid
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Optional

import aiohttp
import av
import customtkinter as ctk
import faster_whisper
import google.generativeai as genai
import numpy as np
import sounddevice as sd

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("JARVIS")

# ── Configuration ────────────────────────────────────────────────────────────
APP_NAME = "JARVIS Neural Interface v1.0"

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/jarvis")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.environ.get("WHISPER_DEVICE", "auto")  # "auto", "cpu", "cuda"
WHISPER_COMPUTE = os.environ.get("WHISPER_COMPUTE", "auto")  # "auto", "float16", "int8"

SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
CHANNELS = 1
DTYPE = np.float32

VAD_THRESHOLD = float(os.environ.get("VAD_THRESHOLD", "0.025"))
VAD_SILENCE_TIMEOUT = float(os.environ.get("VAD_SILENCE_TIMEOUT", "1.5"))
MAX_RECORDING_TIME = 30.0

WAVEFORM_BUFFER_SIZE = 500
WAVEFORM_HEIGHT = 240
WAVEFORM_WIDTH = 960

TTS_VOICES = {
    "ar": "ar-EG-ShakirNeural",
    "en": "en-US-AriaNeural",
}

# ── Color Palette ───────────────────────────────────────────────────────────
COLOR_BG_DARK = "#05050a"
COLOR_BG = "#0a0a12"
COLOR_BG_LIGHT = "#14142a"
COLOR_ACCENT = "#00d4ff"
COLOR_ACCENT_DIM = "#006688"
COLOR_ACCENT_GLOW = "#00aaff"
COLOR_TEXT = "#d0d0e0"
COLOR_TEXT_DIM = "#606080"
COLOR_SUCCESS = "#00ff88"
COLOR_WARNING = "#ffaa00"
COLOR_ERROR = "#ff3355"

WAVE_COLORS = {
    "IDLE": "#006688",
    "LISTENING": "#00ddff",
    "THINKING": COLOR_WARNING,
    "SPEAKING": "#00ff88",
}


# ── Enums & Data Classes ────────────────────────────────────────────────────
class State(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"


@dataclass
class AppConfig:
    n8n_url: str = N8N_WEBHOOK_URL
    whisper_model: str = WHISPER_MODEL_SIZE
    whisper_device: str = WHISPER_DEVICE
    whisper_compute: str = WHISPER_COMPUTE
    vad_threshold: float = VAD_THRESHOLD
    vad_silence_timeout: float = VAD_SILENCE_TIMEOUT


# ── Helpers ──────────────────────────────────────────────────────────────────
def detect_language(text: str) -> str:
    for ch in text:
        if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F' or '\u08A0' <= ch <= '\u08FF':
            return "ar"
    return "en"


def rms(data: np.ndarray) -> float:
    if data.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(data.astype(np.float64) ** 2)))


def alpha_blend(hex_color: str, alpha: float, bg: tuple[int, int, int] = (5, 5, 10)) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    nr = int(r * alpha + bg[0] * (1 - alpha))
    ng = int(g * alpha + bg[1] * (1 - alpha))
    nb = int(b * alpha + bg[2] * (1 - alpha))
    return f"#{nr:02x}{ng:02x}{nb:02x}"


# ── AudioWaveformWidget ──────────────────────────────────────────────────────
class AudioWaveformWidget(ctk.CTkFrame):
    """Animated real-time audio waveform with neon glow. ~60 fps via tkinter after()."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=COLOR_BG)

        self.state: State = State.IDLE
        self._buffer = deque([0.0] * WAVEFORM_BUFFER_SIZE, maxlen=WAVEFORM_BUFFER_SIZE)
        self._playback_buf = deque([0.0] * WAVEFORM_BUFFER_SIZE, maxlen=WAVEFORM_BUFFER_SIZE)
        self._phase = 0.0
        self._t = 0.0
        self._pulse = 0.0
        self._pulse_dir = 1
        self._spin = 0.0

        self.canvas = ctk.CTkCanvas(
            self,
            highlightthickness=0,
            bg=COLOR_BG_DARK,
            takefocus=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

        self.after(16, self._animate)

    def set_state(self, s: State) -> None:
        self.state = s

    def feed_samples(self, samples: np.ndarray) -> None:
        for v in samples.flat:
            self._buffer.append(float(v))

    def feed_playback(self, samples: np.ndarray) -> None:
        for v in samples.flat:
            self._playback_buf.append(float(v))

    # ── animation dispatcher ──
    def _animate(self) -> None:
        self.canvas.delete("all")
        w = max(self.canvas.winfo_width(), 200)
        h = max(self.canvas.winfo_height(), 60)
        if self.state == State.IDLE:
            self._draw_idle(w, h)
        elif self.state == State.LISTENING:
            self._draw_listening(w, h)
        elif self.state == State.THINKING:
            self._draw_thinking(w, h)
        elif self.state == State.SPEAKING:
            self._draw_speaking(w, h)
        else:
            self._draw_idle(w, h)
        self._t += 0.016
        self.after(16, self._animate)

    # ── draw helpers ──
    def _draw_idle(self, w: int, h: int) -> None:
        cx, cy = w // 2, h // 2
        self._phase += 0.025
        amp = 20 + 6 * np.sin(self._t * 0.6)
        pts = []
        for i in range(w):
            y = cy + amp * np.sin(2 * np.pi * i / (w * 0.35) + self._phase)
            pts.extend([i, y])
        self._stroke(pts, WAVE_COLORS["IDLE"])

    def _draw_listening(self, w: int, h: int) -> None:
        cy = h // 2
        buf = list(self._buffer)
        n = len(buf)
        if n < 4:
            return
        mx = max((abs(x) for x in buf), default=0.001)
        scale = (h * 0.42) / mx
        pts = []
        step = max(1, n // w)
        for i in range(0, n, step):
            x = int(i * w / n)
            y = cy + buf[i] * scale
            pts.extend([x, y])
        self._stroke(pts, WAVE_COLORS["LISTENING"])

    def _draw_thinking(self, w: int, h: int) -> None:
        cx, cy = w // 2, h // 2
        self._pulse += 0.05 * self._pulse_dir
        if self._pulse > 1.0:
            self._pulse_dir = -1
        elif self._pulse < 0.0:
            self._pulse_dir = 1
        self._spin += 0.06

        r = 30 + self._pulse * 25
        br = 0.5 + self._pulse * 0.5

        for i in range(3):
            rr = r + i * 14
            a = max(0.1, 0.5 - i * 0.15) * br
            self.canvas.create_oval(
                cx - rr, cy - rr, cx + rr, cy + rr,
                outline=alpha_blend(WAVE_COLORS["THINKING"], a),
                width=3 - i * 0.8,
            )
        # rotating arc segments
        for i in range(4):
            start = self._spin + i * 90
            ext = 40 + self._pulse * 35
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=ext,
                outline=alpha_blend(WAVE_COLORS["THINKING"], 0.85),
                width=2,
            )

    def _draw_speaking(self, w: int, h: int) -> None:
        cy = h // 2
        buf = list(self._playback_buf)
        n = len(buf)
        if n < 4:
            self._draw_idle(w, h)
            return
        mx = max((abs(x) for x in buf), default=0.001)
        scale = (h * 0.44) / mx
        pts = []
        step = max(1, n // w)
        for i in range(0, n, step):
            x = int(i * w / n)
            y = cy + buf[i] * scale
            pts.extend([x, y])
        self._stroke(pts, WAVE_COLORS["SPEAKING"])

    def _stroke(self, pts: list[float], color: str) -> None:
        layers = [(0.12, 6), (0.25, 4), (0.55, 2), (1.0, 1)]
        for a, w in layers:
            if len(pts) >= 4:
                self.canvas.create_line(
                    *pts, fill=alpha_blend(color, a),
                    width=w, smooth=True, splinesteps=60,
                )


# ── AudioManager ─────────────────────────────────────────────────────────────
class AudioManager:
    """Manages mic input (VAD) and playback. Runs callbacks in audio threads."""

    def __init__(self, config: AppConfig):
        self.config = config
        self._stream: sd.InputStream | None = None
        self._rec_buf: list[np.ndarray] = []
        self._is_recording = False
        self._speech_frames = 0
        self._silence_frames = 0
        self._rec_start_time = 0.0
        self.muted = False

        # external callbacks
        self.on_waveform_sample: Callable[[np.ndarray], None] | None = None
        self.on_vad_change: Callable[[bool], None] | None = None
        self.on_utterance: Callable[[np.ndarray], None] | None = None
        self.on_playback_finished: Callable[[], None] | None = None
        self.on_playback_sample: Callable[[np.ndarray], None] | None = None

        self._playback_thread: threading.Thread | None = None

    def start(self) -> None:
        try:
            self._stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                blocksize=BLOCK_SIZE,
                dtype=np.float32,
                callback=self._audio_cb,
            )
            self._stream.start()
            log.info("Microphone stream started")
        except Exception as e:
            log.error("Failed to start mic stream: %s", e)

    def stop(self) -> None:
        if self._stream:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
        sd.stop()

    def toggle_mute(self) -> bool:
        self.muted = not self.muted
        return self.muted

    def play_audio(self, data: np.ndarray, sr: int) -> None:
        def _worker():
            sd.play(data, sr)
            idx = 0
            step = int(sr / 60)
            while idx < len(data):
                chunk = data[idx: idx + step]
                if self.on_playback_sample and len(chunk) > 0:
                    self.on_playback_sample(chunk)
                idx += step
                time.sleep(1 / 60)
            sd.wait()
            if self.on_playback_finished:
                self.on_playback_finished()

        self._playback_thread = threading.Thread(target=_worker, daemon=True)
        self._playback_thread.start()

    # ── internal ──
    def _audio_cb(self, indata: np.ndarray, frames: int, _time, status) -> None:
        if status:
            log.warning("Audio status: %s", status)
        channel = indata[:, 0]

        if self.on_waveform_sample:
            self.on_waveform_sample(channel)

        if self.muted:
            return

        level = rms(channel)

        if level > self.config.vad_threshold:
            self._speech_frames += 1
            self._silence_frames = 0
            if self._speech_frames >= 3 and not self._is_recording:
                self._is_recording = True
                self._rec_buf = [channel.copy()]
                self._rec_start_time = time.time()
                self._on_vad(True)
            elif self._is_recording:
                self._rec_buf.append(channel.copy())
                if time.time() - self._rec_start_time > MAX_RECORDING_TIME:
                    self._finalize_utterance()
        else:
            self._speech_frames = 0
            if self._is_recording:
                self._silence_frames += 1
                timeout_frames = int(self.config.vad_silence_timeout * SAMPLE_RATE / BLOCK_SIZE)
                if self._silence_frames >= timeout_frames:
                    self._finalize_utterance()
            else:
                self._silence_frames = 0

    def _finalize_utterance(self) -> None:
        self._is_recording = False
        if self._rec_buf and self.on_utterance:
            audio = np.concatenate(self._rec_buf)
            self._rec_buf.clear()
            self._on_vad(False)
            self.on_utterance(audio)
        else:
            self._rec_buf.clear()
            self._on_vad(False)

    def _on_vad(self, speaking: bool) -> None:
        if self.on_vad_change:
            self.on_vad_change(speaking)


# ── STTEngine ───────────────────────────────────────────────────────────────
class STTEngine:
    """Local speech-to-text via faster-whisper."""

    def __init__(self, config: AppConfig):
        self.config = config
        self._model: faster_whisper.WhisperModel | None = None
        self._lock = threading.Lock()

    def load_model(self, progress_cb: Callable[[str], None] | None = None) -> None:
        if self._model is not None:
            return
        device = self.config.whisper_device
        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
        compute = self.config.whisper_compute
        if compute == "auto":
            compute = "float16" if device == "cuda" else "int8"

        if progress_cb:
            progress_cb(f"Loading whisper model ({self.config.whisper_model}) on {device}...")
        log.info("Loading whisper model %s on %s (compute=%s)", self.config.whisper_model, device, compute)
        self._model = faster_whisper.WhisperModel(
            self.config.whisper_model,
            device=device,
            compute_type=compute,
            download_root=os.environ.get("WHISPER_CACHE_DIR", None),
        )
        if progress_cb:
            progress_cb("Whisper model loaded.")

    def transcribe(self, audio: np.ndarray, progress_cb: Callable[[str], None] | None = None) -> str:
        with self._lock:
            if self._model is None:
                self.load_model(progress_cb)
            audio_f32 = audio.astype(np.float32)
            if progress_cb:
                progress_cb("Transcribing...")
            segments, info = self._model.transcribe(
                audio_f32,
                beam_size=5,
                vad_filter=True,
            )
            text = " ".join(seg.text for seg in segments)
            lang = info.language if info else "unknown"
            log.info("STT detected language=%s, text='%s'", lang, text[:80])
            return text.strip()


# ── TTSEngine ────────────────────────────────────────────────────────────────
class TTSEngine:
    """Text-to-speech via edge-tts (async)."""

    def __init__(self, loop: asyncio.AbstractEventLoop | None = None):
        self._loop = loop

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def speak_async(self, text: str, voice: str | None = None) -> bytes:
        import edge_tts
        lang = detect_language(text)
        selected = voice or TTS_VOICES.get(lang, TTS_VOICES["en"])

        communicate = edge_tts.Communicate(text, selected)
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)

    def synthesize(self, text: str, voice: str | None = None) -> bytes:
        """Synchronous wrapper. Call from any thread; assumes self._loop is running."""
        if self._loop is None:
            raise RuntimeError("TTSEngine has no asyncio loop set")
        future = asyncio.run_coroutine_threadsafe(self.speak_async(text, voice), self._loop)
        return future.result()

    def decode_to_audio(self, mp3_bytes: bytes) -> tuple[np.ndarray, int]:
        """Decode MP3 bytes to numpy array using PyAV."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(mp3_bytes)
            tmp_path = tmp.name
        try:
            with av.open(tmp_path) as container:
                stream = container.streams.audio[0]
                frames = []
                for frame in container.decode(stream):
                    arr = frame.to_ndarray()
                    if arr.shape[0] == 1:
                        arr = arr[0]
                    else:
                        arr = np.mean(arr, axis=0)
                    frames.append(arr.astype(np.float32) / 32768.0)
                audio = np.concatenate(frames) if frames else np.array([], dtype=np.float32)
                return audio, stream.sample_rate
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


# ── N8NClient ────────────────────────────────────────────────────────────────
class N8NClient:
    """Async HTTP client for communicating with n8n."""

    def __init__(self, config: AppConfig, loop: asyncio.AbstractEventLoop | None = None):
        self.config = config
        self._loop = loop
        self._session: aiohttp.ClientSession | None = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def send_async(self, text: str, source: str = "desktop") -> str | None:
        session = await self._get_session()
        payload = {"source": source, "message": text}
        log.info("-> n8n POST %s", payload)
        try:
            async with session.post(
                self.config.n8n_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status != 200:
                    log.error("n8n returned HTTP %d", resp.status)
                    text_resp = await resp.text()
                    log.error("n8n body: %s", text_resp[:500])
                    return None
                data = await resp.json()
                reply = data.get("reply", "")
                log.info("<- n8n reply: %s", reply[:100])
                return reply
        except asyncio.TimeoutError:
            log.error("n8n request timed out")
            return None
        except aiohttp.ClientConnectorError as e:
            log.error("Cannot connect to n8n at %s: %s", self.config.n8n_url, e)
            return None
        except Exception as e:
            log.error("n8n request failed: %s", e)
            return None

    def send(self, text: str, source: str = "desktop") -> str | None:
        if self._loop is None:
            raise RuntimeError("N8NClient has no asyncio loop set")
        future = asyncio.run_coroutine_threadsafe(self.send_async(text, source), self._loop)
        try:
            return future.result(timeout=60)
        except Exception as e:
            log.error("n8n send error: %s", e)
            return None

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()


# ── GeminiBrain (Direct Fallback) ────────────────────────────────────────────
class GeminiBrain:
    """Direct Google Gemini API client used when n8n is offline."""

    SYSTEM_PROMPT = (
        "You are JARVIS, an omnipotent digital butler and AI assistant. "
        "You are loyal, capable, professional, and efficient. "
        "Respond in the SAME LANGUAGE the user speaks to you — Arabic or English. "
        "Be concise, accurate, and helpful. Do not mention that you are a fallback "
        "or that n8n is offline — just serve as JARVIS normally."
    )

    def __init__(self, api_key: str):
        if not api_key:
            log.warning("GeminiBrain: no API key provided — fallback disabled")
            self._available = False
            return
        self._available = True
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=self.SYSTEM_PROMPT,
        )
        self._history: list = []
        log.info("GeminiBrain fallback initialized")

    @property
    def available(self) -> bool:
        return self._available

    def chat(self, message: str) -> str:
        if not self._available:
            return "JARVIS neural core is not configured. Please set GEMINI_API_KEY."
        try:
            chat = self._model.start_chat(history=self._history)
            response = chat.send_message(message)
            self._history = chat.history[-40:]  # keep last 20 turns
            return response.text
        except Exception as e:
            log.error("Gemini chat error: %s", e)
            return f"I encountered an error processing your request: {e}"


# ── Main Application ────────────────────────────────────────────────────────
class JARVISApp(ctk.CTk):
    TITLE = APP_NAME
    WIN_W, WIN_H = 1100, 780

    def __init__(self):
        super().__init__()

        self.config = AppConfig()
        self._state = State.IDLE
        self._async_loop: asyncio.AbstractEventLoop | None = None
        self._async_thread: threading.Thread | None = None
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="stt")
        self._log_queue: queue.Queue[str] = queue.Queue()
        self._n8n_status = "OFFLINE"
        self._closing = False

        # --- window ---
        self.title(self.TITLE)
        self.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.minsize(800, 600)
        self.configure(fg_color=COLOR_BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # --- components ---
        self.waveform = AudioWaveformWidget(self)
        self.audio = AudioManager(self.config)
        self.stt = STTEngine(self.config)
        self.tts = TTSEngine()
        self.n8n = N8NClient(self.config)
        self.gemini = GeminiBrain(GEMINI_API_KEY)

        # --- build UI ---
        self._build_ui()
        self._connect_audio()
        self._start_async_thread()
        self._poll_log_queue()

        # start audio
        self.audio.start()

        # check n8n connectivity in background
        self.after(1500, self._check_n8n)

        log.info("JARVIS application started")

    # ── UI Construction ──
    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── top bar ──
        top = ctk.CTkFrame(self, fg_color=COLOR_BG, height=44)
        top.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 0))
        top.grid_propagate(False)
        top.grid_columnconfigure(0, weight=0)

        ctk.CTkLabel(
            top, text="JARVIS", font=ctk.CTkFont("Segoe UI", 18, "bold"),
            text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, padx=(12, 20))

        self._badges_frame = ctk.CTkFrame(top, fg_color="transparent")
        self._badges_frame.grid(row=0, column=1, sticky="w")
        self.badge_svr = self._badge("SVR", "LOCAL", COLOR_SUCCESS)
        self.badge_svr.pack(side="left", padx=4)
        self.badge_brain = self._badge("BRAIN", "GEMINI", COLOR_ACCENT)
        self.badge_brain.pack(side="left", padx=4)
        self.badge_n8n = self._badge("N8N", "CHECKING...", COLOR_WARNING)
        self.badge_n8n.pack(side="left", padx=4)

        # ── waveform ──
        self.waveform.grid(row=1, column=0, sticky="nsew", padx=6, pady=(4, 0))

        # ── status & controls ──
        ctrl = ctk.CTkFrame(self, fg_color=COLOR_BG, height=40)
        ctrl.grid(row=2, column=0, sticky="ew", padx=6, pady=(4, 0))
        ctrl.grid_propagate(False)
        ctrl.grid_columnconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(
            ctrl, text="◆ IDLE", font=ctk.CTkFont("Consolas", 13),
            text_color=COLOR_TEXT_DIM,
        )
        self.status_label.grid(row=0, column=0, padx=(12, 8))

        self.mute_btn = ctk.CTkButton(
            ctrl, text="MUTE", width=70, height=26,
            fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT,
            hover_color="#1a1a3a",
            font=ctk.CTkFont("Consolas", 11),
            command=self._toggle_mute,
        )
        self.mute_btn.grid(row=0, column=2, padx=4)

        self.settings_btn = ctk.CTkButton(
            ctrl, text="⚙", width=36, height=26,
            fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT_DIM,
            hover_color="#1a1a3a",
            font=ctk.CTkFont("Consolas", 14),
            command=self._show_settings,
        )
        self.settings_btn.grid(row=0, column=3, padx=(4, 12))

        # ── log area ──
        log_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=6, pady=(4, 6))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont("Consolas", 12),
            fg_color=COLOR_BG_DARK,
            text_color=COLOR_TEXT,
            wrap="word",
            state="disabled",
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.bind("<Key>", lambda e: "break")
        self.log_text.tag_config("user", foreground=COLOR_WARNING)
        self.log_text.tag_config("jarvis", foreground=COLOR_ACCENT)
        self.log_text.tag_config("error", foreground=COLOR_ERROR)
        self.log_text.tag_config("info", foreground=COLOR_TEXT_DIM)

    def _badge(self, prefix: str, label: str, color: str) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            self._badges_frame,
            text=f"[{prefix}: {label}]",
            font=ctk.CTkFont("Consolas", 11, "bold"),
            text_color=color,
            fg_color=COLOR_BG_LIGHT,
            corner_radius=4,
            padx=8,
            pady=2,
        )

    # ── Audio connections ──
    def _connect_audio(self) -> None:
        self.audio.on_waveform_sample = self.waveform.feed_samples
        self.audio.on_playback_sample = self.waveform.feed_playback

        def _on_vad(speaking: bool):
            if speaking and self._state == State.IDLE:
                self._set_state(State.LISTENING)
            elif not speaking and self._state == State.LISTENING:
                pass  # handled by on_utterance

        self.audio.on_vad_change = _on_vad

        def _on_utterance(audio: np.ndarray):
            self._set_state(State.PROCESSING)
            self._executor.submit(self._handle_utterance, audio)

        self.audio.on_utterance = _on_utterance

        def _on_playback_done():
            if self._state == State.SPEAKING:
                self._set_state(State.IDLE)

        self.audio.on_playback_finished = _on_playback_done

    # ── State machine ──
    def _set_state(self, s: State) -> None:
        if self._closing:
            return
        self._state = s
        self.waveform.set_state(s)
        icons = {
            State.IDLE: "◆",
            State.LISTENING: "◉",
            State.PROCESSING: "◌",
            State.THINKING: "⟳",
            State.SPEAKING: "▶",
        }
        colors = {
            State.IDLE: COLOR_TEXT_DIM,
            State.LISTENING: COLOR_WARNING,
            State.PROCESSING: COLOR_ACCENT,
            State.THINKING: COLOR_ACCENT_GLOW,
            State.SPEAKING: COLOR_SUCCESS,
        }
        icon = icons.get(s, "◆")
        color = colors.get(s, COLOR_TEXT_DIM)
        self.after(0, lambda: self._update_status_label(icon, s, color))

    def _update_status_label(self, icon: str, s: State, color: str) -> None:
        try:
            self.status_label.configure(text=f"{icon} {s.value}", text_color=color)
        except Exception:
            pass

    # ── Async thread ──
    def _start_async_thread(self) -> None:
        self._async_loop = asyncio.new_event_loop()
        self.tts.set_loop(self._async_loop)
        self.n8n.set_loop(self._async_loop)

        def _run_loop():
            asyncio.set_event_loop(self._async_loop)
            self._async_loop.run_forever()

        self._async_thread = threading.Thread(target=_run_loop, daemon=True, name="async")
        self._async_thread.start()

    # ── Utterance pipeline ──
    def _handle_utterance(self, audio: np.ndarray) -> None:
        try:
            # STT
            self._gui_log("[AUDIO] Processing speech...")
            text = self.stt.transcribe(audio, progress_cb=lambda m: self._gui_log(f"[STT] {m}"))
            if not text:
                self._gui_log("[STT] No speech detected.")
                self._set_state(State.IDLE)
                return

            self._gui_log(f"[USER] {text}")

            # n8n → fallback → Gemini direct
            self._set_state(State.THINKING)
            reply = None
            if self._n8n_status != "OFFLINE":
                self._gui_log("[N8N] Sending to JARVIS brain...")
                reply = self.n8n.send(text)
            if not reply and self.gemini.available:
                self._gui_log("[BRAIN] Using direct Gemini connection...")
                reply = self.gemini.chat(text)
            if not reply:
                reply = "I apologize, but I'm having trouble connecting to my neural core."
                self._gui_log(f"[JARVIS] {reply}")
            else:
                self._gui_log(f"[JARVIS] {reply}")

            # TTS
            self._set_state(State.SPEAKING)
            self._gui_log("[TTS] Synthesizing speech...")
            mp3 = self.tts.synthesize(reply)
            audio_data, sr = self.tts.decode_to_audio(mp3)
            if len(audio_data) > 0:
                self.audio.play_audio(audio_data, sr)
            else:
                self._set_state(State.IDLE)

        except Exception as e:
            log.exception("Utterance pipeline error")
            self._gui_log(f"[ERROR] {e}")
            self._set_state(State.IDLE)

    # ── Log ──
    def _gui_log(self, msg: str) -> None:
        self._log_queue.put(msg)

    def _poll_log_queue(self) -> None:
        while not self._log_queue.empty():
            msg = self._log_queue.get_nowait()
            self._append_log(msg)
        if not self._closing:
            self.after(100, self._poll_log_queue)

    def _append_log(self, msg: str) -> None:
        try:
            self.log_text.configure(state="normal")
            if msg.startswith("[USER]"):
                self.log_text.insert("end", msg + "\n", "user")
            elif msg.startswith("[JARVIS]"):
                self.log_text.insert("end", msg + "\n", "jarvis")
            elif msg.startswith("[ERROR]"):
                self.log_text.insert("end", msg + "\n", "error")
            else:
                self.log_text.insert("end", msg + "\n", "info")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    # ── n8n health check ──
    def _check_n8n(self) -> None:
        async def _check():
            try:
                async with aiohttp.ClientSession() as sess:
                    url = self.config.n8n_url.replace("/webhook/jarvis", "/healthz")
                    async with sess.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                        return resp.status == 200
            except Exception:
                # try the webhook endpoint with a GET to see if n8n is alive
                try:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(
                            self.config.n8n_url,
                            timeout=aiohttp.ClientTimeout(total=3),
                        ) as resp:
                            return resp.status in (200, 404, 405)
                except Exception:
                    return False

        async def _update():
            ok = await _check()
            status = "CONNECTED" if ok else "OFFLINE"
            color = COLOR_SUCCESS if ok else COLOR_ERROR
            self._n8n_status = status
            self.after(0, lambda: self.badge_n8n.configure(
                text=f"[N8N: {status}]", text_color=color,
            ))

        if self._async_loop and not self._closing:
            asyncio.run_coroutine_threadsafe(_update(), self._async_loop)

        # recheck every 30s
        self.after(30000, self._check_n8n)

    # ── Controls ──
    def _toggle_mute(self) -> None:
        muted = self.audio.toggle_mute()
        self.mute_btn.configure(text="UNMUTE" if muted else "MUTE")
        self._gui_log(f"[SYS] Microphone {'muted' if muted else 'unmuted'}")

    def _show_settings(self) -> None:
        from tkinter import messagebox
        messagebox.showinfo(
            "JARVIS Settings",
            f"n8n URL: {self.config.n8n_url}\n"
            f"Whisper Model: {self.config.whisper_model}\n"
            f"VAD Threshold: {self.config.vad_threshold}\n\n"
            "Set environment variables to configure:\n"
            "  N8N_WEBHOOK_URL, WHISPER_MODEL, VAD_THRESHOLD",
        )

    # ── Shutdown ──
    def _on_close(self) -> None:
        self._closing = True
        log.info("Shutting down JARVIS...")
        self.audio.stop()
        self._executor.shutdown(wait=False)
        if self._async_loop is not None:
            try:
                self._async_loop.call_soon_threadsafe(self._async_loop.stop)
            except Exception:
                pass
        if self._async_thread is not None and self._async_thread.is_alive():
            self._async_thread.join(timeout=3)
        self.destroy()

    def run(self) -> None:
        try:
            self.mainloop()
        except KeyboardInterrupt:
            self._on_close()


# ── Entry Point ──────────────────────────────────────────────────────────────
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = JARVISApp()
    app.run()


if __name__ == "__main__":
    main()
