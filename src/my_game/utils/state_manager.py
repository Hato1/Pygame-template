"""
This module contains the fundamental StateManager class and a prototype class
for States.  Also contained here are resource loading functions.

TODO: Fix state specifier.
TODO: Fix key manager to capture both keypress instances and key holds.
      Use pygame.key.get_pressed() for key holds and key.get_just_pressed
      and key.get_just_released alongside event.pump for instantaneous.
      Actually don't because this will miss non keyboard events.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pygame as pg


class StateManager:
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""

    def __init__(self, screen: pg.Surface, states: dict[type[State], State], starting_state: type[State], caption: str):
        """Initialize the StateManager with a dictionary of states and the starting state."""

        self.screen: pg.Surface = screen
        self.state_dict: dict[type[State], State] = states
        self.state: State = self.state_dict[starting_state]
        self.caption: str = caption  # Caption for the window.

        self.quit: bool = False  # Set to True to exit program.
        self.clock: pg.Clock = pg.time.Clock()
        self.fps: float = 60.0  # Used to limit the framerate.
        self.show_fps: bool = True  # Display the framerate in the caption.
        self.current_time: float = 0.0  # Current time in seconds since program launched.
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
    """This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States."""

    def __init__(self):
        # Time in seconds since the State started.
        self.start_time: float = 0.0
        # Current time in seconds since the program launched.
        self.current_time: float = 0.0
        # Set to True to leave this state and go to the next one.
        self.done: bool = False
        # Set to True to exit the entire program.
        self.quit: bool = False
        # Next state to go to when self.done is True.
        self.next: type[State] | None = None
        # The state that was active before this one.
        self.previous: type[State] | None = None
        # Dictionary of variables that should persist to the next state.
        self.persist: dict[str, Any] = {}

    @abstractmethod
    def get_event(self, event: pg.Event):
        """Processes events that were passed from the main event loop.

        Must be overloaded in children.
        """
        pass

    def startup(self, current_time, persistant, previous: type[State]):
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
    def update(self, surface, keys, current_time, dt):
        """Update function for state. Must be overloaded in children."""
        pass

    def render_font(
        self, font: pg.Font, msg, color: pg.typing.ColorLike, center: pg.Vector2
    ) -> tuple[pg.Surface, pg.Rect]:
        """Returns the rendered font surface and its rect centered on center.

        TODO: Move to seperate utility module?
        """
        msg = font.render(msg, True, color)
        rect = msg.get_rect(center=center)
        return msg, rect
