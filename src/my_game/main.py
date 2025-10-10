"""Run the game."""

import pygame as pg

from my_game.states.game import Game
from my_game.states.main_menu import MainMenu
from my_game.utils.state_manager import State, StateManager

SCREEN_SIZE = (800, 600)
ORIGINAL_CAPTION = "My Game"


# Initialization
pg.init()
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)


def main():
    """Add states to StateManager here."""
    state_dict: dict[type[State], State] = {
        MainMenu : MainMenu(),
        Game      : Game()
    }
    state_manager = StateManager(state_dict, MainMenu, ORIGINAL_CAPTION)
    state_manager.main()


if __name__ == "__main__":
    main()


# import pygame

# pygame.init()


# WHITE = (255, 255, 255)
# RED = (255, 0, 0)


# def main() -> None:
#     """Run the game."""
#     resolution = (640, 640)
#     screen = pygame.display.set_mode(resolution)
#     clock = pygame.time.Clock()

#     running = True
#     while running:
#         screen.fill(WHITE)

#         rectangle = pygame.Rect(300, 0, 160, 280)
#         pygame.draw.rect(screen, RED, rectangle)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         pygame.display.flip()

#         clock.tick(60)

#     pygame.quit()


# if __name__ == "__main__":
#     main()
