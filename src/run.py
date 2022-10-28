from collections import defaultdict

import numpy as np
import pygame

from config import MS_PER_UPDATE
from consts import PI
from event_handlers import EventHandler, QuitHandler
from loop import SimulationLoop
from pendulum import DoublePendulum
from renderers import FPSTrackerRenderer, PendulumsRenderer, SimulationRenderer
from world import World


def create_pendulum(
    initial_theta1: float = 0.8 * PI,
    initial_theta2: float = PI,
    random_factor: float = 0,
):
    theta1 = initial_theta1 + np.random.randn() * random_factor
    theta2 = initial_theta2 + np.random.randn() * random_factor
    return DoublePendulum(10, 10, 200, 200, theta1, theta2, dt=0.01)


def create_default_anchor_vector(screen) -> pygame.Vector2:
    w, h = screen.get_size()
    return pygame.Vector2(w // 2, h // 2)


def main():
    n = 3

    pygame.init()
    screen = pygame.display.set_mode()
    anchor: pygame.Vector2 = create_default_anchor_vector(screen)

    pendulums = [create_pendulum(random_factor=1e-5) for _ in range(n)]

    pendulums_renderer = PendulumsRenderer(pendulums, screen, None, None, anchor)
    fps_renderer = FPSTrackerRenderer(screen)

    world = World(pendulums)

    event_handlers: dict[int, list[EventHandler]] = defaultdict(list)

    quit_handler = QuitHandler()

    event_handlers[pygame.KEYDOWN].append(pendulums_renderer)
    event_handlers[pygame.KEYDOWN].append(quit_handler)
    event_handlers[pygame.QUIT].append(quit_handler)

    renderer = SimulationRenderer(screen, [pendulums_renderer, fps_renderer])

    loop = SimulationLoop(world, renderer, event_handlers, MS_PER_UPDATE)

    loop.run()


if __name__ == "__main__":
    main()
