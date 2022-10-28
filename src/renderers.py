from dataclasses import dataclass
from itertools import cycle, islice
from typing import Protocol

import pygame

from consts import BLACK, PALETTE, WHITE
from pendulum import DoublePendulum


class Renderer(Protocol):
    def render(self):
        ...


@dataclass
class PendulumStyle:
    trail_color: str = WHITE
    trail_width: str = 2
    l1_color: str = WHITE
    l2_color: str = WHITE
    m1_color: str = WHITE
    m2_color: str = WHITE
    l1_width: float = 5
    l2_width: float = 5
    m1_radius: float = 5
    m2_radius: float = 5


@dataclass
class DisplayFlags:
    show_limbs: bool = True
    show_masses: bool = True


class PendulumsRenderer:
    def __init__(
        self,
        pendulums: list[DoublePendulum],
        screen: pygame.Surface,
        styles: list[PendulumStyle] | None,
        flags: DisplayFlags | None,
        drawing_anchor: pygame.Vector2,
    ):
        self.pendulums = pendulums
        self.screen = screen

        colors = cycle(PALETTE)
        self.styles = styles or [
            PendulumStyle(c) for _, c in zip(range(len(pendulums)), colors)
        ]
        self.flags = flags or DisplayFlags()
        self.anchor = drawing_anchor

    def render(self):
        for p, s in zip(self.pendulums, self.styles):
            self.draw_pendulum(p, s)
            self.draw_trail(p.trail, s)

    def draw_pendulum(self, p: DoublePendulum, s: PendulumStyle):
        v1 = pygame.Vector2(p.x1, -p.y1) + self.anchor
        v2 = pygame.Vector2(p.x2, -p.y2) + self.anchor

        if self.flags.show_limbs:
            pygame.draw.line(self.screen, s.l1_color, self.anchor, v1, s.l1_width)
            pygame.draw.line(self.screen, s.l2_color, v1, v2, s.l2_width)

        if self.flags.show_masses:
            pygame.draw.circle(self.screen, s.m1_color, v1, s.m1_radius)
            pygame.draw.circle(self.screen, s.m2_color, v2, s.m2_radius)

    def draw_trail(self, trail: list[tuple[float, float]], s: PendulumStyle):

        trail_length = len(trail)

        if trail_length < 2:
            return

        vtrail = [pygame.Vector2(x, -y) for x, y in trail]

        lines = (islice(vtrail, None, trail_length - 1), islice(vtrail, 1, None))
        for sp, ep in zip(*lines):
            start = sp + self.anchor
            end = ep + self.anchor
            pygame.draw.line(self.screen, s.trail_color, start, end, s.trail_width)

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.flags.show_masses = not self.flags.show_masses

            if event.key == pygame.K_l:
                self.flags.show_limbs = not self.flags.show_limbs


class FPSTrackerRenderer:
    FONT_FAMILY = "Verdana"
    FONT_SIZE_FACTOR = 100
    X_FACTOR = 0.8
    Y_FACTOR = 0.1

    def __init__(self, screen: pygame.Surface):

        self.screen = screen
        self.clock = pygame.time.Clock()

        self._reset_dimensions(screen.get_size())

    def _reset_dimensions(self, screen_size: tuple[int, int]):
        w, h = screen_size
        self.font = pygame.font.SysFont(self.FONT_FAMILY, w // self.FONT_SIZE_FACTOR)
        self.position = (w * self.X_FACTOR, h * self.Y_FACTOR)

    @property
    def fps(self) -> str:
        return str(round(self.clock.get_fps()))

    @property
    def text(self) -> str:
        return f"FPS: {self.fps}"

    def render(self):
        self.clock.tick()
        self.text_surface = self.font.render(self.text, True, WHITE)
        self.screen.blit(self.text_surface, self.position)


class SimulationRenderer:
    def __init__(self, screen: pygame.Surface, renderers: list[Renderer]):
        self.screen = screen
        self.renderers = renderers

    def render(self):
        self.screen.fill(BLACK)
        for renderer in self.renderers:
            renderer.render()
        pygame.display.flip()
