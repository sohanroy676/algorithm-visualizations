import pygame
from abc import ABC, abstractmethod

class Visualizer(ABC):
    WIDTH: int
    HEIGHT: int
    NAME: str
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen: pygame.Surface = screen
        self.screen_rect: pygame.Rect = screen.get_rect()

        self.blit_pos: pygame.Rect = pygame.Rect()
        self.blit_pos.size = (self.WIDTH, self.HEIGHT)
        self.blit_pos.center = (self.screen_rect.width//2, self.screen_rect.height//2)

        self.surface: pygame.Surface = pygame.Surface((self.WIDTH, self.HEIGHT)).convert()
        self.surface_rect: pygame.Rect = self.surface.get_rect()
        pygame.display.set_caption(self.NAME)

        self.clock = pygame.time.Clock()
    
    @abstractmethod
    def mainloop(self) -> bool:
        pass
    
    def update_screen(self) -> None:
        pygame.display.update(self.screen.blit(self.surface, self.blit_pos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")