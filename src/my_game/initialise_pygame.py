import pygame as pg
from pygame._sdl2 import controller as pg_controller

from my_game.constants import SCREEN_SIZE

pg.init()
# pg.init() doesn't start the controller subsystem; without it no CONTROLLERDEVICEADDED events are sent.
pg_controller.init()
# Start hidden so assets can be loaded before the window is shown.
# And it prevents window flickering on some platforms.
pg.display.set_mode(SCREEN_SIZE, pg.SCALED | pg.HIDDEN | pg.RESIZABLE)
