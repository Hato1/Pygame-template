"""Run the game."""

import pygame

from pygame_me.logging import get_logger
from spatial.world import test

pygame.init()

logger = get_logger()


WHITE = (255, 255, 255)
RED = (255, 0, 0)


def main() -> None:
    """Run the game."""
    logger.debug("Debug", x=5)
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    logger.critical("Critical", bad="bad")
    test()
    resolution = (640, 640)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        rectangle = pygame.Rect(300, 0, 160, 280)
        pygame.draw.rect(screen, RED, rectangle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
