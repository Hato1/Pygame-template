"""Defines the input actions and maps them to Pygame keys for the bullet hell example game."""

from enum import Enum, auto

import pygame as pg

from my_game.core.input_manager import InputManager


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
input_manager.map_action_to_key(InputAction.UI_SELECT, pg.K_RETURN)
input_manager.map_action_to_key(InputAction.UI_SELECT, pg.K_SPACE)
input_manager.map_action_to_key(InputAction.UI_CANCEL, pg.K_ESCAPE)
input_manager.map_action_to_key(InputAction.TOGGLE_DEBUG, pg.K_F1)
input_manager.map_action_to_key(InputAction.UP, pg.K_w)
input_manager.map_action_to_key(InputAction.DOWN, pg.K_s)
input_manager.map_action_to_key(InputAction.LEFT, pg.K_a)
input_manager.map_action_to_key(InputAction.RIGHT, pg.K_d)

# Controller
input_manager.map_action_to_key(InputAction.UI_SELECT, pg.CONTROLLER_BUTTON_A)
input_manager.map_action_to_key(InputAction.UI_CANCEL, pg.CONTROLLER_BUTTON_B)
input_manager.map_action_to_key(InputAction.UP, pg.CONTROLLER_BUTTON_DPAD_UP)
input_manager.map_action_to_key(InputAction.DOWN, pg.CONTROLLER_BUTTON_DPAD_DOWN)
input_manager.map_action_to_key(InputAction.LEFT, pg.CONTROLLER_BUTTON_DPAD_LEFT)
input_manager.map_action_to_key(InputAction.RIGHT, pg.CONTROLLER_BUTTON_DPAD_RIGHT)
