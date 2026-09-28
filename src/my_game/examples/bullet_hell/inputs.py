"""Defines the input actions and maps them to Pygame keys for the bullet hell example game."""

from enum import Enum, auto

import pygame as pg

from my_game.core.input_manager import ControllerButtonBinding, InputManager, KeyboardBinding


class InputAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UI_SELECT = auto()
    UI_CANCEL = auto()
    TOGGLE_DEBUG = auto()


input_manager = InputManager(InputAction)

# Keyboard
input_manager.map_action_to_key(InputAction.UI_SELECT, KeyboardBinding(pg.K_RETURN))
input_manager.map_action_to_key(InputAction.UI_SELECT, KeyboardBinding(pg.K_SPACE))
input_manager.map_action_to_key(InputAction.UI_CANCEL, KeyboardBinding(pg.K_ESCAPE))
input_manager.map_action_to_key(InputAction.TOGGLE_DEBUG, KeyboardBinding(pg.K_F1))
input_manager.map_action_to_key(InputAction.UP, KeyboardBinding(pg.K_w))
input_manager.map_action_to_key(InputAction.DOWN, KeyboardBinding(pg.K_s))
input_manager.map_action_to_key(InputAction.LEFT, KeyboardBinding(pg.K_a))
input_manager.map_action_to_key(InputAction.RIGHT, KeyboardBinding(pg.K_d))

# Controller
input_manager.map_action_to_key(InputAction.UI_SELECT, ControllerButtonBinding(pg.CONTROLLER_BUTTON_A))
input_manager.map_action_to_key(InputAction.UI_CANCEL, ControllerButtonBinding(pg.CONTROLLER_BUTTON_B))
input_manager.map_action_to_key(InputAction.UP, ControllerButtonBinding(pg.CONTROLLER_BUTTON_DPAD_UP))
input_manager.map_action_to_key(InputAction.DOWN, ControllerButtonBinding(pg.CONTROLLER_BUTTON_DPAD_DOWN))
input_manager.map_action_to_key(InputAction.LEFT, ControllerButtonBinding(pg.CONTROLLER_BUTTON_DPAD_LEFT))
input_manager.map_action_to_key(InputAction.RIGHT, ControllerButtonBinding(pg.CONTROLLER_BUTTON_DPAD_RIGHT))
