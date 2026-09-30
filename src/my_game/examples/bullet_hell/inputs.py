"""Defines the input actions and maps them to Pygame keys for the bullet hell example game."""

from enum import Enum, auto

import pygame as pg

from my_game.core.input_manager import InputEvent, InputManager


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UI_SELECT = auto()
    UI_CANCEL = auto()
    TOGGLE_DEBUG = auto()


input_manager = InputManager(Action)

# Keyboard
input_manager.map_input_to_action(Action.UI_SELECT, InputEvent.keyboard(pg.K_RETURN))
input_manager.map_input_to_action(Action.UI_SELECT, InputEvent.keyboard(pg.K_SPACE))
input_manager.map_input_to_action(Action.UI_CANCEL, InputEvent.keyboard(pg.K_ESCAPE))
input_manager.map_input_to_action(Action.TOGGLE_DEBUG, InputEvent.keyboard(pg.K_F1))
input_manager.map_input_to_action(Action.UP, InputEvent.keyboard(pg.K_w))
input_manager.map_input_to_action(Action.UP, InputEvent.keyboard(pg.K_UP))
input_manager.map_input_to_action(Action.DOWN, InputEvent.keyboard(pg.K_s))
input_manager.map_input_to_action(Action.DOWN, InputEvent.keyboard(pg.K_DOWN))
input_manager.map_input_to_action(Action.LEFT, InputEvent.keyboard(pg.K_a))
input_manager.map_input_to_action(Action.LEFT, InputEvent.keyboard(pg.K_LEFT))
input_manager.map_input_to_action(Action.RIGHT, InputEvent.keyboard(pg.K_d))
input_manager.map_input_to_action(Action.RIGHT, InputEvent.keyboard(pg.K_RIGHT))

# Controller
input_manager.map_input_to_action(Action.UI_SELECT, InputEvent.controller_button(pg.CONTROLLER_BUTTON_A))
input_manager.map_input_to_action(Action.UI_CANCEL, InputEvent.controller_button(pg.CONTROLLER_BUTTON_B))
input_manager.map_input_to_action(Action.UP, InputEvent.controller_button(pg.CONTROLLER_BUTTON_DPAD_UP))
input_manager.map_input_to_action(Action.DOWN, InputEvent.controller_button(pg.CONTROLLER_BUTTON_DPAD_DOWN))
input_manager.map_input_to_action(Action.LEFT, InputEvent.controller_button(pg.CONTROLLER_BUTTON_DPAD_LEFT))
input_manager.map_input_to_action(Action.RIGHT, InputEvent.controller_button(pg.CONTROLLER_BUTTON_DPAD_RIGHT))
