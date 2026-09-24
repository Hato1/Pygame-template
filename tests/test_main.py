"""Test basic project functionality."""

import pytest


def test_game_import() -> None:
    """Check project imports successfully."""
    import my_game  # noqa: F401


@pytest.mark.filterwarnings("ignore:no fast renderer available")
def test_main_exists():
    """Check main function exists.

    This is required for web builds, which need to call main() to start the game.
    """
    from my_game.main import main

    assert callable(main)


def test_state_transition_uses_explicit_enter_exit_and_payload() -> None:
    """State transitions should pass payloads through an explicit lifecycle."""
    import pygame as pg

    from my_game.utils.state_manager import State, StateManager

    class Alpha(State):
        def handle_event(self, event: pg.event.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, keys, dt: float) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    class Beta(State):
        def handle_event(self, event: pg.event.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, keys, dt: float) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    screen = pg.display.set_mode((64, 64))
    states = {Alpha: Alpha(), Beta: Beta()}
    manager = StateManager(screen, states, Alpha, "Transition test")

    alpha = manager.current_state
    alpha.done = True
    alpha.next_state = Beta
    alpha.persist["score"] = 42

    manager.change_state(Beta)

    assert manager.current_state is states[Beta]
    assert manager.current_state.persist == {"score": 42}
    assert manager.current_state.previous_state is Alpha
