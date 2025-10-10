import pygame as pg

from my_game.utils.state_manager import State


class Game(State):
    def __init__(self):
        super().__init__()

    def get_event(self, event: pg.Event):
        pass

    def update(self, surface, keys, current_time, dt):
        surface.fill(pg.Color("red"))
