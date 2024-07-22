import pygame
from src.consts import BLACK


class ControlsRenderer:
    FONT_FAMILY = "Verdana"
    FONT_SIZE_FACTOR = 80
    X_FACTOR = 0.2
    Y_FACTOR = 0.1

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.text = """Toggle limbs:  L\nToggle masses:  M\nExit:  Esc"""
        self._reset_dimensions(screen.get_size())

    def _reset_dimensions(self, screen_size: tuple[int, int]):
        w, h = screen_size
        self.font = pygame.font.SysFont(self.FONT_FAMILY, w // self.FONT_SIZE_FACTOR)
        self.position = (w * self.X_FACTOR, h * self.Y_FACTOR)

    def render(self):
        lines = self.text.splitlines()
        for index, line in enumerate(lines):
            surf = self.font.render(line, True, BLACK)
            pos = (self.position[0], self.position[1] + self.font.get_height() * index)
            self.screen.blit(surf, pos)
