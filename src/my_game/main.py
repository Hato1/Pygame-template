"""Run the program."""

import pygame as pg

import my_game.initialise_pygame  # noqa: F401
from my_game.constants import DEFAULT_CAPTION, SCREEN_SIZE
from my_game.core.state_manager import StateManager
from my_game.examples.bullet_hell import registry as bullet_hell


def main():
    """Run the program."""

    # Initialization
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
    assert screen is not None, "Pygame display surface not initialized."
    pg.display.set_caption(DEFAULT_CAPTION)

    state_manager = StateManager(
        screen,
        bullet_hell.STATE_REGISTRY,
        bullet_hell.input_manager,
        DEFAULT_CAPTION,
    )

    # Run main loop.
    state_manager.main()

    pg.quit()


if __name__ == "__main__":
    main()
