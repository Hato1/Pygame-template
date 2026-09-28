"""Manages input mappings for the game.

Pygame key constants can be found here:
https://pyga.me/docs/ref/key.html
Pygame event types can be found here:
https://pyga.me/docs/ref/event.html
"""

from collections import defaultdict
from enum import Enum, StrEnum
from typing import Any, NamedTuple

import pygame as pg


class InputType(StrEnum):
    KEYBOARD = "keyboard"
    MOUSE_BUTTON = "mouse_button"
    MOUSE_MOTION = "mouse_motion"
    CONTROLLER_BUTTON = "controller_button"
    CONTROLLER_AXIS = "controller_axis"


class InputEvent(NamedTuple):
    """_summary_

    value (Any): The key, button, or axis value to map the action to.
    input_type (str): The kind of input, such as keyboard or controller_button.
    keyup (bool): Bind to keyup instead of keydown.

    Inputs that don't toggle such as mouse motion or joystick
    axis should always be mapped to keydown.
    """

    value: Any
    input_type: InputType
    keyup: bool = False

    @classmethod
    def for_keyboard(cls, value: Any, *, keyup: bool = False):
        return cls(value, InputType.KEYBOARD, keyup)

    @classmethod
    def for_mouse_button(cls, value: Any, *, keyup: bool = False):
        return cls(value, InputType.MOUSE_BUTTON, keyup)

    @classmethod
    def for_mouse_motion(cls, value: Any):
        return cls(value, InputType.MOUSE_MOTION, keyup=False)

    @classmethod
    def for_controller_button(cls, value: Any, *, keyup: bool = False):
        return cls(value, InputType.CONTROLLER_BUTTON, keyup)

    @classmethod
    def for_controller_axis(cls, value: Any):
        return cls(value, InputType.CONTROLLER_AXIS, keyup=False)


KeyboardBinding = InputEvent.for_keyboard
MouseBinding = InputEvent.for_mouse_button
MouseMotionBinding = InputEvent.for_mouse_motion
ControllerButtonBinding = InputEvent.for_controller_button
ControllerAxisBinding = InputEvent.for_controller_axis


def is_keyup(event: pg.Event):
    return event.type in [pg.KEYUP, pg.CONTROLLERBUTTONUP, pg.MOUSEBUTTONUP]


class InputManager:
    """Maps actions to Pygame inputs.

    TODO: Add support for held keys.
    TODO: Add support for unbinding keys.
    TODO: Add support to bind positive and negative actions to joystick axes.
    """

    def __init__(self, actions: type[Enum]) -> None:
        self._input_to_action: defaultdict[InputEvent, set[Enum]] = defaultdict(set)

    def map_action_to_key(
        self,
        action: Enum,
        input_event: InputEvent,
    ) -> None:
        """Register binding

        Args:
            action (Enum): The action to bind.
            input_event: The users input.
        """
        self._input_to_action[input_event].add(action)

    def get_bound_actions(
        self,
        input_event: InputEvent,
    ) -> set[Enum]:
        """Returns actions associated with binding.

        Returns:
            set[Enum]: Associated actions.
        """
        return self._input_to_action.get(input_event, set())

    def get_bound_actions_for_pygame_event(self, event: pg.Event) -> tuple[set[Enum], dict[str, Any]]:
        """Returns the Actions corresponding to the given Pygame event.

        Args:
            event (pg.Event): Pygame event.

        Returns:
            tuple[set[Enum], dict[str, Any]]: Bound actions and normalized event data.
        """
        if event.type == pg.QUIT:
            raise ValueError("Quit event should not be passed to InputManager.")
        if event.type in (pg.KEYDOWN, pg.KEYUP):
            input_event, data = self._normalize_keyboard_event(event)
        elif event.type in (pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEWHEEL):
            input_event, data = self._normalize_mouse_event(event)
        elif event.type in (pg.CONTROLLERAXISMOTION, pg.CONTROLLERBUTTONDOWN, pg.CONTROLLERBUTTONUP):
            input_event, data = self._normalize_controller_event(event)
        else:
            print(f"Unhandled event type: {event.type}")
            return set(), {}

        actions = self.get_bound_actions(input_event)

        return actions, data

    @staticmethod
    def _normalize_keyboard_event(event: pg.Event) -> tuple[InputEvent, dict[str, Any]]:
        data = {"input": event.key}
        return KeyboardBinding(event.key, keyup=is_keyup(event)), data

    @staticmethod
    def _normalize_mouse_event(event: pg.Event) -> tuple[InputEvent, dict[str, Any]]:
        match event.type:
            case pg.MOUSEMOTION:
                data = {"input": "mouse_motion", "pos": event.pos, "rel": event.rel, "buttons": event.buttons}
                return MouseMotionBinding(event.pos), data
            case pg.MOUSEBUTTONDOWN | pg.MOUSEBUTTONUP:
                data = {"input": event.button, "pos": event.pos}
                return MouseBinding(event.button, keyup=is_keyup(event)), data
            case pg.MOUSEWHEEL:
                raise NotImplementedError("Mouse wheel events not yet implemented.")
        raise ValueError(f"Unsupported mouse event type: {event.type}")

    @staticmethod
    def _normalize_controller_event(event: pg.Event) -> tuple[InputEvent, dict[str, Any]]:
        match event.type:
            case pg.CONTROLLERAXISMOTION:
                data = {"input": f"joy_axis_{event.axis}", "axis": event.axis, "value": event.value}
                return ControllerAxisBinding(event.axis), data
            case pg.CONTROLLERBUTTONDOWN | pg.CONTROLLERBUTTONUP:
                data = {"input": event.button, "instance_id": event.instance_id}
                return ControllerButtonBinding(event.button, keyup=is_keyup(event)), data
        raise ValueError(f"Unsupported joystick event type: {event.type}")

    def get_binding(self, action: Enum) -> set[InputEvent]:
        """Returns input kind, value, and pressed/released direction for an action.

        This is useful for displaying mapped keys when rebinding controls.

        Args:
            action (Enum): The action to look up.

        Returns:
            set[InputEvent]: Corresponding inputs.
        """
        keys = set()
        for key, actions in self._input_to_action.items():
            if action in actions:
                keys.add(key)
        return keys
