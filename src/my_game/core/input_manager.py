"""Manages input mappings for the game.

Pygame key constants can be found here:
https://pyga.me/docs/ref/key.html
Pygame event types can be found here:
https://pyga.me/docs/ref/event.html
"""

from collections import defaultdict
from enum import Enum, StrEnum
from typing import NamedTuple

import pygame as pg


class InputType(StrEnum):
    KEYBOARD = "keyboard"
    MOUSE_BUTTON = "mouse_button"
    MOUSE_MOTION = "mouse_motion"
    CONTROLLER_BUTTON = "controller_button"
    CONTROLLER_AXIS = "controller_axis"


class InputEvent(NamedTuple):
    """Represents an input event that can be bound to an action.

    value (Any): A key, button, or axis id (see pygame-ce key constants).
    input_type (str): The kind of input, such as keyboard or controller_button.
    keyup (bool): Bind to keyup instead of keydown.

    Inputs that don't toggle such as mouse motion or joystick
    axis should always be mapped to keydown.
    """

    value: int
    input_type: InputType
    keyup: bool = False

    @classmethod
    def keyboard(cls, value, *, keyup: bool = False):
        return cls(value, InputType.KEYBOARD, keyup)

    @classmethod
    def mouse_button(cls, value: int, *, keyup: bool = False):
        return cls(value, InputType.MOUSE_BUTTON, keyup)

    @classmethod
    def mouse_motion(cls, value: int):
        return cls(value, InputType.MOUSE_MOTION, keyup=False)

    @classmethod
    def controller_button(cls, value: int, *, keyup: bool = False):
        return cls(value, InputType.CONTROLLER_BUTTON, keyup)

    @classmethod
    def controller_axis(cls, value: int):
        return cls(value, InputType.CONTROLLER_AXIS, keyup=False)


def is_keyup(event: pg.Event):
    return event.type in [pg.KEYUP, pg.CONTROLLERBUTTONUP, pg.MOUSEBUTTONUP]


class InputManager:
    """Maps actions to Pygame inputs.

    Attributes:
        bindings (defaultdict[InputEvent, set[Enum]]): Maps input events to sets of actions.

    TODO: Add support for held keys.
    TODO: Add support to bind positive and negative actions to joystick axes.
    """

    def __init__(self, actions: type[Enum]) -> None:
        """Initialize the InputManager with a set of actions.

        Args:
            actions (type[Enum]): The enumeration of possible actions that can be bound to inputs.
        """
        self.bindings: defaultdict[InputEvent, set[Enum]] = defaultdict(set)

    def map_input_to_action(
        self,
        action: Enum,
        input_event: InputEvent,
    ) -> None:
        """Register binding

        Args:
            action (Enum): The action to bind.
            input_event: The users input.
        """
        self.bindings[input_event].add(action)

    def unmap_input_from_action(
        self,
        action: Enum,
        input_event: InputEvent,
    ) -> None:
        """Unregister binding

        If the action was not previously bound to the input event, this method does nothing.

        Args:
            action (Enum): The action to unbind.
            input_event (InputEvent): The input event to unbind from the action.
        """
        self.bindings[input_event].discard(action)

    def get_bound_actions(
        self,
        input_event: InputEvent,
    ) -> set[Enum]:
        """Returns actions associated with binding.

        Returns:
            set[Enum]: Associated actions.
        """
        return self.bindings.get(input_event, set())

    def get_bound_actions_for_pygame_event(self, event: pg.Event) -> set[Enum]:
        """Returns the Actions corresponding to the given Pygame event.

        Args:
            event (pg.Event): Pygame event.

        Returns:
            set[Enum]: Bound actions.
        """
        if event.type == pg.QUIT:
            raise ValueError("Quit event should not be passed to InputManager")
        elif event.type in (pg.KEYDOWN, pg.KEYUP):
            input_event = self._normalize_keyboard_event(event)
        elif event.type in (pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            input_event = self._normalize_mouse_event(event)
        elif event.type in (pg.CONTROLLERAXISMOTION, pg.CONTROLLERBUTTONDOWN, pg.CONTROLLERBUTTONUP):
            input_event = self._normalize_controller_event(event)
        else:
            return set()

        actions = self.get_bound_actions(input_event)
        return actions

    @staticmethod
    def _normalize_keyboard_event(event: pg.Event) -> InputEvent:
        return InputEvent.keyboard(event.key, keyup=is_keyup(event))

    @staticmethod
    def _normalize_mouse_event(event: pg.Event) -> InputEvent:
        match event.type:
            case pg.MOUSEMOTION:
                return InputEvent.mouse_motion(event.pos)
            case pg.MOUSEBUTTONDOWN | pg.MOUSEBUTTONUP:
                return InputEvent.mouse_button(event.button, keyup=is_keyup(event))
        raise ValueError(f"Unsupported mouse event type: {event.type}")

    @staticmethod
    def _normalize_controller_event(event: pg.Event) -> InputEvent:
        match event.type:
            case pg.CONTROLLERAXISMOTION:
                return InputEvent.controller_axis(event.axis)
            case pg.CONTROLLERBUTTONDOWN | pg.CONTROLLERBUTTONUP:
                return InputEvent.controller_button(event.button, keyup=is_keyup(event))
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
        for key, actions in self.bindings.items():
            if action in actions:
                keys.add(key)
        return keys
