"""This module contains the StateManager class and a abstract State class.

TODO: Fix key manager to capture both keypress instances and key holds.
      Use pygame.key.get_pressed() for key holds and key.get_just_pressed
      and key.get_just_released alongside event.pump for instantaneous.
      Actually don't because this will miss non keyboard events.
TODO: Remove next state from TransitionData.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame as pg


@dataclass
class TransitionData:
    """Data to be passed between states during a transition."""

    previous_state: type[State] | None = None

    # Used to pass the player's score from the game state to the scoreboard state.
    score: float = 0.0


class State(ABC):
    """Abstract base class for program states.

    Attributes:
        done (bool): Set to True to leave this state and go to the next one.
        quit (bool): Set to True to exit the entire program.
        next_state (type[State] | None): Next state to go to when self.done is True.
        persist (dict[str, Any]): Dictionary of variables that should persist to the next state.
        previous_state (type[State] | None): The state that was active before this one.
        start_time (float): Time in seconds since the State started.

    Methods:
        enter(surface_rect, *, previous_state, payload):
            Initializes the state with the current time, persistent variables, and previous state.

        exit():
            Prepares persistent variables for the next state and resets the done flag.

        handle_event(event: pg.Event):
            Abstract method to process events from the main event loop.
            Must be implemented by subclasses.

        update(surface, keys, dt):
            Abstract method to update the state logic.
            Don't draw anything to the surface here.
            Must be implemented by subclasses.

        draw(surface, dt):
            Abstract method to draw the state to the given surface.
            Don't update game logic here.
            Must be implemented by subclasses.
    """

    def __init__(self):
        self.done: bool = False
        self.quit: bool = False
        self.next_state: type[State] | None = None
        self.transition_data: TransitionData = TransitionData()
        self.start_time: float = 0.0

    def enter(
        self,
        surface_rect: pg.Rect,
        transition_data: TransitionData,
    ) -> None:
        """Called when this state becomes the active state."""
        self.start_time = pg.time.get_ticks() / 1000.0

    def exit(self) -> TransitionData:
        """Called before leaving this state."""
        self.done = False
        self.transition_data.previous_state = type(self)
        return self.transition_data

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


class StateManager:
    """Responsible for managing the different states/scenes of a Pygame application.

    Methods:
        change_state(new_state: type[State]):
            Cleans up the current state and transitions to the next state, passing persistent variables.

        toggle_show_fps():
            Toggles the display of FPS in the window caption when F5 is pressed.

        handle_events():
            Processes all Pygame events and passes them to the current state. Handles global toggling of FPS display.

        update(dt: float):
            Updates the current state, checks for state changes, and manages quitting.

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

        self.current_state.enter(self.screen.get_rect(), TransitionData())

    def change_state(self, next_state: type[State] | None) -> None:
        """Exit the current state, enter the next one."""
        transition_data = self.current_state.exit()
        if not next_state:
            raise ValueError("Attempted to change state but next_state not set.")

        self.current_state = self.states[next_state]
        self.current_state.enter(
            self.screen.get_rect(),
            transition_data=transition_data,
        )

    def toggle_show_fps(self) -> None:
        """Toggle displaying the framerate in the window caption."""
        self.show_fps = not self.show_fps
        if not self.show_fps:
            pg.display.set_caption(self.caption)

    def handle_events(self) -> None:
        """Process all events and pass them down to current State.

        The f5 key globally turns on/off the display of FPS in the caption
        """
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.quit = True
                case pg.KEYDOWN:
                    self.keys = pg.key.get_pressed()
                    if event.key == pg.K_F5:
                        self.toggle_show_fps()
                case pg.KEYUP:
                    self.keys = pg.key.get_pressed()

            self.current_state.handle_event(event)

    def update(self, dt: float):
        """Checks for state change and updates the current state.

        dt: Time in seconds since last frame.
        """
        if self.current_state.quit:
            self.quit = True
            return

        if self.current_state.done:
            self.change_state(self.current_state.next_state)

        self.current_state.update(self.screen.get_rect(), self.keys, dt)
        self.current_state.draw(self.screen, dt)

    def main(self):
        """Main loop for entire program."""

        while not self.quit:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            pg.display.update()

            if self.show_fps:
                fps = self.clock.get_fps()
                pg.display.set_caption(f"{self.caption} - {fps:.2f} FPS")
