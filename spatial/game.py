"""Run the game."""

import pygame

pygame.init()


WHITE = (255, 255, 255)
RED = (255, 0, 0)


def main() -> None:
    """Run the game."""
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
