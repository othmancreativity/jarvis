from __future__ import annotations

import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def mock_groq_api() -> Generator[MagicMock, None, None]:
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Mock response from Groq"}}]
        }
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_playwright() -> Generator[MagicMock, None, None]:
    mock_page = AsyncMock()
    mock_page.title.return_value = "Mock Page"
    mock_page.url = "https://example.com"
    mock_page.screenshot.return_value = b"mock_png_bytes"
    mock_page.goto.return_value = None

    mock_context = AsyncMock()
    mock_context.new_page.return_value = mock_page

    mock_browser = AsyncMock()
    mock_browser.new_context.return_value = mock_context

    mock_playwright_instance = AsyncMock()
    mock_playwright_instance.chromium.launch.return_value = mock_browser

    with patch("jarvis.browser_pool.async_playwright") as mock_pw:
        mock_pw.return_value.start.return_value = mock_playwright_instance
        yield mock_pw


@pytest.fixture
def jarvis_core() -> AsyncGenerator[Any, None]:
    from core.jarvis_core import JarvisCore
    core = JarvisCore()
    yield core


@pytest.fixture
def memory_agent() -> AsyncGenerator[Any, None]:
    from agents.memory_agent import MemoryAgent
    agent = MemoryAgent()
    yield agent


@pytest.fixture
def sample_vector_store(temp_dir: Path) -> Path:
    store_path = temp_dir / "vector_store"
    store_path.mkdir(parents=True, exist_ok=True)
    return store_path
