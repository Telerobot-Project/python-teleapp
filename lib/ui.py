"""UI elements for the application."""

import math
from typing import NamedTuple

import pygame

Color = tuple[int, int, int]


class Point(NamedTuple):
    """A point on the screen with x and y coordinates."""

    x: int
    y: int


class Rectangle(NamedTuple):
    """A rectangle/bounding box for a UI element."""

    x: int
    y: int
    width: int
    height: int


class Mouse:
    """Mouse pointer state."""

    def __init__(self) -> None:
        """Initialize the mouse state."""
        self.pos = (0, 0)
        self.clicked = False
        self.scroll = 0

    def read(self) -> None:
        """Get the mouse data from pygame and update the instance attributes."""
        self.pos = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()[0]
        self.scroll = pygame.mouse.get_rel()[1]

    def get_distance(self, x: int, y: int) -> float:
        """Get the distance from the mouse pointer to (x, y)."""
        return math.sqrt((self.pos[0] - x) ** 2 + (self.pos[1] - y) ** 2)

    def get_angle(self, x: int, y: int) -> float:
        """Get the angle of the line from mouse pointer to (x, y)."""
        return math.degrees(math.atan2(self.pos[0] - x, y - self.pos[1]))

    def is_in_rect(self, rect: Rectangle) -> bool:
        """Check whether the mouse pointer is inside of a given rectangle."""
        return (
            self.pos[0] > rect.x
            and self.pos[0] < rect.x + rect.width
            and self.pos[1] > rect.y
            and self.pos[1] < rect.y + rect.height
        )

    def is_in_circle(self, x: int, y: int, radius: float) -> bool:
        """Check whether the mouse pointer is inside of a given circle."""
        return self.get_distance(x, y) < radius


class Window:
    """The main application window."""

    def __init__(self, width: int, height: int, caption: str) -> None:
        """Initialize the window."""
        self.size = (width, height)
        self.caption = caption
        self.mouse = Mouse()

        self.run = True

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.SysFont("Arial", 15)
        self.clock = pygame.time.Clock()

    def read(self) -> None:
        """Check the event queue for quit event and update the mouse state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()

        self.mouse.read()

    def update(self) -> None:
        """Refresh the contents of the pygame window."""
        self.clock.tick(20)
        pygame.display.update()

    def fill(self, color: Color) -> None:
        """Fill the window with a solid color."""
        self.screen.fill(color)


class JoysticSize(NamedTuple):
    """Inner and outer radius of the joystick."""

    inner: float
    outer: float


class Joystick:
    """A joystick for controlling the robot."""

    def __init__(
        self,
        position: Point,
        sizes: JoysticSize,
        color: Color,
        window: Window,
    ) -> None:
        """Create a joystick for controlling the robot."""
        self.position = position
        self.inner_radius, self.outer_radius = sizes
        self.color = color
        self.window: Window = window
        self.angle: float = 0
        self.distance: float = 0
        self.clicked = False

    def draw(self) -> None:
        """Draw the joystick to the screen."""
        pygame.draw.circle(
            self.window.screen,
            self.color,
            self.position,
            self.inner_radius,
            2,
        )
        pygame.draw.circle(
            self.window.screen,
            self.color,
            (
                self.position.x + self.distance * math.sin(math.radians(self.angle)),
                self.position.y - self.distance * math.cos(math.radians(self.angle)),
            ),
            self.outer_radius,
        )

    def read(self) -> None:
        """Update the state of the joystick."""
        if self.window.mouse.clicked:
            if self.window.mouse.is_in_circle(
                self.position.x,
                self.position.y,
                self.inner_radius,
            ):
                self.clicked = True

            if self.clicked:
                self.distance = self.window.mouse.get_distance(
                    self.position.x,
                    self.position.y,
                )
                self.distance = min(self.distance, self.inner_radius)
                self.angle = self.window.mouse.get_angle(
                    self.position.x,
                    self.position.y,
                )
                self.angle = (self.angle + 360) % 360
        else:
            self.distance = 0
            self.angle = 0
            self.clicked = False


class Button:
    """A button UI element."""

    def __init__(
        self,
        rect: Rectangle,
        color: Color,
        window: Window,
    ) -> None:
        """Create a button from rectangle and color."""
        self.rect = rect
        self.color = color
        self.window = window
        self.down = False

    def draw(self) -> None:
        """Draw the button to the screen."""
        pygame.draw.rect(
            self.window.screen,
            self.color,
            self.rect,
            border_radius=5,
        )

    def read(self) -> None:
        """Check if the button is clicked."""
        self.down = self.window.mouse.clicked and self.window.mouse.is_in_rect(
            self.rect,
        )
