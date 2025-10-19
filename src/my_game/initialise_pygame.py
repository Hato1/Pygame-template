import pygame as pg

SCREEN_SIZE = (128, 128)
ORIGINAL_CAPTION = "My Game"

pg.init()
pg.display.set_mode(SCREEN_SIZE, pg.SCALED)
pg.display.set_caption(ORIGINAL_CAPTION)
