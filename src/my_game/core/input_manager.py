from collections import defaultdict
from enum import Enum


class InputManager:
    """Maps actions to Pygame keys."""

    def __init__(self, actions: type[Enum]) -> None:
        self._key_to_action: defaultdict[int, set[Enum]] = defaultdict(set)

    def map_action_to_key(self, action: Enum, key: int) -> None:
        """Maps an action to a Pygame key constant.

        Args:
            action (Enum): The action to map.
            key (int): The Pygame key constant to map the action to.
        """
        self._key_to_action[key].add(action)

    def get_actions(self, key: int) -> set[Enum]:
        """Returns the Enum corresponding to the given Pygame key constant.

        Args:
            key (int): Pygame key constant.

        Returns:
            set[Enum]: Corresponding Enums or empty set if not found.
        """
        return self._key_to_action.get(key) or set()

    def get_keys(self, action: Enum) -> set[int]:
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
