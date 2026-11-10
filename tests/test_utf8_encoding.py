"""Ensure markdown files are always read and written as UTF-8."""

from __future__ import annotations

import io as _io
from typing import TYPE_CHECKING, Any

from markdown_code_runner import update_markdown_file

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_update_markdown_file_forces_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-UTF-8 platform defaults must not break UTF-8 markdown files."""
    original_io_open = _io.open

    def cp1252_default_open(
        file: Any,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if "b" not in mode and encoding is None and "encoding" not in kwargs:
            encoding = "cp1252"
        return original_io_open(file, mode, buffering, encoding, *args, **kwargs)

    monkeypatch.setattr(_io, "open", cp1252_default_open)

    doc = tmp_path / "doc.md"
    # U+00CD encodes as b"\xc3\x8d" in UTF-8; 0x8D is undefined in cp1252,
    # so a locale-default read must raise UnicodeDecodeError here.
    doc.write_bytes("# Caf\u00e9 \u00cd \u2615\n\nplain text\n".encode("utf-8"))

    update_markdown_file(doc)

    text = doc.read_text(encoding="utf-8")
    assert "\u00cd" in text
    assert "\u2615" in text
