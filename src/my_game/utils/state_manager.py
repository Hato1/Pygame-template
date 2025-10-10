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
        self.state_dict: dict[type[State], State] = states
        self.state: State = self.state_dict[starting_state]
        self.caption: str = caption  # Caption for the window.

        self.quit: bool = False  # Set to True to exit program.
        self.clock: pg.Clock = pg.time.Clock()
        self.current_time: float = 0.0  # Current time in seconds since program launched.
        self.fps: float = 60.0  # Used to limit the framerate.
        self.show_fps: bool = True  # Display the framerate in the caption.
        self.keys = pg.key.get_pressed()  # Current state of all keyboard buttons.

    def event_loop(self):
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
            self.state.get_event(event)

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
        self.current_time = pg.time.get_ticks() / 1000.0
        if self.state.quit:
            self.quit = True
        elif self.state.done:
            self.change_state()
        self.state.update(self.screen, self.keys, self.current_time, dt)

    def change_state(self):
        """Cleanup the current state, switch to and startup the next state."""
        previous, next = type(self.state), self.state.next
        if next is None:
            raise ValueError("Next state not set")

        persistant_variables = self.state.cleanup()
        self.state = self.state_dict[next]
        self.state.startup(self.current_time, persistant_variables, previous)

    def main(self):
        """Main loop for entire program."""

        while not self.quit:
            time_delta = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
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
            Must be implemented by subclasses.
    """

    def __init__(self):
        # Time in seconds since the State started.
        self.start_time: float = 0.0
        # Current time in seconds since the program launched.
        self.current_time: float = 0.0
        # Exit the entire program.
        self.quit: bool = False
        # Leave this state and go to the next one.
        self.done: bool = False
        # Next state to go to when self.done is True.
        self.next: type[State] | None = None
        # The state that was active before this one.
        self.previous: type[State] | None = None
        # Dictionary of variables that should persist to the next state.
        self.persist: dict[str, Any] = {}

    @abstractmethod
    def get_event(self, event: pg.Event):
        """Processes events that were passed from the main event loop."""
        pass

    def startup(self, current_time: float, persistant: dict[str, Any], previous: type[State]):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = current_time
        self.previous = previous

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        self.done = False
        return self.persist

    @abstractmethod
    def update(self, surface: pg.Surface, keys, current_time: float, dt: float):
        """Update function for state. Must be overloaded in children.

        surface: The surface to draw to.
        keys: The current state of all keyboard buttons.
        current_time: Current time in seconds since program launched.
        dt: Time in seconds since last frame.
        """
        pass
