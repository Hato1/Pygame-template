import pygame as pg

import my_game.states.main_menu as main_menu
from my_game.utils.state_manager import State


class Game(State):
    def __init__(self):
        super().__init__()

    def get_event(self, event: pg.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                # assign the class object from the module alias to avoid
                # circular-import issues that arise from `from ... import ...`
                # and to keep the reference short.
                self.next = main_menu.MainMenu

    def update(self, surface, keys, current_time, dt):
        surface.fill(pg.Color("red"))
