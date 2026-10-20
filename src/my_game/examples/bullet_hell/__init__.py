"""Constants to assist with running the bullet hell example game."""

from my_game.core.state_manager import State
from my_game.examples.bullet_hell.game import Game
from my_game.examples.bullet_hell.inputs import input_manager
from my_game.examples.bullet_hell.main_menu import MainMenu
from my_game.examples.bullet_hell.scoreboard import Scoreboard

__all__ = ["INITIAL_STATE", "STATE_DICT", "input_manager"]

STATE_DICT: dict[type[State], State] = {MainMenu: MainMenu(), Game: Game(), Scoreboard: Scoreboard()}
INITIAL_STATE: type[State] = MainMenu
