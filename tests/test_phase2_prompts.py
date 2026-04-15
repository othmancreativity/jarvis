"""Phase 2.3 / 2.17.1 — Personas and Arabic/English system prompts."""

from __future__ import annotations

from models.llm.prompts import combined_system, jarvis_persona_ar


def test_jarvis_persona_ar_contains_jarvis() -> None:
    p = jarvis_persona_ar()
    assert "جارفيس" in p or "jarvis" in p.lower()


def test_combined_system_ar_mode() -> None:
    s = combined_system(language="ar", mode="normal")
    assert len(s) > 20
    assert "جارفيس" in s or "Jarvis" in s
