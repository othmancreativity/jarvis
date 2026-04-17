"""Phase 3 tests: Context Buffer system."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from core.context.buffer import ContextBuffer, InputType


class TestContextBuffer:
    def test_add_text(self):
        buf = ContextBuffer()
        iid = buf.add_text("Hello world")
        assert buf.count == 1
        assert not buf.is_empty

        items = buf.snapshot()
        assert items[0].input_type == InputType.TEXT
        assert items[0].content == "Hello world"

    def test_add_file(self, tmp_path):
        f = tmp_path / "test.pdf"
        f.write_text("fake pdf content")

        buf = ContextBuffer()
        iid = buf.add_file(f)
        items = buf.snapshot()
        assert items[0].input_type == InputType.FILE
        assert items[0].metadata["extension"] == ".pdf"
        assert items[0].metadata["size_bytes"] > 0

    def test_add_image(self, tmp_path):
        f = tmp_path / "photo.jpg"
        f.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        buf = ContextBuffer()
        buf.add_image(f)
        items = buf.snapshot()
        assert items[0].input_type == InputType.IMAGE

    def test_add_audio(self, tmp_path):
        f = tmp_path / "voice.wav"
        f.write_bytes(b"\x00" * 50)

        buf = ContextBuffer()
        buf.add_audio(f)
        assert buf.modality_flags()["has_audio"] is True

    def test_multiple_inputs(self):
        buf = ContextBuffer()
        buf.add_text("First")
        buf.add_text("Second")
        buf.add_text("Third")
        assert buf.count == 3

        text = buf.text_content()
        assert "First" in text
        assert "Third" in text

    def test_merged_summary(self):
        buf = ContextBuffer()
        buf.add_text("Hello world this is a test")
        summary = buf.merged_summary()
        assert "Buffered inputs:" in summary
        assert "[text]" in summary

    def test_modality_flags(self, tmp_path):
        buf = ContextBuffer()
        buf.add_text("test")
        flags = buf.modality_flags()
        assert flags["has_text"] is True
        assert flags["has_image"] is False

    def test_clear(self):
        buf = ContextBuffer()
        buf.add_text("test")
        buf.add_text("test2")
        buf.clear()
        assert buf.is_empty

    def test_remove(self):
        buf = ContextBuffer()
        iid = buf.add_text("to remove")
        buf.add_text("to keep")
        assert buf.count == 2

        removed = buf.remove(iid)
        assert removed is True
        assert buf.count == 1

    def test_max_items_eviction(self):
        buf = ContextBuffer(max_items=3)
        for i in range(5):
            buf.add_text(f"msg {i}")
        assert buf.count == 3
        # Oldest should have been evicted
        items = buf.snapshot()
        assert items[0].content == "msg 2"

    def test_file_type_classification(self, tmp_path):
        buf = ContextBuffer()

        img = tmp_path / "photo.png"
        img.write_bytes(b"\x89PNG")
        buf.add_file(img)

        audio = tmp_path / "sound.mp3"
        audio.write_bytes(b"\x00" * 10)
        buf.add_file(audio)

        doc = tmp_path / "readme.txt"
        doc.write_text("text file")
        buf.add_file(doc)

        items = buf.snapshot()
        assert items[0].input_type == InputType.IMAGE
        assert items[1].input_type == InputType.AUDIO
        assert items[2].input_type == InputType.FILE
