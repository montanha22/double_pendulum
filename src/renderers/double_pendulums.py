from dataclasses import dataclass
from itertools import cycle, islice

import pygame
from src.consts import BLACK, PALETTE
from src.pendulum import DoublePendulum


@dataclass
class PendulumStyle:
    trail_color: str = BLACK
    trail_width: str = 4
    l1_color: str = BLACK
    l2_color: str = BLACK
    m1_color: str = BLACK
    m2_color: str = BLACK
    l1_width: float = 5
    l2_width: float = 5
    m1_radius: float = 5
    m2_radius: float = 5


@dataclass
class DisplayOptions:
    show_limbs: bool = True
    show_masses: bool = True


class DoublePendulumsRenderer:
    def __init__(
        self,
        pendulums: list[DoublePendulum],
        screen: pygame.Surface,
        styles: list[PendulumStyle] | None,
        flags: DisplayOptions | None,
        drawing_anchor: pygame.Vector2,
    ):
        self.pendulums = pendulums
        self.screen = screen

        colors = cycle(PALETTE)
        self.styles = styles or [PendulumStyle(c) for _, c in zip(range(len(pendulums)), colors)]
        self.flags = flags or DisplayOptions()
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
