from enum import Enum
from typing import Any

from my_game.core.input_manager import InputManager
from my_game.core.state_manager import TransitionData


def test_state_transition_uses_explicit_enter_exit_and_payload() -> None:
    """State transitions should pass payloads through an explicit lifecycle."""
    import pygame as pg

    from my_game.core.state_manager import State, StateManager

    class Alpha(State):
        def handle_event(self, actions: set[Enum], data: dict[str, Any]) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    class Beta(State):
        def handle_event(self, actions: set[Enum], data: dict[str, Any]) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

        def enter(self, surface_rect: pg.Rect, transition_data: TransitionData) -> None:
            super().enter(surface_rect, transition_data)
            assert transition_data.previous_state is Alpha
            assert transition_data.score == 42

    screen = pg.display.set_mode((64, 64))
    states = {Alpha: Alpha(), Beta: Beta()}
    manager = StateManager(screen, states, Alpha, InputManager(Enum), "Transition test")

    alpha = manager.current_state
    alpha.done = True
    alpha.transition_data.score = 42

    manager.change_state(Beta)

    assert manager.current_state is states[Beta]
