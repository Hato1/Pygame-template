"""Run the program."""

import pygame as pg

from my_game.states.game import Game
from my_game.states.main_menu import MainMenu
from my_game.utils.state_manager import State, StateManager

SCREEN_SIZE = (800, 600)
ORIGINAL_CAPTION = "My Game"


def main():
    """Run the program."""

    # Initialization
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(ORIGINAL_CAPTION)

    # Add states to StateManager here.
    state_dict: dict[type[State], State] = {MainMenu: MainMenu(), Game: Game()}
    state_manager = StateManager(screen, state_dict, MainMenu, ORIGINAL_CAPTION)

    # Run main loop.
    state_manager.main()

    pg.quit()


if __name__ == "__main__":
    raise ValueError("Run using `uv run my-game`")
