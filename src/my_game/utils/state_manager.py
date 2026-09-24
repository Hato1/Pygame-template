"""This module contains the StateManager class and a abstract State class.

TODO: Fix state specifier.
TODO: Fix key manager to capture both keypress instances and key holds.
      Use pygame.key.get_pressed() for key holds and key.get_just_pressed
      and key.get_just_released alongside event.pump for instantaneous.
      Actually don't because this will miss non keyboard events.
TODO: Store state dict in states/__init__.py and import here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pygame as pg


class StateManager:
    """Responsible for managing the different states/scenes of a Pygame application.

    Methods:
        event_loop():
            Processes all Pygame events and passes them to the current state. Handles global toggling of FPS display.

        toggle_show_fps(key):
            Toggles the display of FPS in the window caption when F5 is pressed.

        update(dt):
            Updates the current state, checks for state changes, and manages quitting.

        change_state():
            Cleans up the current state and transitions to the next state, passing persistent variables.

        main():
            Runs the main loop, handling events, updating states, rendering, and updating the window caption.
    """

    def __init__(self, screen: pg.Surface, states: dict[type[State], State], starting_state: type[State], caption: str):
        """Initialize the StateManager with a dictionary of states and the starting state."""

        self.screen: pg.Surface = screen
        self.states: dict[type[State], State] = states
        self.current_state: State = self.states[starting_state]
        self.caption: str = caption  # Caption for the window.

        self.quit: bool = False  # Set to True to exit program.
        self.clock: pg.Clock = pg.time.Clock()
        self.fps: float = 60.0  # Used to limit the framerate.
        self.show_fps: bool = True  # Display the framerate in the caption.
        self.keys = pg.key.get_pressed()  # Current state of all keyboard buttons.

    def change_state(self, new_state: type[State]):
        """Exit the current state, enter the next state."""
        previous_state = type(self.current_state)
        transition_data = self.current_state.exit()
        self.current_state = self.states[new_state]
        self.current_state.enter(
            self.screen.get_rect(),
            previous_state=previous_state,
            payload=transition_data,
        )

    def handle_events(self):
        """Process all events and pass them down to current State.

        The f5 key globally turns on/off the display of FPS in the caption
        """
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.quit = True
                case pg.KEYDOWN:
                    self.keys = pg.key.get_pressed()
                    self.toggle_show_fps(event.key)
                case pg.KEYUP:
                    self.keys = pg.key.get_pressed()
            self.current_state.handle_event(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def update(self, dt: float):
        """Checks for state change and updates the current state.

        dt: Time in seconds since last frame.
        """
        if self.current_state.quit:
            self.quit = True
        elif self.current_state.done:
            if (next := self.current_state.next_state) is None:
                raise ValueError("State marked done but next_state not set.")
            self.change_state(next)
        self.current_state.update(self.screen.get_rect(), self.keys, dt)
        self.current_state.draw(self.screen, dt)

    def main(self):
        """Main loop for entire program."""

        while not self.quit:
            time_delta = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(time_delta)
            pg.display.update()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = f"{self.caption} - {fps:.2f} FPS"
                pg.display.set_caption(with_fps)


class State(ABC):
    """Abstract base class for program states.

    Attributes:
        start_time (float): Time in seconds since the State started.
        current_time (float): Current time in seconds since the program launched.
        done (bool): Set to True to leave this state and go to the next one.
        quit (bool): Set to True to exit the entire program.
        next (type[State] | None): Next state to go to when self.done is True.
        previous (type[State] | None): The state that was active before this one.
        persist (dict[str, Any]): Dictionary of variables that should persist to the next state.

    Methods:
        get_event(event: pg.Event):
            Abstract method to process events from the main event loop.
            Must be implemented by subclasses.

        startup(current_time, persistant, previous: type[State]):
            Initializes the state with the current time, persistent variables, and previous state.

        cleanup():
            Prepares persistent variables for the next state and resets the done flag.

        update(surface, keys, current_time, dt):
            Abstract method to update the state logic.
            Don't draw anything to the surface here.
            Must be implemented by subclasses.

        draw(surface, keys, current_time, dt):
            Abstract method to draw the state to the given surface.
            Don't update game logic here.
            Must be implemented by subclasses.
    """

    def __init__(self):
        self.done: bool = False
        self.quit: bool = False
        self.next_state: type[State] | None = None
        self.persist: dict[str, Any] = {}

        self.previous_state: type[State] | None = None
        self.start_time: float = 0.0

    def enter(
        self,
        surface_rect: pg.Rect,
        *,
        previous_state: type[State] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Called when this state becomes the active state."""
        self.persist = payload or {}
        self.previous_state = previous_state
        self.start_time = pg.time.get_ticks() / 1000.0

    def exit(self) -> dict[str, Any]:
        """Called before leaving this state."""
        self.done = False
        return self.persist

    @abstractmethod
    def handle_event(self, event: pg.Event) -> None:
        """Handle one pygame event."""
        pass

    @abstractmethod
    def update(self, surface_rect: pg.Rect, keys, dt: float) -> None:
        """Update game state. Runs every frame.

        surface_rect: Rect representing the surface dimensions.
        keys: The current state of all keyboard buttons.
        current_time: Current time in seconds since program launched.
        dt: Time in seconds since last frame.
        """
        pass

    @abstractmethod
    def draw(self, surface: pg.Surface, dt: float):
        """Render to the given surface. Runs every frame.

        surface: The surface to draw to.
        current_time: Current time in seconds since program launched.
        dt: Time in seconds since last frame.
        """
        pass
