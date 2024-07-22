import pygame
from src.consts import BLACK


class FPSRenderer:
    FONT_FAMILY = "Verdana"
    FONT_SIZE_FACTOR = 80
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
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.screen.blit(self.text_surface, self.position)
