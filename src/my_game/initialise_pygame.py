import pygame as pg

# TODO: Move to a new game config file.
from my_game.constants import SCREEN_SIZE

pg.init()
# Start hidden so assets can be loaded before the window is shown.
# Additionally prevents pytest from opening a visible window.
# And it prevents window flickering on some platforms.
pg.display.set_mode(SCREEN_SIZE, pg.SCALED | pg.HIDDEN | pg.RESIZABLE)
