#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import logging
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

from config import config
from jarvis.logger import logger

LOG_DIR = config.log_dir
LOG_DIR.mkdir(parents=True, exist_ok=True)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
    QSystemTrayIcon, QMenu, QMessageBox, QDialog,
    QCheckBox, QFrame, QProgressBar,
    QStatusBar,
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer,
)
from PyQt6.QtGui import QAction, QKeySequence, QShortcut

from core.jarvis_core import JarvisCore

CURRENT_LANG = config.language


def load_translations(lang: str = CURRENT_LANG) -> dict:
    locales_dir = Path(__file__).parent / "locales"
    fp = locales_dir / f"{lang}.json"
    if not fp.exists():
        fp = locales_dir / "en.json"
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return {}


_translations = load_translations(CURRENT_LANG)


def _(key: str, fallback: str = "") -> str:
    return _translations.get(key, fallback or key)


class SafetyDialog(QDialog):
    confirmed = pyqtSignal(dict)

    def __init__(self, action: str, target: str, risk: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Action Requires Confirmation")
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
        layout.addWidget(QLabel(f'<h3 style="color: #f59e0b;">Action: {action}</h3>'))
        layout.addWidget(QLabel(f"Target: {target}"))
        layout.addWidget(QLabel(f'<span style="color: #ef4444;">Risk: {risk}</span>'))
        btn_layout = QHBoxLayout()
        deny = QPushButton("Deny")
        deny.setStyleSheet("background: #ef4444; color: white;")
        deny.clicked.connect(lambda: (self.confirmed.emit({"confirmed": False}), self.reject()))
        allow = QPushButton("Allow")
        allow.setStyleSheet("background: #22c55e; color: white;")
        allow.clicked.connect(lambda: (self.confirmed.emit({"confirmed": True}), self.accept()))
        btn_layout.addWidget(deny)
        btn_layout.addStretch()
        btn_layout.addWidget(allow)
        layout.addLayout(btn_layout)


class CoreThread(QThread):
    response_ready = pyqtSignal(str)
    status_update = pyqtSignal(str, dict)
    initialized = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.core: JarvisCore = None
        self._loop: asyncio.AbstractEventLoop = None

    def run(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._main())
        except Exception as e:
            self.error_occurred.emit(str(e))

    async def _main(self):
        self.core = JarvisCore()
        self.core.on_response(self._on_response)
        self.core.on_status_update(self._on_status)
        await self.core.initialize()
        self.initialized.emit()
        await self.core.run()

    def _on_response(self, text: str):
        self.response_ready.emit(text)

    def _on_status(self, status: str, data: dict):
        self.status_update.emit(status, data)

    def process_message(self, text: str):
        if self.core and self._loop:
            asyncio.run_coroutine_threadsafe(self.core.process_input(text), self._loop)

    def emergency_stop(self):
        if self.core:
            self.core.emergency_stop()

    def stop(self):
        if self.core and self._loop:
            asyncio.run_coroutine_threadsafe(self.core.stop(), self._loop)
        self.quit()
        self.wait(5000)


class JarvisMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS 4.6 - AI Operating Assistant")
        self.setMinimumSize(1000, 750)
        self._setup_ui()
        self._setup_tray()
        self._start_core()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        self.emergency_btn = QPushButton("STOP")
        self.emergency_btn.setStyleSheet("background: #ef4444; color: white; font-weight: bold; padding: 8px 16px;")
        self.emergency_btn.clicked.connect(self._emergency_stop)
        toolbar.addWidget(self.emergency_btn)

        self.loading_bar = QProgressBar()
        self.loading_bar.setMaximumWidth(150)
        self.loading_bar.setRange(0, 0)
        self.loading_bar.hide()
        toolbar.addWidget(self.loading_bar)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._clear_chat)
        toolbar.addWidget(self.clear_btn)

        toolbar.addStretch()
        vlabel = QLabel("v4.6.0")
        vlabel.setStyleSheet("color: #64748b;")
        toolbar.addWidget(vlabel)
        layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.chat_panel = QFrame()
        chat_layout = QVBoxLayout(self.chat_panel)
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setStyleSheet("background: #1e293b; color: #e2e8f0; border-radius: 8px; padding: 8px;")
        chat_layout.addWidget(self.history)

        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.returnPressed.connect(self._send)
        self.input_field.setStyleSheet("padding: 10px; border-radius: 6px; background: #334155; color: #f1f5f9;")
        input_row.addWidget(self.input_field)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("background: #3b82f6; color: white; padding: 8px 16px;")
        self.send_btn.clicked.connect(self._send)
        input_row.addWidget(self.send_btn)
        chat_layout.addLayout(input_row)
        splitter.addWidget(self.chat_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.status_display = QLabel("JARVIS Initializing...")
        self.status_display.setStyleSheet("color: #94a3b8; padding: 8px;")
        right_layout.addWidget(self.status_display)
        right_layout.addStretch()
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])
        layout.addWidget(splitter)

        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Initializing...")
        self.setStatusBar(self.status_bar)

        self.setStyleSheet("""
            QMainWindow { background: #0f172a; }
            QWidget { font-family: 'Segoe UI', sans-serif; }
            QPushButton { background: #334155; color: #f1f5f9; border: none; border-radius: 6px; padding: 6px 12px; }
            QPushButton:hover { background: #475569; }
            QLineEdit { border: 1px solid #334155; }
            QStatusBar { background: #1e293b; color: #94a3b8; }
        """)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        self.tray.setToolTip("JARVIS 4.6")
        menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        menu.addAction(show_action)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def _start_core(self):
        self.core_thread = CoreThread()
        self.core_thread.response_ready.connect(self._handle_response)
        self.core_thread.status_update.connect(self._handle_status)
        self.core_thread.initialized.connect(self._on_core_ready)
        self.core_thread.error_occurred.connect(self._handle_error)
        self.core_thread.start()

    def _on_core_ready(self):
        self.status_bar.showMessage("JARVIS 4.6 Ready")
        self._add_message("system", "JARVIS 4.6 is ready. How can I help you?")

    def _send(self):
        text = self.input_field.text().strip()
        if text:
            self._add_message("user", text)
            self.loading_bar.show()
            self.input_field.clear()
            self.core_thread.process_message(text)

    def _add_message(self, role: str, text: str):
        colors = {"user": "#3b82f6", "assistant": "#22c55e", "system": "#f59e0b", "error": "#ef4444"}
        labels = {"user": "You", "assistant": "JARVIS", "system": "System", "error": "Error"}
        color = colors.get(role, "#94a3b8")
        label = labels.get(role, "Unknown")
        timestamp = datetime.now().strftime("%H:%M")
        html = f'<p><span style="color: {color};"><b>{label}</b></span> <span style="color: #64748b;">{timestamp}</span><br>{text}</p>'
        self.history.append(html)

    def _handle_response(self, text: str):
        self._add_message("assistant", text)
        self.loading_bar.hide()
        self.status_bar.showMessage("Ready")

    def _handle_status(self, status: str, data: dict):
        self.status_display.setText(f"Status: {status}" if not data else f"Status: {status} - {data}")

    def _handle_error(self, error: str):
        self._add_message("error", f"Error: {error}")
        self.loading_bar.hide()

    def _emergency_stop(self):
        self.core_thread.emergency_stop()
        self._add_message("system", "EMERGENCY STOP ACTIVATED")

    def _clear_chat(self):
        self.history.clear()

    def _quit(self):
        if hasattr(self, 'core_thread'):
            self.core_thread.stop()
        QApplication.quit()

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("4.6.0")
    app.setQuitOnLastWindowClosed(False)

    signal.signal(signal.SIGINT, lambda s, f: QApplication.quit())
    signal.signal(signal.SIGTERM, lambda s, f: QApplication.quit())

    window = JarvisMainWindow()
    window.show()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
