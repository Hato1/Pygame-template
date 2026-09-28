from enum import Enum, auto

import pygame as pg

from my_game.core.input_manager import (
    InputEvent,
    InputManager,
    InputType,
)


class Action(Enum):
    SELECT = auto()
    MOUSE_CLICK = auto()
    JOYSTICK_CLICK = auto()


def test_mouse_and_joystick_buttons_have_distinct_bindings() -> None:
    manager = InputManager(Action)
    manager.map_input_to_action(Action.MOUSE_CLICK, InputEvent.mouse_button(1))
    manager.map_input_to_action(Action.JOYSTICK_CLICK, InputEvent.controller_button(1))

    mouse_actions, _ = manager.get_bound_actions_for_pygame_event(
        pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(10, 20))
    )
    joystick_actions, joystick_data = manager.get_bound_actions_for_pygame_event(
        pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=1, instance_id=7)
    )

    assert mouse_actions == {Action.MOUSE_CLICK}
    assert joystick_actions == {Action.JOYSTICK_CLICK}
    assert joystick_data["instance_id"] == 7


def test_controller_button_event_resolves_controller_binding() -> None:
    manager = InputManager(Action)
    manager.map_input_to_action(
        Action.SELECT,
        InputEvent.controller_button(pg.CONTROLLER_BUTTON_A),
    )

    actions, data = manager.get_bound_actions_for_pygame_event(
        pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=pg.CONTROLLER_BUTTON_A, instance_id=4)
    )

    assert actions == {Action.SELECT}
    assert data == {"input": pg.CONTROLLER_BUTTON_A, "instance_id": 4}


def test_get_binding_returns_structured_input_identity() -> None:
    manager = InputManager(Action)
    manager.map_input_to_action(Action.SELECT, InputEvent.keyboard(pg.K_RETURN))
    manager.map_input_to_action(
        Action.SELECT,
        InputEvent.controller_button(pg.CONTROLLER_BUTTON_A),
    )

    keyup = False
    assert manager.get_binding(Action.SELECT) == {
        (pg.K_RETURN, InputType.KEYBOARD, keyup),
        (pg.CONTROLLER_BUTTON_A, InputType.CONTROLLER_BUTTON, keyup),
    }
