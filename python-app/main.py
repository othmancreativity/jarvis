#!/usr/bin/env python3
"""
JARVIS 4.5 — Desktop Companion App
====================================
Integrated desktop application with:
    - Central orchestrator (JarvisCore)
    - Real-time agent runtime monitoring
    - Multilingual support (EN + AR with RTL)
    - Safety confirmation dialogs
    - WebSocket bridge for n8n integration
    - LLM integration via Groq API
    - Emergency stop
    - System tray integration
    - Graceful shutdown on SIGTERM/SIGINT
"""

from __future__ import annotations

import sys
import os
import asyncio
import json
import logging
import signal
import time
import traceback
from pathlib import Path
from datetime import datetime

# ── Logging Setup (must be first) ──────────────────────────────────────

from config import config

LOG_DIR = config.log_dir
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("jarvis.app")

# ── PyQt6 Imports ───────────────────────────────────────────────────────

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
    QSystemTrayIcon, QMenu, QMessageBox, QDialog,
    QDialogButtonBox, QCheckBox, QFrame, QProgressBar,
    QTabWidget, QStatusBar, QToolBar, QFileDialog,
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QLocale, QTranslator,
    QLibraryInfo, QPoint, QSize,
)
from PyQt6.QtGui import QAction, QFont, QIcon, QPalette, QColor, QKeySequence, QShortcut

# ── i18n ─────────────────────────────────────────────────────────────────

DEFAULT_LANG = "en"
CURRENT_LANG = config.language

def load_translations(lang: str = CURRENT_LANG) -> dict:
    """Load translation strings."""
    locales_dir = Path(__file__).parent / "locales"
    file_path = locales_dir / f"{lang}.json"
    if not file_path.exists():
        file_path = locales_dir / f"{DEFAULT_LANG}.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

_translations = load_translations(CURRENT_LANG)

def _(key: str, fallback: str = "") -> str:
    """Get translated string."""
    return _translations.get(key, fallback or key)

# ── Safety Dialog ────────────────────────────────────────────────────────

class SafetyDialog(QDialog):
    """Modal dialog for confirming risky operations."""

    confirmed = pyqtSignal(dict)

    def __init__(self, action: str, target: str, risk: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_("safety_dialog_title", "Action Requires Confirmation"))
        self.setMinimumWidth(500)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background: #0f172a; color: #e2e8f0; }
            QLabel { color: #e2e8f0; }
            QPushButton { background: #334155; color: #f1f5f9; border: none; border-radius: 6px; padding: 8px 16px; }
            QPushButton:hover { background: #475569; }
            QCheckBox { color: #94a3b8; }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        header = QLabel(f'<h2 style="color: #f59e0b; margin: 0;">⚠️  {_("action_requires_confirmation", "Action Requires Confirmation")}</h2>')
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        details = QFrame()
        details.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 12px;")
        dlayout = QVBoxLayout(details)
        dlayout.setSpacing(8)
        dlayout.addWidget(QLabel(f'<b>{_("action", "Action")}:</b> <span style="color: #e2e8f0;">{action}</span>'))
        dlayout.addWidget(QLabel(f'<b>{_("target", "Target")}:</b> <span style="color: #38bdf8;">{target}</span>'))
        dlayout.addWidget(QLabel(f'<b>{_("risk", "Risk")}:</b> <span style="color: #ef4444;">{risk}</span>'))
        dlayout.addWidget(QLabel(f'<small style="color: #94a3b8;">{_("requested_by", "Requested by")}: JARVIS 4.5 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</small>'))
        layout.addWidget(details)

        self.remember_cb = QCheckBox(_("remember_choice_5min", "Remember my choice for 5 minutes"))
        layout.addWidget(self.remember_cb)

        btn_layout = QHBoxLayout()
        self.deny_btn = QPushButton(f"❌  {_("deny", "Deny")}")
        self.deny_btn.setStyleSheet("background: #ef4444; color: white;")
        self.deny_btn.clicked.connect(self._on_deny)
        self.allow_btn = QPushButton(f"✅  {_("allow", "Allow")}")
        self.allow_btn.setStyleSheet("background: #22c55e; color: white;")
        self.allow_btn.clicked.connect(self._on_allow)
        btn_layout.addWidget(self.deny_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.allow_btn)
        layout.addLayout(btn_layout)

        self.timeout_label = QLabel(f"⏱️  {_("auto_deny_in", "Auto-deny in")} 60s")
        self.timeout_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeout_label.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.timeout_label)

        self.remaining = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _tick(self):
        self.remaining -= 1
        self.timeout_label.setText(f'⏱️  {_("auto_deny_in", "Auto-deny in")} {self.remaining}s')
        if self.remaining <= 0:
            self._on_deny()

    def _on_allow(self):
        self.timer.stop()
        self.confirmed.emit({"confirmed": True, "remember": self.remember_cb.isChecked()})
        self.accept()

    def _on_deny(self):
        self.timer.stop()
        self.confirmed.emit({"confirmed": False, "remember": self.remember_cb.isChecked()})
        self.reject()


# ── Audio Visualization ──────────────────────────────────────────────────

class AudioVizWidget(QFrame):
    """Simulated audio frequency visualization."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.setMaximumHeight(140)
        self.setStyleSheet("background: #0f172a; border-radius: 8px;")
        self._bars = [0.0] * 32
        self._active = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_bars)
        self._timer.start(50)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        self.label = QLabel(f'🎤  {_("audio_visualization", "Audio Visualization")}')
        self.label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(self.label)

    def _update_bars(self):
        import random
        import math
        if self._active:
            self._bars = [
                max(0.05, min(1.0, abs(math.sin(i * 0.3 + time.time() * 3) * random.uniform(0.5, 1.0))))
                for i in range(32)
            ]
        else:
            self._bars = [max(0.02, v * 0.95) for v in self._bars]
        self.update()

    def set_active(self, active: bool):
        self._active = active

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width() - 16
        height = self.height() - 30
        bar_width = width / 32
        gradient = QLinearGradient(0, height, 0, 0)
        gradient.setColorAt(0.0, QColor("#3b82f6"))
        gradient.setColorAt(0.5, QColor("#8b5cf6"))
        gradient.setColorAt(1.0, QColor("#ec4899"))
        for i, val in enumerate(self._bars):
            bar_h = val * height
            x = 8 + i * bar_width
            y = 20 + height - bar_h
            painter.fillRect(int(x), int(y), int(bar_width - 1), int(bar_h), gradient)
        painter.end()


# ── Status Panel ─────────────────────────────────────────────────────────

class StatusPanel(QFrame):
    """Bottom status panel with system info."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._refresh)
        self._update_timer.start(5000)

    def _setup_ui(self):
        self.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 4px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        self.model_label = QLabel(f'🤖  <b>Model:</b> {config.model}')
        self.model_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.model_label)

        self.bridge_label = QLabel(f'🔗  <b>Bridge:</b> <span style="color: #ef4444;">●</span> Disconnected')
        self.bridge_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.bridge_label)

        self.agent_label = QLabel(f'🎯  <b>Agents:</b> 9 active')
        self.agent_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.agent_label)

        self.runtime_label = QLabel(f'⏱️  <b>Runtime:</b> idle')
        self.runtime_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.runtime_label)

        self.memory_label = QLabel(f'💾  <b>Memory:</b> —')
        self.memory_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.memory_label)

    def set_bridge_connected(self, connected: bool):
        color = "#22c55e" if connected else "#ef4444"
        status = "Connected" if connected else "Disconnected"
        self.bridge_label.setText(f'🔗  <b>Bridge:</b> <span style="color: {color};">●</span> {status}')

    def set_runtime_state(self, state: str):
        self.runtime_label.setText(f'⏱️  <b>Runtime:</b> {state}')

    def set_memory_usage(self, usage: str):
        self.memory_label.setText(f'💾  <b>Memory:</b> {usage}')

    def _refresh(self):
        try:
            import psutil
            mem = psutil.virtual_memory()
            self.memory_label.setText(f'💾  <b>Memory:</b> {mem.percent}% used')
        except ImportError:
            pass


# ── Chat Panel ───────────────────────────────────────────────────────────

class ChatPanel(QFrame):
    """Chat interface with message history."""

    message_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setStyleSheet("""
            QTextEdit {
                background: #1e293b;
                color: #e2e8f0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.history)

        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(_("type_message", "Type a message..."))
        self.input_field.returnPressed.connect(self._send)
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 6px;
                background: #334155;
                color: #f1f5f9;
                border: 1px solid #475569;
                font-size: 13px;
            }
        """)
        input_row.addWidget(self.input_field, 1)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedWidth(40)
        self.send_btn.setStyleSheet("background: #3b82f6; color: white; font-weight: bold;")
        self.send_btn.clicked.connect(self._send)
        input_row.addWidget(self.send_btn)

        self.attach_btn = QPushButton("📎")
        self.attach_btn.setFixedWidth(40)
        self.attach_btn.setToolTip("Attach file")
        self.attach_btn.clicked.connect(self._attach_file)
        input_row.addWidget(self.attach_btn)

        layout.addLayout(input_row)

    def _send(self):
        text = self.input_field.text().strip()
        if text:
            self.add_message("user", text)
            self.message_sent.emit(text)
            self.input_field.clear()

    def _attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Attach File")
        if file_path:
            self.add_message("system", f"📎 Attached: {file_path}")

    def add_message(self, role: str, text: str):
        colors = {
            "user": "#3b82f6",
            "assistant": "#22c55e",
            "system": "#f59e0b",
            "error": "#ef4444",
        }
        labels = {"user": "You", "assistant": "JARVIS", "system": "System", "error": "Error"}
        color = colors.get(role, "#94a3b8")
        label = labels.get(role, "Unknown")
        timestamp = datetime.now().strftime("%H:%M")

        html = f'<p><span style="color: {color};"><b>{label}</b></span> <span style="color: #64748b; font-size: 10px;">{timestamp}</span><br>{text}</p>'
        self.history.append(html)

    def clear_history(self):
        self.history.clear()


# ── Core Thread ──────────────────────────────────────────────────────────

class CoreThread(QThread):
    """Runs the JarvisCore orchestrator in a background thread."""

    response_ready = pyqtSignal(str)
    status_update = pyqtSignal(str, dict)
    initialized = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.core = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._running = True

    def run(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._main())
        except Exception as e:
            logger.error(f"Core thread error: {e}")
            self.error_occurred.emit(str(e))

    async def _main(self):
        try:
            from core.jarvis_core import JarvisCore
            self.core = JarvisCore()

            # Wire callbacks
            self.core.on_response(self._on_response)
            self.core.on_status_update(self._on_status)

            # Initialize
            await self.core.initialize()
            self.initialized.emit()

            # Run
            await self.core.run()
        except Exception as e:
            logger.error(f"Core init error: {e}\n{traceback.format_exc()}")
            self.error_occurred.emit(f"Core initialization failed: {e}")

    def _on_response(self, text: str):
        self.response_ready.emit(text)

    def _on_status(self, status: str, data: dict):
        self.status_update.emit(status, data)

    def process_message(self, text: str):
        """Send a message to the core for processing."""
        if self.core and self._loop:
            asyncio.run_coroutine_threadsafe(
                self.core.process_input(text),
                self._loop,
            )

    def emergency_stop(self):
        if self.core:
            self.core.emergency_stop()

    def get_status(self) -> dict:
        if self.core:
            return self.core.get_status()
        return {}

    def stop(self):
        self._running = False
        if self.core and self._loop:
            asyncio.run_coroutine_threadsafe(self.core.stop(), self._loop)
        self.quit()
        self.wait(5000)


# ── Bridge Thread ────────────────────────────────────────────────────────

class BridgeThread(QThread):
    """Runs the WebSocket bridge server with auto-reconnect."""

    message_received = pyqtSignal(dict)
    client_connected = pyqtSignal()
    client_disconnected = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, port: int = None, secret: str = None):
        super().__init__()
        self.port = port or config.bridge_port
        self.secret = secret or config.bridge_secret
        self._running = True
        self._retry_count = 0
        self._max_retries = 5

    def run(self):
        while self._running and self._retry_count < self._max_retries:
            try:
                import websockets
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                from bridge_server import BridgeServer

                async def start():
                    server = BridgeServer()
                    await server.start()

                logger.info(f"Bridge server starting on port {self.port}")
                loop.run_until_complete(start())
                self._retry_count = 0  # Reset on success
            except ImportError as e:
                self.error_occurred.emit(f"websockets not installed: {e}")
                break
            except Exception as e:
                self._retry_count += 1
                logger.error(f"Bridge error (attempt {self._retry_count}): {e}")
                self.error_occurred.emit(str(e))
                time.sleep(min(2 ** self._retry_count, 30))  # Exponential backoff

    def stop(self):
        self._running = False
        self.quit()
        self.wait(3000)


# ── Main Window ──────────────────────────────────────────────────────────

class JarvisMainWindow(QMainWindow):
    """Main application window for JARVIS 4.5."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("app_title", "JARVIS 4.5 — AI Operating Assistant"))
        self.setMinimumSize(1000, 750)
        self._setup_ui()
        self._setup_tray()
        self._setup_shortcuts()
        self._apply_theme()
        self._start_core()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Toolbar
        toolbar = QHBoxLayout()
        self.lang_btn = QPushButton("🌐 EN / AR")
        self.lang_btn.setToolTip("Switch language")
        self.lang_btn.setFixedWidth(100)
        self.lang_btn.clicked.connect(self._toggle_language)
        toolbar.addWidget(self.lang_btn)

        self.emergency_btn = QPushButton("🛑 STOP")
        self.emergency_btn.setStyleSheet("background: #ef4444; color: white; font-weight: bold;")
        self.emergency_btn.setToolTip("Emergency Stop")
        self.emergency_btn.clicked.connect(self._emergency_stop)
        toolbar.addWidget(self.emergency_btn)

        self.clear_btn = QPushButton("🗑️")
        self.clear_btn.setToolTip("Clear chat")
        self.clear_btn.clicked.connect(self._clear_chat)
        toolbar.addWidget(self.clear_btn)

        toolbar.addStretch()

        version_label = QLabel("v4.5.0")
        version_label.setStyleSheet("color: #64748b; font-size: 11px;")
        toolbar.addWidget(version_label)
        layout.addLayout(toolbar)

        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Chat panel
        self.chat_panel = ChatPanel()
        self.chat_panel.message_sent.connect(self._process_message)
        splitter.addWidget(self.chat_panel)

        # Right: Info panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        self.audio_viz = AudioVizWidget()
        right_layout.addWidget(self.audio_viz)

        self.status_panel = StatusPanel()
        right_layout.addWidget(self.status_panel)

        actions_frame = QFrame()
        actions_frame.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 8px;")
        actions_layout = QVBoxLayout(actions_frame)
        actions_label = QLabel(f"<b>{_("quick_actions", "Quick Actions")}</b>")
        actions_label.setStyleSheet("color: #e2e8f0;")
        actions_layout.addWidget(actions_label)

        quick_actions = [
            ("📸 Screenshot", lambda: self._quick_action("screenshot")),
            ("🔍 OCR", lambda: self._quick_action("ocr")),
            ("🌐 Browser", lambda: self._quick_action("browser")),
            ("📊 System Info", lambda: self._quick_action("system_info")),
            ("📝 New Note", lambda: self._quick_action("new_note")),
        ]
        for label, handler in quick_actions:
            btn = QPushButton(label)
            btn.setStyleSheet("text-align: left; padding: 6px; background: #334155;")
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)

        right_layout.addWidget(actions_frame)
        right_layout.addStretch()
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])
        layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("JARVIS 4.5 Initializing...")
        self.setStatusBar(self.status_bar)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        self.tray.setToolTip("JARVIS 4.5")

        tray_menu = QMenu()
        show_action = QAction(_("show", "Show"), self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction(_("quit", "Quit"), self)
        quit_action.triggered.connect(self._quit)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+L"), self, self._clear_chat)
        QShortcut(QKeySequence("Ctrl+Return"), self, lambda: self.chat_panel._send())
        QShortcut(QKeySequence("Ctrl+Q"), self, self._quit)

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #0f172a; }
            QWidget { font-family: 'Segoe UI', 'Helvetica', sans-serif; }
            QPushButton {
                background: #334155; color: #f1f5f9; border: none;
                border-radius: 6px; padding: 6px 12px;
            }
            QPushButton:hover { background: #475569; }
            QTextEdit { border: 1px solid #334155; }
            QLineEdit { border: 1px solid #334155; }
            QLabel { color: #e2e8f0; }
            QStatusBar { background: #1e293b; color: #94a3b8; }
            QSplitter::handle { background: #334155; }
        """)

    def _start_core(self):
        """Start the core orchestrator."""
        self.core_thread = CoreThread()
        self.core_thread.response_ready.connect(self._handle_response)
        self.core_thread.status_update.connect(self._handle_status)
        self.core_thread.initialized.connect(self._on_core_ready)
        self.core_thread.error_occurred.connect(self._handle_error)
        self.core_thread.start()

        # Start bridge server
        self.bridge_thread = BridgeThread()
        self.bridge_thread.client_connected.connect(
            lambda: self.status_panel.set_bridge_connected(True)
        )
        self.bridge_thread.client_disconnected.connect(
            lambda: self.status_panel.set_bridge_connected(False)
        )
        self.bridge_thread.start()

    def _on_core_ready(self):
        self.status_bar.showMessage("JARVIS 4.5 Ready")
        self.chat_panel.add_message("system", "JARVIS 4.5 is ready. How can I help you?")

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def _toggle_language(self):
        global CURRENT_LANG, _translations
        CURRENT_LANG = "ar" if CURRENT_LANG == "en" else "en"
        _translations = load_translations(CURRENT_LANG)
        if CURRENT_LANG == "ar":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.Orientation.LeftToRight)
        self.chat_panel.input_field.setPlaceholderText(_("type_message", "Type a message..."))
        QMessageBox.information(self, _("language_changed", "Language Changed"), f"Language: {CURRENT_LANG.upper()}")

    def _emergency_stop(self):
        self.core_thread.emergency_stop()
        self.chat_panel.add_message("system", _('emergency_stop_activated', "🛑 EMERGENCY STOP ACTIVATED"))
        self.status_panel.set_runtime_state("emergency_stop")
        logger.critical("Emergency stop activated from UI")

    def _clear_chat(self):
        self.chat_panel.clear_history()
        self.chat_panel.add_message("system", _('chat_cleared', "Chat history cleared"))

    def _quit(self):
        self.tray.hide()
        if hasattr(self, 'core_thread'):
            self.core_thread.stop()
        if hasattr(self, 'bridge_thread'):
            self.bridge_thread.stop()
        QApplication.quit()

    def _process_message(self, text: str):
        """Process user message through the core orchestrator."""
        self.audio_viz.set_active(True)
        self.status_panel.set_runtime_state("processing")
        self.core_thread.process_message(text)

    def _handle_response(self, text: str):
        self.chat_panel.add_message("assistant", text)
        self.audio_viz.set_active(False)
        self.status_panel.set_runtime_state("idle")

    def _handle_status(self, status: str, data: dict):
        if status == "state_change":
            self.status_panel.set_runtime_state(data.get("to", "unknown"))
        elif status == "emergency_stop":
            self.status_panel.set_runtime_state("emergency_stop")

    def _handle_error(self, error: str):
        self.chat_panel.add_message("error", f"Error: {error}")
        self.audio_viz.set_active(False)
        self.status_panel.set_runtime_state("error")

    def _quick_action(self, action: str):
        actions = {
            "screenshot": "Take a screenshot and describe what you see.",
            "ocr": "Perform OCR on the screen and extract all visible text.",
            "browser": "Open the browser and wait for instructions.",
            "system_info": "Get system information and show a summary.",
            "new_note": "Create a new text note file.",
        }
        prompt = actions.get(action, action)
        self.chat_panel.input_field.setText(prompt)
        self.chat_panel.input_field.setFocus()

    def show_safety_dialog(self, action: str, target: str, risk: str) -> dict:
        dialog = SafetyDialog(action, target, risk, self)
        result = {}
        dialog.confirmed.connect(lambda r: result.update(r))
        dialog.exec()
        return result

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide()
            self.tray.showMessage(
                "JARVIS 4.5",
                "Running in background. Click the tray icon to restore.",
                QSystemTrayIcon.MessageIcon.Information,
                3000,
            )
            event.ignore()
        else:
            event.accept()


# ── Entry Point ──────────────────────────────────────────────────────────

def handle_signal(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down...")
    QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("4.5.0")
    app.setQuitOnLastWindowClosed(False)

    # Signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Qt translations
    qt_translator = QTranslator()
    qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    qt_translator.load(f"qt_{CURRENT_LANG}", qt_path)
    app.installTranslator(qt_translator)

    window = JarvisMainWindow()
    window.show()

    logger.info("JARVIS 4.5 Desktop App started")

    # Use timer to handle Unix signals
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    exit_code = app.exec()
    logger.info("JARVIS 4.5 Desktop App stopped")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
