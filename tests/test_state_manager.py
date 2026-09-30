from enum import Enum

from my_game.core.input_manager import InputManager
from my_game.core.state_manager import TransitionData


def test_state_transition_uses_explicit_enter_exit_and_payload() -> None:
    """State transitions should pass payloads through an explicit lifecycle."""
    import pygame as pg

    from my_game.core.state_manager import State, StateManager

    class Alpha(State):
        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, held_actions: set[Enum]) -> None:
            pass

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    class Beta(State):
        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, held_actions: set[Enum]) -> None:
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

    from my_game.core.input_manager import InputEvent
    from my_game.core.state_manager import State, StateManager

    class Action(Enum):
        MOVE = 1

    class TestState(State):
        def __init__(self) -> None:
            super().__init__()
            self.held_actions: set[Enum] = set()

        def handle_event(self, actions: set[Enum], event: pg.Event) -> None:
            pass

        def update(self, surface_rect: pg.Rect, dt: float, held_actions: set[Enum]) -> None:
            self.held_actions = held_actions

        def draw(self, surface: pg.Surface, dt: float) -> None:
            pass

    input_manager = InputManager(Action)
    input_manager.map_input_to_action(Action.MOVE, InputEvent.keyboard(pg.K_w))
    state = TestState()
    screen = pg.display.set_mode((64, 64))
    manager = StateManager(screen, {TestState: state}, TestState, input_manager, "Held input test")
    monkeypatch.setattr(pg.event, "get", lambda: [pg.event.Event(pg.KEYDOWN, key=pg.K_w)])

    manager.handle_events()
    manager.update(1 / 60)

    assert state.held_actions == {Action.MOVE}
