import pygame as pg

# TODO: Move to a new game config file.
SCREEN_SIZE = (128, 128)

pg.init()
# Start hidden so assets can be loaded before the window is shown.
# Additionally prevents pytest from opening a visible window.
# And it prevents window flickering on some platforms.
pg.display.set_mode(SCREEN_SIZE, pg.SCALED | pg.HIDDEN | pg.RESIZABLE)
