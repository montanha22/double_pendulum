from collections import defaultdict

import numpy as np
import pygame

from src.consts import PI, MS_PER_UPDATE
from src.event_handlers import EventHandler, QuitHandler
from src.loop import SimulationLoop
from src.pendulum import DoublePendulum
from src.renderers import FPSRenderer, ControlsRenderer, DoublePendulumsRenderer, SceneRenderer
from src.world import World


def create_pendulum(
    initial_theta1: float = 0.8 * PI,
    initial_theta2: float = PI,
    random_factor: float = 0,
    m1: float = 10,
    m2: float = 10,
    l1: float = 200,
    l2: float = 200,
    dt: float = 0.01,
):
    theta1 = initial_theta1 + np.random.randn() * random_factor
    theta2 = initial_theta2 + np.random.randn() * random_factor
    return DoublePendulum(m1, m2, l1, l2, theta1, theta2, dt=dt)


def create_default_anchor_vector(screen: pygame.Surface) -> pygame.Vector2:
    w, h = screen.get_size()
    return pygame.Vector2(w // 2, h // 2)


def main():
    n = 3

    pygame.init()
    screen = pygame.display.set_mode()
    anchor: pygame.Vector2 = create_default_anchor_vector(screen)

    pendulums = [create_pendulum(random_factor=1e-5) for _ in range(n)]

    pendulums_renderer = DoublePendulumsRenderer(pendulums, screen, None, None, anchor)
    fps_renderer = FPSRenderer(screen)
    instructions_renderer = ControlsRenderer(screen)

    world = World(pendulums)

    event_handlers: dict[int, list[EventHandler]] = defaultdict(list)

    quit_handler = QuitHandler()

    event_handlers[pygame.KEYDOWN].append(pendulums_renderer)
    event_handlers[pygame.KEYDOWN].append(quit_handler)
    event_handlers[pygame.QUIT].append(quit_handler)

    renderer = SceneRenderer(screen, [pendulums_renderer, fps_renderer, instructions_renderer])

    loop = SimulationLoop(world, renderer, event_handlers, MS_PER_UPDATE)

    loop.run()


if __name__ == "__main__":
    main()
