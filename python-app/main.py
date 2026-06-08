#!/usr/bin/env python3
"""
JARVIS 4.5 — Desktop Companion App
===================================
Modern Python desktop application for the JARVIS AI Operating Assistant.

Features:
    - Real-time audio frequency visualization (pyqtgraph)
    - Multilingual support (EN + AR with RTL)
    - Safety confirmation dialogs
    - WebSocket bridge for n8n integration
    - LLM integration via Groq API
    - Agent runtime monitoring
    - Emergency stop button
    - System tray integration

Environment:
    JARVIS_BRIDGE_SECRET  — Shared secret for n8n bridge auth
    BRIDGE_PORT           — WebSocket port (default: 8765)
    GROQ_API_KEY          — Groq API key for LLM chat
    JARVIS_MODEL          — Display name of active LLM model
"""

from __future__ import annotations

import sys
import os
import asyncio
import json
import logging
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

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

# ── Logging ──────────────────────────────────────────────────────────────

LOG_DIR = Path.home() / ".jarvis"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("jarvis.app")

# ── i18n ─────────────────────────────────────────────────────────────────

DEFAULT_LANG = "en"
CURRENT_LANG = os.environ.get("JARVIS_LANG", DEFAULT_LANG)

def load_translations(lang: str = CURRENT_LANG) -> dict:
    """Load translation strings."""
    locales_dir = Path(__file__).parent / "locales"
    file_path = locales_dir / f"{lang}.json"
    if not file_path.exists():
        file_path = locales_dir / f"{DEFAULT_LANG}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Global translation function set after QApplication creation
_ = None

# ── Safety Dialog ────────────────────────────────────────────────────────

class SafetyDialog(QDialog):
    """Modal dialog for confirming risky operations."""

    def __init__(self, action: str, target: str, risk: str, parent=None):
        super().__init__(parent)
        self.action = action
        self.target = target
        self.risk = risk
        self.result_data = {"confirmed": False, "remember": False}
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(_("safety_dialog_title") if _ else "Action Requires Confirmation")
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

        # Header
        header = QLabel(f"<h2 style='color: #f59e0b; margin: 0;'>⚠️ { _('action_requires_confirmation') if _ else 'Action Requires Confirmation'}</h2>")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Details
        details = QFrame()
        details.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 12px;")
        dlayout = QVBoxLayout(details)
        dlayout.setSpacing(8)

        dlayout.addWidget(QLabel(f"<b>{_('action') if _ else 'Action'}:</b> <span style='color: #e2e8f0;'>{self.action}</span>"))
        dlayout.addWidget(QLabel(f"<b>{_('target') if _ else 'Target'}:</b> <span style='color: #38bdf8;'>{self.target}</span>"))
        dlayout.addWidget(QLabel(f"<b>{_('risk') if _ else 'Risk'}:</b> <span style='color: #ef4444;'>{self.risk}</span>"))
        dlayout.addWidget(QLabel(f"<small style='color: #94a3b8;'>{_('requested_by') if _ else 'Requested by'}: n8n (JARVIS 4.5) | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>"))
        layout.addWidget(details)

        # Remember checkbox
        self.remember_cb = QCheckBox(_("remember_choice_5min") if _ else "Remember my choice for 5 minutes")
        layout.addWidget(self.remember_cb)

        # Buttons
        btn_layout = QHBoxLayout()
        self.deny_btn = QPushButton(f"❌ {_('deny') if _ else 'Deny'}")
        self.deny_btn.setStyleSheet("background: #ef4444; color: white;")
        self.deny_btn.clicked.connect(self._on_deny)
        self.allow_btn = QPushButton(f"✅ {_('allow') if _ else 'Allow'}")
        self.allow_btn.setStyleSheet("background: #22c55e; color: white;")
        self.allow_btn.clicked.connect(self._on_allow)
        btn_layout.addWidget(self.deny_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.allow_btn)
        layout.addLayout(btn_layout)

        # Timeout
        self.timeout_label = QLabel(f"⏱️ {_('auto_deny_in') if _ else 'Auto-deny in'} 60s")
        self.timeout_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeout_label.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.timeout_label)

        self.remaining = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _tick(self):
        self.remaining -= 1
        self.timeout_label.setText(f"⏱️ {_('auto_deny_in') if _ else 'Auto-deny in'} {self.remaining}s")
        if self.remaining <= 0:
            self._on_deny()

    def _on_allow(self):
        self.result_data = {"confirmed": True, "remember": self.remember_cb.isChecked()}
        self.timer.stop()
        self.accept()

    def _on_deny(self):
        self.result_data = {"confirmed": False, "remember": self.remember_cb.isChecked()}
        self.timer.stop()
        self.reject()


# ── Audio Visualization ──────────────────────────────────────────────────

class AudioVizWidget(QFrame):
    """Real-time audio frequency visualization using simulated data."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.setMaximumHeight(160)
        self.setStyleSheet("background: #0f172a; border-radius: 8px;")
        self._bars = [0.0] * 32
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_bars)
        self._timer.start(50)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        self.label = QLabel(f"🎤 { _('audio_visualization') if _ else 'Audio Frequency Visualization'}")
        self.label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(self.label)

    def _update_bars(self):
        import random
        import math
        self._bars = [
            max(0.05, min(1.0, abs(math.sin(i * 0.3 + time.time() * 2) * random.uniform(0.5, 1.0))))
            for i in range(32)
        ]
        self.update()

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
    """Bottom status panel with model info and bridge status."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_name = os.environ.get("JARVIS_MODEL", "llama-4-scout-17b-16e-instruct")
        self.bridge_status = "disconnected"
        self.pending_confirmations = 0
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 4px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        self.model_label = QLabel(f"🤖 <b>Model:</b> {self.model_name}")
        self.model_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.model_label)

        self.bridge_label = QLabel(f"🔗 <b>Bridge:</b> <span style='color: #ef4444;'>●</span> Disconnected")
        self.bridge_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.bridge_label)

        self.agent_label = QLabel(f"🎯 <b>Agents:</b> 9 active")
        self.agent_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.agent_label)

        self.runtime_label = QLabel(f"⏱️ <b>Runtime:</b> idle")
        self.runtime_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.runtime_label)

    def set_bridge_connected(self, connected: bool):
        self.bridge_status = "connected" if connected else "disconnected"
        color = "#22c55e" if connected else "#ef4444"
        status = "Connected" if connected else "Disconnected"
        self.bridge_label.setText(f"🔗 <b>Bridge:</b> <span style='color: {color};'>●</span> {status}")

    def set_runtime_state(self, state: str):
        self.runtime_label.setText(f"⏱️ <b>Runtime:</b> {state}")

    def set_pending_confirmations(self, count: int):
        self.pending_confirmations = count


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

        # Chat history
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

        # Input area
        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(_("type_message") if _ else "Type a message...")
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


# ── Bridge Thread ────────────────────────────────────────────────────────

class BridgeThread(QThread):
    """Runs the WebSocket bridge server in a background thread."""

    message_received = pyqtSignal(dict)
    client_connected = pyqtSignal()
    client_disconnected = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, port: int = 8765, secret: str = ""):
        super().__init__()
        self.port = port
        self.secret = secret
        self._running = True
        self._loop: asyncio.AbstractEventLoop | None = None

    def run(self):
        try:
            import websockets
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            from bridge_server import BridgeServer

            async def start():
                server = BridgeServer()
                await server.start()

            self._loop.run_until_complete(start())
        except ImportError:
            self.error_occurred.emit("websockets library not installed")
        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self):
        self._running = False
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        self.quit()
        self.wait(3000)


# ── LLM Worker ───────────────────────────────────────────────────────────

class LLMWorker(QThread):
    """Worker thread for LLM API calls."""

    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, api_key: str, model: str, message: str, context: list = None):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.message = message
        self.context = context or []

    def run(self):
        try:
            messages = [{"role": "system", "content": "You are JARVIS 4.5, a highly capable personal AI assistant. Be helpful, concise, and precise."}]
            for ctx in self.context[-5:]:
                messages.append(ctx)
            messages.append({"role": "user", "content": self.message})

            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=json.dumps({
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 2000,
                }).encode(),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                content = data["choices"][0]["message"]["content"]
                self.response_ready.emit(content)
        except urllib.error.HTTPError as e:
            self.error_occurred.emit(f"API Error: {e.code} - {e.reason}")
        except Exception as e:
            self.error_occurred.emit(str(e))


# ── Main Window ──────────────────────────────────────────────────────────

class JarvisMainWindow(QMainWindow):
    """Main application window for JARVIS 4.5 Companion."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS 4.5 — AI Operating Assistant")
        self.setMinimumSize(1000, 750)
        self._llm_workers: list[LLMWorker] = []
        self._chat_context: list[dict] = []
        self._setup_ui()
        self._setup_tray()
        self._setup_shortcuts()
        self._apply_theme()

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

        # Audio viz
        self.audio_viz = AudioVizWidget()
        right_layout.addWidget(self.audio_viz)

        # Status panel
        self.status_panel = StatusPanel()
        right_layout.addWidget(self.status_panel)

        # Quick actions
        actions_frame = QFrame()
        actions_frame.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 8px;")
        actions_layout = QVBoxLayout(actions_frame)
        actions_label = QLabel("<b>Quick Actions</b>")
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
        self.status_bar.showMessage("JARVIS 4.5 Ready")
        self.setStatusBar(self.status_bar)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        self.tray.setToolTip("JARVIS 4.5")

        tray_menu = QMenu()
        show_action = QAction(_("show") if _ else "Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction(_("quit") if _ else "Quit", self)
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

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def _toggle_language(self):
        global CURRENT_LANG, _
        CURRENT_LANG = "ar" if CURRENT_LANG == "en" else "en"
        _ = load_translations(CURRENT_LANG)
        if CURRENT_LANG == "ar":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.chat_panel.input_field.setPlaceholderText(_("type_message"))
        logger.info(f"Language switched to: {CURRENT_LANG}")
        QMessageBox.information(self, _("language_changed"), f"Language: {CURRENT_LANG.upper()}")

    def _emergency_stop(self):
        """Trigger emergency stop."""
        from security.permissions import permission_engine
        permission_engine.trigger_emergency_stop()
        self.chat_panel.add_message("system", "🛑 EMERGENCY STOP ACTIVATED — All operations halted")
        self.status_panel.set_runtime_state("emergency_stop")
        logger.critical("Emergency stop activated from UI")

    def _clear_chat(self):
        self.chat_panel.clear_history()
        self._chat_context.clear()
        self.chat_panel.add_message("system", "Chat history cleared")

    def _quit(self):
        self.tray.hide()
        QApplication.quit()

    def _process_message(self, text: str):
        """Process user message through LLM."""
        api_key = os.environ.get("GROQ_API_KEY", "")
        model = os.environ.get("JARVIS_MODEL", "llama-3.3-70b-versatile")

        if not api_key:
            self.chat_panel.add_message("error", "GROQ_API_KEY not set. Please set your API key.")
            return

        self.status_panel.set_runtime_state("processing")

        worker = LLMWorker(api_key, model, text, self._chat_context)
        worker.response_ready.connect(self._handle_response)
        worker.error_occurred.connect(self._handle_llm_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._llm_workers.append(worker)
        worker.start()

        self._chat_context.append({"role": "user", "content": text})

    def _handle_response(self, text: str):
        self.chat_panel.add_message("assistant", text)
        self._chat_context.append({"role": "assistant", "content": text})
        self.status_panel.set_runtime_state("idle")

    def _handle_llm_error(self, error: str):
        self.chat_panel.add_message("error", f"LLM Error: {error}")
        self.status_panel.set_runtime_state("error")

    def _cleanup_worker(self, worker):
        if worker in self._llm_workers:
            self._llm_workers.remove(worker)
        worker.deleteLater()

    def _quick_action(self, action: str):
        """Handle quick action buttons."""
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
        """Show safety confirmation dialog."""
        dialog = SafetyDialog(action, target, risk, self)
        dialog.exec()
        return dialog.result_data

    def closeEvent(self, event):
        """Handle window close — minimize to tray instead."""
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

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("4.5.0")
    app.setQuitOnLastWindowClosed(False)

    # Load translations
    global _
    _ = load_translations(CURRENT_LANG)

    if CURRENT_LANG == "ar":
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # Qt translations for standard dialogs
    qt_translator = QTranslator()
    qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    qt_translator.load(f"qt_{CURRENT_LANG}", qt_path)
    app.installTranslator(qt_translator)

    # Create main window
    window = JarvisMainWindow()
    window.show()

    # Start bridge server in background thread
    bridge_secret = os.environ.get("JARVIS_BRIDGE_SECRET", "change-me-in-production")
    bridge_port = int(os.environ.get("BRIDGE_PORT", "8765"))
    bridge_thread = BridgeThread(port=bridge_port, secret=bridge_secret)
    bridge_thread.client_connected.connect(lambda: window.status_panel.set_bridge_connected(True))
    bridge_thread.client_disconnected.connect(lambda: window.status_panel.set_bridge_connected(False))
    bridge_thread.start()

    logger.info("JARVIS 4.5 Companion App started")

    try:
        exit_code = app.exec()
    finally:
        bridge_thread.stop()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
