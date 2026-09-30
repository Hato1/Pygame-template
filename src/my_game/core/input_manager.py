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

    TODO: Handle controller axis motion properly, possibly with deadzone and sensitivity adjustments.
    TODO: Handle negative and positive joystick axes separately.
    """

    def __init__(self, actions: type[Enum]) -> None:
        """Initialize the InputManager with a set of actions.

        Args:
            actions (type[Enum]): The enumeration of possible actions that can be bound to inputs.
        """
        self.bindings: defaultdict[InputEvent, set[Enum]] = defaultdict(set)
        self.held_inputs: set[InputEvent] = set()

    def bind(
        self,
        action: Enum,
        input_event: InputEvent,
    ) -> None:
        """Register binding

        Args:
            action (Enum): The action to bind.
            input_event (InputEvent): The users input.
        """
        self.bindings[input_event].add(action)

    def unbind(
        self,
        input_event: InputEvent,
        action: Enum,
    ) -> None:
        """Unregister binding

        If the action was not previously bound to the input event, this method does nothing.

        Args:
            input_event (InputEvent): The input event to unbind from the action.
            action (Enum): The action to unbind.
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

    def get_bound_inputs(self, action: Enum) -> set[InputEvent]:
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

    def get_held_actions(self) -> set[Enum]:
        """Return actions bound to currently held inputs."""
        held_actions: set[Enum] = set()
        for input_event in self.held_inputs:
            held_actions.update(self.get_bound_actions(input_event))
        return held_actions

    def clear_held_controller_inputs(self) -> None:
        """Clear all held controller button and axis inputs."""
        controller_events = (InputType.CONTROLLER_BUTTON, InputType.CONTROLLER_AXIS)
        self.held_inputs = {
            input_event for input_event in self.held_inputs if input_event.input_type not in controller_events
        }

    def _update_held_input(self, input_event: InputEvent) -> None:
        if input_event.keyup:
            self.held_inputs.discard(input_event._replace(keyup=False))
        else:
            self.held_inputs.add(input_event)

    def process_pygame_event(self, event: pg.Event) -> set[Enum]:
        """Update held-button state and return actions bound to this event."""
        input_event: InputEvent | None = None

        match event.type:
            case pg.QUIT:
                raise ValueError("Quit event should not be passed to InputManager")
            case pg.WINDOWFOCUSLOST:
                self.held_inputs.clear()
            case pg.CONTROLLERDEVICEREMOVED:
                self.clear_held_controller_inputs()
            case pg.KEYDOWN | pg.KEYUP:
                input_event = InputEvent.keyboard(event.key, keyup=is_keyup(event))
                self._update_held_input(input_event)
            case pg.MOUSEBUTTONDOWN | pg.MOUSEBUTTONUP:
                input_event = InputEvent.mouse_button(event.button, keyup=is_keyup(event))
                self._update_held_input(input_event)
            case pg.CONTROLLERBUTTONDOWN | pg.CONTROLLERBUTTONUP:
                input_event = InputEvent.controller_button(event.button, keyup=is_keyup(event))
                self._update_held_input(input_event)
            case pg.CONTROLLERAXISMOTION:
                input_event = InputEvent.controller_axis(event.axis)
                self._update_held_input(input_event)
            # Mouse motion events are not considered "held" inputs, so we don't update held_inputs.
            case pg.MOUSEMOTION:
                input_event = InputEvent.mouse_motion(event.pos)

        return self.get_bound_actions(input_event) if input_event else set()
