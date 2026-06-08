#!/usr/bin/env python3
"""
JARVIS 4.0 — Desktop Companion App
====================================
A modern Python desktop application that serves as the local control panel
for the JARVIS automation system. Features real-time audio visualization,
multilingual support (English + Arabic with RTL), safety confirmation dialogs,
and a WebSocket bridge for n8n integration.

Usage:
    python main.py

Environment Variables:
    JARVIS_BRIDGE_SECRET  — Shared secret for n8n bridge auth
    BRIDGE_PORT           — WebSocket port (default: 8765)
    JARVIS_MODEL          — Display name of the active LLM model
"""

import sys
import os
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
    QSystemTrayIcon, QMenu, QStyle, QMessageBox, QDialog,
    QDialogButtonBox, QCheckBox, QFrame
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QLocale, QTranslator,
    QLibraryInfo, QPoint
)
from PyQt6.QtGui import QAction, QFont, QIcon, QPalette, QColor

# ---------------------------------------------------------------------------
# Configure logging
# ---------------------------------------------------------------------------
LOG_DIR = Path.home() / ".jarvis"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "audit.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("jarvis")

# ---------------------------------------------------------------------------
# i18n Setup
# ---------------------------------------------------------------------------
DEFAULT_LANG = "en"
CURRENT_LANG = os.environ.get("JARVIS_LANG", DEFAULT_LANG)

def load_translations(lang: str = CURRENT_LANG) -> dict:
    """Load translation strings from locales/ directory."""
    locales_dir = Path(__file__).parent / "locales"
    file_path = locales_dir / f"{lang}.json"
    if not file_path.exists():
        file_path = locales_dir / f"{DEFAULT_LANG}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

_ = None  # Will be set after QApplication creation

# ---------------------------------------------------------------------------
# Safety Confirmation Dialog
# ---------------------------------------------------------------------------
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
        self.setWindowTitle(_("safety_dialog_title") if _ else "⚠️ Confirm Action")
        self.setMinimumWidth(480)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Warning icon + header
        header = QLabel(
            f"<h2 style='color: #f59e0b;'>⚠️ "
            f"{_('action_requires_confirmation') if _ else 'Action Requires Confirmation'}"
            f"</h2>"
        )
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Details frame
        details = QFrame()
        details.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 12px;")
        dlayout = QVBoxLayout(details)

        dlayout.addWidget(QLabel(f"<b>{_('action') if _ else 'Action'}:</b> {self.action}"))
        dlayout.addWidget(QLabel(f"<b>{_('target') if _ else 'Target'}:</b> {self.target}"))
        dlayout.addWidget(QLabel(f"<b>{_('risk') if _ else 'Risk'}:</b> <span style='color: #ef4444;'>{self.risk}</span>"))
        dlayout.addWidget(QLabel(f"<small>{_('requested_by') if _ else 'Requested by'}: n8n (JARVIS Agent) | "
                                 f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>"))
        layout.addWidget(details)

        # Remember checkbox
        self.remember_cb = QCheckBox(_("remember_choice_5min") if _ else "☑️ Remember my choice for 5 minutes")
        layout.addWidget(self.remember_cb)

        # Buttons
        btn_box = QDialogButtonBox()
        self.deny_btn = btn_box.addButton(
            _("deny") if _ else "❌ Deny", QDialogButtonBox.ButtonRole.RejectRole
        )
        self.allow_btn = btn_box.addButton(
            _("allow") if _ else "✅ Allow", QDialogButtonBox.ButtonRole.AcceptRole
        )
        btn_box.accepted.connect(self._on_allow)
        btn_box.rejected.connect(self._on_deny)
        layout.addWidget(btn_box)

        # Timeout warning
        self.timeout_label = QLabel(_("auto_deny_60s") if _ else "⏱️ Auto-deny in 60 seconds")
        self.timeout_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeout_label.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.timeout_label)

        # Countdown timer
        self.remaining = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _tick(self):
        self.remaining -= 1
        self.timeout_label.setText(
            f"⏱️ {_('auto_deny_in') if _ else 'Auto-deny in'} {self.remaining}s"
        )
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


# ---------------------------------------------------------------------------
# Audio Visualization Widget (Placeholder — pyqtgraph integration)
# ---------------------------------------------------------------------------
class AudioVizWidget(QFrame):
    """Real-time audio frequency visualization panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.setMaximumHeight(160)
        self.setStyleSheet("background: #0f172a; border-radius: 8px;")
        self._setup_ui()
        self._bars = [0.0] * 32
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_bars)
        self._timer.start(50)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        self.label = QLabel("🎤 " + (_("audio_visualization") if _ else "Audio Frequency Visualization"))
        self.label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def _update_bars(self):
        import random
        import math
        # Simulate FFT data — replace with actual pyaudio + pyqtgraph integration
        self._bars = [
            max(0.05, min(1.0, abs(math.sin(i * 0.3 + self._bars[i] * 2) * random.uniform(0.7, 1.3))))
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


# ---------------------------------------------------------------------------
# Model Display Widget (Bottom-Left)
# ---------------------------------------------------------------------------
class ModelDisplayWidget(QFrame):
    """Displays the currently selected on-device model."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_name = os.environ.get("JARVIS_MODEL", "llama-4-scout-17b-16e-instruct")
        self.bridge_status = "disconnected"
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background: #1e293b; border-radius: 8px; padding: 4px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        self.model_label = QLabel(f"🤖 <b>{_('model') if _ else 'Model'}:</b> {self.model_name}")
        self.model_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.model_label)

        self.bridge_label = QLabel(f"🔗 <b>{_('bridge') if _ else 'Bridge'}:</b> <span style='color: #ef4444;'>●</span> {_('disconnected') if _ else 'Disconnected'}")
        self.bridge_label.setStyleSheet("color: #e2e8f0; font-size: 11px;")
        layout.addWidget(self.bridge_label)

    def set_bridge_connected(self, connected: bool):
        self.bridge_status = "connected" if connected else "disconnected"
        color = "#22c55e" if connected else "#ef4444"
        status_text = (_("connected") if _ else "Connected") if connected else (_("disconnected") if _ else "Disconnected")
        self.bridge_label.setText(f"🔗 <b>{_('bridge') if _ else 'Bridge'}:</b> <span style='color: {color};'>●</span> {status_text}")


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------
class JarvisMainWindow(QMainWindow):
    """Main application window for JARVIS Companion."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS 4.0 — Companion")
        self.setMinimumSize(900, 700)
        self._setup_ui()
        self._setup_tray()
        self._apply_theme()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Top bar: Language switcher
        top_bar = QHBoxLayout()
        self.lang_btn = QPushButton("🌐 EN / AR")
        self.lang_btn.setToolTip("Switch language / تبديل اللغة")
        self.lang_btn.setFixedWidth(100)
        self.lang_btn.clicked.connect(self._toggle_language)
        top_bar.addStretch()
        top_bar.addWidget(self.lang_btn)
        layout.addLayout(top_bar)

        # Main splitter: Chat + Side panel
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Chat panel
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("background: #1e293b; color: #e2e8f0; border-radius: 8px; padding: 8px;")
        chat_layout.addWidget(self.chat_history)

        # Input area
        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(_("type_message") if _ else "Type a message...")
        self.input_field.returnPressed.connect(self._send_message)
        self.input_field.setStyleSheet("padding: 8px; border-radius: 6px; background: #334155; color: #f1f5f9;")
        input_row.addWidget(self.input_field)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedWidth(40)
        self.send_btn.clicked.connect(self._send_message)
        input_row.addWidget(self.send_btn)

        self.voice_btn = QPushButton("🎤")
        self.voice_btn.setFixedWidth(40)
        self.voice_btn.setToolTip(_("voice_input") if _ else "Voice input")
        input_row.addWidget(self.voice_btn)
        chat_layout.addLayout(input_row)

        splitter.addWidget(chat_widget)

        # Right panel: Audio viz + Model display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.audio_viz = AudioVizWidget()
        right_layout.addWidget(self.audio_viz)

        right_layout.addStretch()

        self.model_display = ModelDisplayWidget()
        right_layout.addWidget(self.model_display)

        splitter.addWidget(right_panel)
        splitter.setSizes([650, 250])
        layout.addWidget(splitter)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.tray.setToolTip("JARVIS 4.0")

        tray_menu = QMenu()
        show_action = QAction(_("show") if _ else "Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        quit_action = QAction(_("quit") if _ else "Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #0f172a; }
            QPushButton {
                background: #334155; color: #f1f5f9; border: none;
                border-radius: 6px; padding: 6px 12px;
            }
            QPushButton:hover { background: #475569; }
            QTextEdit { border: 1px solid #334155; }
            QLineEdit { border: 1px solid #334155; }
        """)

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self._append_chat("user", text)
        self.input_field.clear()

        # TODO: Send to local LLM or n8n for processing
        self._append_chat("assistant", f"Echo: {text}")

    def _append_chat(self, role: str, text: str):
        color = "#3b82f6" if role == "user" else "#22c55e"
        label = "You" if role == "user" else "JARVIS"
        self.chat_history.append(
            f'<p><span style="color: {color};"><b>{label}:</b></span> {text}</p>'
        )

    def _toggle_language(self):
        """Toggle between English and Arabic."""
        global CURRENT_LANG, _
        CURRENT_LANG = "ar" if CURRENT_LANG == "en" else "en"

        if CURRENT_LANG == "ar":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Reload translations
        _ = load_translations(CURRENT_LANG)
        self.input_field.setPlaceholderText(_("type_message"))
        logger.info(f"Language switched to: {CURRENT_LANG}")
        QMessageBox.information(self, _("language_changed"), f"Language: {CURRENT_LANG.upper()}")

    def show_safety_dialog(self, action: str, target: str, risk: str) -> dict:
        """Show safety confirmation dialog. Returns {'confirmed': bool, 'remember': bool}."""
        dialog = SafetyDialog(action, target, risk, self)
        dialog.exec()
        return dialog.result_data


# ---------------------------------------------------------------------------
# Bridge Server Thread
# ---------------------------------------------------------------------------
class BridgeServerThread(QThread):
    """Runs the WebSocket bridge server in a background thread."""

    message_received = pyqtSignal(dict)
    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self, port: int = 8765, secret: str = ""):
        super().__init__()
        self.port = port
        self.secret = secret
        self._running = True

    def run(self):
        try:
            import websockets
            import asyncio

            async def handler(websocket):
                self.connected.emit()
                logger.info(f"Bridge client connected: {websocket.remote_address}")
                try:
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            self.message_received.emit(data)
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON from bridge: {message[:200]}")
                except websockets.exceptions.ConnectionClosed:
                    pass
                finally:
                    self.disconnected.emit()
                    logger.info("Bridge client disconnected")

            async def start_server():
                server = await websockets.serve(handler, "0.0.0.0", self.port)
                logger.info(f"Bridge server started on ws://0.0.0.0:{self.port}")
                await server.wait_closed()

            asyncio.run(start_server())

        except ImportError:
            logger.error("websockets library not installed. Run: pip install websockets")
        except Exception as e:
            logger.error(f"Bridge server error: {e}")

    def stop(self):
        self._running = False
        self.quit()
        self.wait(2000)


# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("4.0.0")

    # Load translations
    global _
    _ = load_translations(CURRENT_LANG)

    # Apply RTL if Arabic
    if CURRENT_LANG == "ar":
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # Qt translations for standard dialogs
    qt_translator = QTranslator()
    qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    qt_translator.load(f"qt_{CURRENT_LANG}", qt_path)
    app.installTranslator(qt_translator)

    window = JarvisMainWindow()
    window.show()

    # Start bridge server
    bridge_secret = os.environ.get("JARVIS_BRIDGE_SECRET", "change-me-in-production")
    bridge_port = int(os.environ.get("BRIDGE_PORT", "8765"))
    bridge_thread = BridgeServerThread(port=bridge_port, secret=bridge_secret)
    bridge_thread.connected.connect(lambda: window.model_display.set_bridge_connected(True))
    bridge_thread.disconnected.connect(lambda: window.model_display.set_bridge_connected(False))
    bridge_thread.start()

    logger.info("JARVIS 4.0 Companion App started")

    try:
        exit_code = app.exec()
    finally:
        bridge_thread.stop()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
