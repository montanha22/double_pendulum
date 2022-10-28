from time import time

import pygame

from event_handlers import EventHandler
from renderers import SimulationRenderer
from world import World


class Timer:
    def __init__(self):
        self.previous_t = time()
        self.current_t = time()
        self.elapsed_t = 0
        self.lag = 0

    def tick(self):
        self.current_t = time()
        self.elapsed_t = self.current_t - self.previous_t
        self.previous_t = self.current_t
        self.lag += self.elapsed_t

    def decrease_lag(self, value: float):
        self.lag -= value


class SimulationLoop:
    def __init__(
        self,
        world: World,
        renderer: SimulationRenderer,
        event_handlers: dict[pygame.event.Event, list[EventHandler]],
        ms_per_update: float,
    ):
        self.world = world
        self.renderer = renderer
        self.MPU = ms_per_update
        self.event_handlers = event_handlers

    def run(self):
        timer = Timer()
        while True:

            for event in pygame.event.get():
                for handler in self.event_handlers.get(event.type, []):
                    handler.handle(event)

            timer.tick()
            while timer.lag >= self.MPU:
                self.world.update()
                timer.decrease_lag(self.MPU)

            self.renderer.render()
