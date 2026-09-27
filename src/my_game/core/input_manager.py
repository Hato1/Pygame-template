"""Manages input mappings for the game.

Pygame key constants can be found here:
https://pyga.me/docs/ref/key.html
Pygame event types can be found here:
https://pyga.me/docs/ref/event.html
"""

from collections import defaultdict
from enum import Enum
from typing import Any

import pygame as pg


def format_key_name(key: Any, *, keydown: bool) -> str:
    """Formats a key name for use in the InputManager.

    Args:
        key (Any): Pygame key constant.
        keydown (bool): Whether the key is for a keydown or keyup event.

    Returns:
        str: Formatted key name.
    """
    return f"{key}_{'keydown' if keydown else 'keyup'}"


class InputManager:
    """Maps actions to Pygame keys.

    TODO: Add support for held keys.
    TODO: Add support for unbinding keys.
    TODO: Add support to bind positive and negative actions to joystick axes.
    """

    KEYDOWN = "keydown"
    KEYUP = "keyup"

    def __init__(self, actions: type[Enum]) -> None:
        self._key_to_action: defaultdict[Any, set[Enum]] = defaultdict(set)

    def map_action_to_key(self, action: Enum, key: Any, *, keydown: bool = True) -> None:
        """Maps an action to a Pygame key constant.

        Inputs that don't toggle such as mouse motion or joystick axis motion should always be mapped to keydown.

        Args:
            action (Enum): The action to map.
            key (int): The Pygame key constant to map the action to.
            keydown (bool): Whether a button/key should be mapped for keydown or keyup events.
        """
        key_name = format_key_name(key, keydown=keydown)
        self._key_to_action[key_name].add(action)

    def get_bound_actions(self, key: Any, *, keydown: bool = True) -> set[Enum]:
        """Returns the Enum corresponding to the given Pygame key constant.

        Args:
            key (int): Pygame key constant.
            keydown (bool): Whether to look for keydown or keyup events.

        Returns:
            set[Enum]: Corresponding Enums or empty set if not found.
        """
        key_name = format_key_name(key, keydown=keydown)
        return self._key_to_action.get(key_name) or set()

    def get_bound_actions_for_pygame_event(self, event: pg.Event) -> tuple[set[Enum], dict]:  # noqa: C901
        """Returns the Enum corresponding to the given Pygame event.

        Args:
            event (pg.Event): Pygame event.

        Returns:
            set[Enum]: Corresponding Enums or empty set if not found.
        """
        data = {}
        keydown = True

        match event.type:
            case pg.QUIT:
                raise ValueError("Quit event should not be passed to InputManager.")
            case pg.KEYDOWN:
                data["input"] = event.key
            case pg.KEYUP:
                data["input"] = event.key
                keydown = False
            case pg.MOUSEMOTION:
                data["input"] = "mouse_motion"
                data["pos"] = event.pos
                data["rel"] = event.rel
                data["buttons"] = event.buttons
            case pg.MOUSEBUTTONDOWN:
                data["input"] = event.button
                data["pos"] = event.pos
            case pg.MOUSEBUTTONUP:
                data["input"] = event.button
                data["pos"] = event.pos
                keydown = False
            case pg.MOUSEWHEEL:
                raise NotImplementedError("Mouse wheel events not yet implemented.")
            case pg.JOYAXISMOTION:
                data["input"] = f"joy_axis_{event.axis}"
                data["axis"] = event.axis
                data["value"] = event.value
            case pg.JOYBUTTONDOWN:
                data["input"] = event.button
                data["instance_id"] = event.instance_id
            case pg.JOYBUTTONUP:
                data["input"] = event.button
                data["instance_id"] = event.instance_id
                keydown = False
            case _:
                print(f"Unhandled event type: {event.type}")
                return set(), {}

        actions = self.get_bound_actions(data["input"], keydown=keydown)

        return actions, data

    def get_binding(self, action: Enum) -> set[int]:
        """Returns the Pygame key constants corresponding to the given Enum.

        This is useful for displaying mapped keys when rebinding controls.

        Args:
            action (Enum): The action to look up.

        Returns:
            set[int]: Corresponding Pygame key constants or empty set if not found.
        """
        keys = set()
        for key, actions in self._key_to_action.items():
            if action in actions:
                keys.add(key)
        return keys


# Handle pressed, unpressed and held keys. What about joysticks? Triggers? Mouse buttons/wheel/movement?
