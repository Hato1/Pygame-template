import random
from typing import Any, Self

import pygame as pg

import my_game.states.main_menu as main_menu
from my_game.utils.asset_manager import Images, UIElements
from my_game.utils.state_manager import State


def get_random_position_on_rect_perimeter(rect: pg.Rect) -> pg.Vector2:
    """Returns a random position on the perimeter of the given rect."""

    # Decide whether to pick a position on a horizontal or vertical edge.
    # This is weighted by the length of the edges to ensure uniform distribution.
    if random.random() < (rect.width / (rect.width + rect.height)):
        x = random.randrange(rect.left, rect.right)
        y = random.choice([rect.top, rect.bottom])
    else:
        x = random.choice([rect.left, rect.right])
        y = random.randrange(rect.top, rect.bottom)
    return pg.Vector2(x, y)


class Monster:
    """A simple monster class for demonstration purposes."""

    SPRITE = (
        Images.MONSTER_FRAME_0.load(),
        Images.MONSTER_FRAME_1.load(),
    )

    def __init__(self, position: pg.Vector2, direction: pg.Vector2, speed: float):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.rect = self.SPRITE[0].get_rect(center=(self.position))

    @classmethod
    def create_monster(cls, screen: pg.Surface, target: pg.Vector2) -> Self:
        """Create a monster with a default position, vector, and speed."""
        position = get_random_position_on_rect_perimeter(screen.get_rect())
        # Aim the monster towards the target position.
        vector = target - position
        speed = random.uniform(0.05, 0.5)
        return cls(position, vector, speed)

    def update(self, dt: float):
        """Update the monster's position based on its speed and direction."""
        self.position += self.direction * self.speed * dt

    def draw(self, surface: pg.Surface, current_time: float):
        # Simple animation based on time and monster speed.
        sprite_index = int((current_time * self.speed * 10) % 2)
        sprite = self.SPRITE[sprite_index]
        self.rect = sprite.get_rect(center=(self.position))
        surface.blit(sprite, self.rect)


class Player:
    """A simple player class for demonstration purposes."""

    SPRITE = Images.MONSTER_FRAME_1.load()
    INITIAL_HEALTH_CAPACITY = 3

    def __init__(self):
        self.position: pg.Vector2 = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(0, 0)
        self.max_health = self.INITIAL_HEALTH_CAPACITY
        self.health = self.max_health
        self.rect = self.SPRITE.get_rect(center=(self.position))

    def increase_velocity(self, delta: pg.Vector2):
        if not delta:
            return
        delta = pg.Vector2.normalize(delta) * 2
        self.velocity += delta

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.velocity *= 0.95  # Friction

    def draw(self, surface):
        self.rect = self.SPRITE.get_rect(center=(self.position))
        surface.blit(self.SPRITE, self.rect)


class Game(State):
    DEFAULT_MONSTER_INTERVAL = 2  # Seconds between monster spawns.
    MONSTER_INTERVAL_DECREASE_RATE = 0.02  # Rate at which monster spawn interval decreases.
    MINIMUM_MONSTER_INTERVAL = 0.1  # Minimum seconds between monster spawns.

    def __init__(self):
        super().__init__()
        self.monster_meter: float
        self.monster_interval: float
        self.monsters: list[Monster]
        self.player: Player

    def startup(self, current_time: float, persistant: dict[str, Any], previous: type[State]):
        super().startup(current_time, persistant, previous)
        self.monster_meter = 0
        self.monster_interval = self.DEFAULT_MONSTER_INTERVAL
        self.monsters = []
        self.player = Player()

    def get_event(self, event: pg.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.done = True
                # assign the class object from the module alias to avoid
                # circular-import issues that arise from `from ... import ...`
                # and to keep the reference short.
                self.next = main_menu.MainMenu

    def draw_healthbar(self, surface):
        """Draws the player's health as hearts in the top-left corner."""
        heart_full = UIElements.HEART_FULL.load()
        empty_heart = UIElements.HEART_EMPTY.load()

        for i in range(self.player.max_health):
            heart = heart_full if i < self.player.health else empty_heart
            surface.blit(heart, (5 + i * (heart.get_width() + 5), 5))

    def update_monster_spawner(self, surface, dt: float):
        """Spawns monsters over time based on the monster meter and interval."""
        self.monster_meter += dt
        while self.monster_meter > self.monster_interval:
            new_monster = Monster.create_monster(surface, self.player.position)
            self.monsters.append(new_monster)
            self.monster_meter -= self.monster_interval

    def update_player_movement(self, keys, dt: float):
        """Update player position based on input keys."""
        movement = pg.Vector2(0, 0)
        if keys[pg.K_w] or keys[pg.K_UP]:
            movement.y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            movement.y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            movement.x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            movement.x += 1
        # TODO: Controller support?
        self.player.increase_velocity(movement)
        self.player.update(dt)

    def update_difficulty(self, dt: float):
        """Gradually increase game difficulty over time."""
        self.monster_interval -= self.MONSTER_INTERVAL_DECREASE_RATE * dt
        if self.monster_interval < self.MINIMUM_MONSTER_INTERVAL:
            self.monster_interval = self.MINIMUM_MONSTER_INTERVAL

    def update(self, surface, keys, current_time, dt):
        self.update_monster_spawner(surface, dt)
        self.update_player_movement(keys, dt)

        for monster in self.monsters:
            monster.update(dt)
            if monster.rect.colliderect(self.player.rect):
                self.player.health -= 1
                self.monsters.remove(monster)

        if self.player.health <= 0:
            self.done = True
            self.next = main_menu.MainMenu

        self.update_difficulty(dt)

    def draw(self, surface: pg.Surface, keys, current_time: float, dt: float):
        surface.fill(pg.Color("gray"))
        for monster in self.monsters:
            monster.draw(surface, current_time)
        self.player.draw(surface)
        self.draw_healthbar(surface)
