import pygame as pg

import my_game.states.game as game
from my_game.utils.state_manager import State


class MainMenu(State):
    def __init__(self):
        super().__init__()

    def get_event(self, event: pg.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                # assign the class object from the module alias to avoid
                # circular-import issues that arise from `from ... import ...`
                # and to keep the reference short.
                self.next = game.Game

    def update(self, surface, keys, current_time, dt):
        pass

    def draw(self, surface, keys, current_time, dt):
        surface.fill(pg.Color("blue"))
