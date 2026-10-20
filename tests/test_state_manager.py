from enum import Enum

import pytest

from my_game.core.input_manager import InputManager, InputState
from my_game.core.state_manager import TransitionData


def test_state_transition_uses_explicit_enter_exit_and_payload() -> None:
    """State transitions should pass payloads through an explicit lifecycle."""
    import pygame as pg

    from my_game.core.state_manager import State, StateManager

    class Alpha(State):
        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, input_state: InputState) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    class Beta(State):
        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, input_state: InputState) -> None:
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


def test_state_manager_passes_held_actions_to_update(monkeypatch) -> None:
    import pygame as pg

    from my_game.core.input_manager import AXIS_MAX_VALUE, InputEvent
    from my_game.core.state_manager import State, StateManager

    class Action(Enum):
        MOVE = 1
        ANALOG_MOVE = 2

    class TestState(State):
        def __init__(self) -> None:
            super().__init__()
            self.input_state: InputState | None = None

        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, input_state: InputState) -> None:
            self.input_state = input_state

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    input_manager = InputManager(Action)
    input_manager.bind(Action.MOVE, InputEvent.keyboard(pg.K_w))
    input_manager.bind(Action.ANALOG_MOVE, InputEvent.controller_axis(pg.CONTROLLER_AXIS_LEFTX))
    state = TestState()
    screen = pg.display.set_mode((64, 64))
    manager = StateManager(screen, {TestState: state}, TestState, input_manager, "Held input test")
    monkeypatch.setattr(
        pg.event,
        "get",
        lambda: [
            pg.event.Event(pg.KEYDOWN, key=pg.K_w),
            pg.event.Event(
                pg.CONTROLLERAXISMOTION,
                axis=pg.CONTROLLER_AXIS_LEFTX,
                value=int(0.6 * AXIS_MAX_VALUE),
                instance_id=1,
            ),
        ],
    )

    manager.handle_events()
    manager.update(1 / 60)

    assert state.input_state is not None
    assert state.input_state.held_actions == {Action.MOVE}
    assert state.input_state.get_action_strength(Action.MOVE) == 1.0
    assert state.input_state.get_action_strength(Action.ANALOG_MOVE) == pytest.approx(0.5, rel=1e-4)
