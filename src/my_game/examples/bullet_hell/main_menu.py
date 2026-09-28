from enum import Enum
from typing import Any

import pygame as pg

from my_game.core.asset_manager import Fonts
from my_game.core.state_manager import State
from my_game.examples.bullet_hell import game
from my_game.examples.bullet_hell.inputs import Action


class MainMenu(State):
    FONT = Fonts.PICO8.load(6)

    def __init__(self) -> None:
        super().__init__()

    def handle_event(self, actions: set[Enum], data: dict[str, Any]) -> None:
        if Action.UI_SELECT in actions:
            self.done = True
            self.next_state = game.Game

    def update(self, surface_rect: pg.Rect, dt: float) -> None:
        pass

    def draw(self, surface: pg.Surface, dt: float) -> None:
        surface.fill(pg.Color("gray20"))

        text = "press enter to start"
        anti_alias = True
        text_surface = self.FONT.render(text, anti_alias, pg.Color("yellow"))
        text_rect = text_surface.get_rect(center=(surface.get_rect().center))
        surface.blit(text_surface, text_rect)
