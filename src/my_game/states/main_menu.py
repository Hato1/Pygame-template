import pygame as pg

from my_game.states.game import Game
from my_game.utils.state_manager import State


class MainMenu(State):
    def __init__(self):
        super().__init__()

    def get_event(self, event: pg.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                self.next = Game

    def update(self, surface, keys, current_time, dt):
        surface.fill(pg.Color("blue"))
