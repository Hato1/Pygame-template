"""Test config."""

from pathlib import Path

import pytest

from pygame_me.config import load_config


def test_load_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Check game imports successfully."""
    monkeypatch.chdir(tmp_path)

    test_config = tmp_path / "config.yaml"
    test_config.write_text(
        """
    game:
        name: "Hello World!"

    """
    )

    c = load_config()
    assert c.game.name == "Hello World!"
