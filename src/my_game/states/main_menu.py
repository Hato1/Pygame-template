import pygame as pg

from my_game.states import game
from my_game.utils.state_manager import State


class MainMenu(State):
    def __init__(self) -> None:
        super().__init__()

    def handle_event(self, event: pg.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                # assign the class object from the module alias to avoid
                # circular-import issues that arise from `from ... import ...`
                # and to keep the reference short.
                self.next_state = game.Game

    def update(self, surface_rect: pg.Rect, keys, dt: float) -> None:
        pass

    def draw(self, surface: pg.Surface, dt: float) -> None:
        surface.fill(pg.Color("blue"))
