from typing import Protocol

import pygame


class EventHandler(Protocol):
    def handle(self, event: pygame.event.Event): ...


class QuitHandler:
    def handle(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
