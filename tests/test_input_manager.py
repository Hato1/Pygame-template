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
    manager.bind(Action.MOUSE_CLICK, InputEvent.mouse_button(1))
    manager.bind(Action.JOYSTICK_CLICK, InputEvent.controller_button(1))

    mouse_actions = manager.process_pygame_event(pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(10, 20)))
    controller_actions = manager.process_pygame_event(pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=1, instance_id=7))

    assert mouse_actions == {Action.MOUSE_CLICK}
    assert controller_actions == {Action.JOYSTICK_CLICK}


def test_controller_button_event_resolves_controller_binding() -> None:
    manager = InputManager(Action)
    manager.bind(
        Action.SELECT,
        InputEvent.controller_button(pg.CONTROLLER_BUTTON_A),
    )

    actions = manager.process_pygame_event(
        pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=pg.CONTROLLER_BUTTON_A, instance_id=4)
    )

    assert actions == {Action.SELECT}


def test_get_binding_returns_structured_input_identity() -> None:
    manager = InputManager(Action)
    manager.bind(Action.SELECT, InputEvent.keyboard(pg.K_RETURN))
    manager.bind(
        Action.SELECT,
        InputEvent.controller_button(pg.CONTROLLER_BUTTON_A),
    )

    keyup = False
    assert manager.get_bound_inputs(Action.SELECT) == {
        (pg.K_RETURN, InputType.KEYBOARD, keyup),
        (pg.CONTROLLER_BUTTON_A, InputType.CONTROLLER_BUTTON, keyup),
    }


def test_held_actions_follow_button_down_and_up_events() -> None:
    manager = InputManager(Action)
    manager.bind(Action.SELECT, InputEvent.keyboard(pg.K_RETURN))
    manager.bind(Action.MOUSE_CLICK, InputEvent.mouse_button(1))
    manager.bind(Action.JOYSTICK_CLICK, InputEvent.controller_button(1))

    manager.process_pygame_event(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
    manager.process_pygame_event(pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))
    manager.process_pygame_event(pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=1, instance_id=3))
    assert manager.get_held_actions() == {Action.SELECT, Action.MOUSE_CLICK, Action.JOYSTICK_CLICK}

    manager.process_pygame_event(pg.event.Event(pg.KEYUP, key=pg.K_RETURN))
    assert manager.get_held_actions() == {Action.MOUSE_CLICK, Action.JOYSTICK_CLICK}

    manager.process_pygame_event(pg.event.Event(pg.MOUSEBUTTONUP, button=1, pos=(0, 0)))
    manager.process_pygame_event(pg.event.Event(pg.CONTROLLERBUTTONUP, button=1, instance_id=3))
    assert manager.get_held_actions() == set()


def test_non_button_inputs_are_not_held_and_focus_loss_clears_held_inputs() -> None:
    manager = InputManager(Action)
    manager.bind(Action.SELECT, InputEvent.keyboard(pg.K_RETURN))

    manager.process_pygame_event(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
    manager.process_pygame_event(pg.event.Event(pg.MOUSEMOTION, pos=(10, 20), rel=(1, 1), buttons=(0, 0, 0)))
    manager.process_pygame_event(pg.event.Event(pg.CONTROLLERAXISMOTION, axis=0, value=10000, instance_id=3))
    assert manager.get_held_actions() == {Action.SELECT}

    manager.process_pygame_event(pg.event.Event(pg.WINDOWFOCUSLOST))
    assert manager.get_held_actions() == set()


def test_controller_removal_clears_held_controller_buttons_only() -> None:
    manager = InputManager(Action)
    manager.bind(Action.SELECT, InputEvent.keyboard(pg.K_RETURN))
    manager.bind(Action.JOYSTICK_CLICK, InputEvent.controller_button(1))
    manager.process_pygame_event(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
    manager.process_pygame_event(pg.event.Event(pg.CONTROLLERBUTTONDOWN, button=1, instance_id=3))

    manager.process_pygame_event(pg.event.Event(pg.CONTROLLERDEVICEREMOVED, instance_id=3))

    assert manager.get_held_actions() == {Action.SELECT}
