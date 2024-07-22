from typing import Protocol

import pygame
from src.consts import WHITE


class Renderer(Protocol):
    def render(self): ...


class SceneRenderer:
    def __init__(
        self,
        screen: pygame.Surface,
        renderers: list[Renderer],
        screen_color: str = WHITE,
    ):
        self.screen = screen
        self.renderers = renderers
        self.screen_color = screen_color

    def render(self):
        self.screen.fill(self.screen_color)
        for renderer in self.renderers:
            renderer.render()
        pygame.display.flip()
