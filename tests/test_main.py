"""Test basic project functionality."""


def test_game_import() -> None:
    """Check project imports successfully."""
    import my_game  # noqa: F401


def test_main_exists():
    """Check main function exists.

    This is required for web builds, which need to call main() to start the game.
    """
    from my_game.main import main

    assert callable(main)
