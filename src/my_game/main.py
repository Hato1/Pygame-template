"""Run the program."""

import pygame as pg

import my_game.initialise_pygame  # noqa: F401
from my_game.states.game import Game
from my_game.states.main_menu import MainMenu
from my_game.utils.state_manager import State, StateManager

ORIGINAL_CAPTION = "My Game"


def main():
    """Run the program."""

    # Initialization
    pg.init()
    screen = pg.display.get_surface()
    assert screen is not None, "Pygame display surface not initialized."
    pg.display.set_caption(ORIGINAL_CAPTION)

    # Add states to StateManager here.
    state_dict: dict[type[State], State] = {MainMenu: MainMenu(), Game: Game()}
    state_manager = StateManager(screen, state_dict, MainMenu, ORIGINAL_CAPTION)

    # Run main loop.
    state_manager.main()

    pg.quit()


if __name__ == "__main__":
    main()
