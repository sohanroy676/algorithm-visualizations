from abc import ABC, abstractmethod
import pygame

class Visualizer(ABC):
    def __init__(self, window: pygame.Surface) -> None:
        self.window: pygame.Surface = window
        self.win_rect: pygame.Rect = window.get_rect()

        self.blitPos: tuple[int] = ((self.win_rect.width - self.WIDTH)//2, (self.win_rect.height - self.HEIGHT)//2)

        self.surf: pygame.Surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        pygame.display.set_caption(self.NAME)

        self.clock = pygame.time.Clock()
    
    @abstractmethod
    def mainloop(self) -> None:
        pass
    
    def update_window(self) -> None:
        pygame.display.update(self.window.blit(self.surf, self.blitPos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")