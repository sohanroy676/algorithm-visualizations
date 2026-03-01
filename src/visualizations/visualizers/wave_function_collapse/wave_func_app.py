import pygame
from visualizations.utils import remap
from visualizations.visualizers.visualizer import Visualizer
from .tileset import Tilesets
from .wave_func import WaveFunc, Cell

class WaveFuncApp(Visualizer):
    NAME: str = "WaveFunc"
    ROWS: int = 12
    COLS: int = 18
    SIZE: int = 56
    WIDTH: int = COLS * SIZE
    HEIGHT: int = ROWS * SIZE

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        Tilesets.init()

        self.fps: int = 60
        
        self.reset()
    
    def reset(self) -> None:
        self.wave_func: WaveFunc = WaveFunc(self.ROWS, self.COLS, self.update_surface)
        self.started: bool = False

        self.clear_surface()
    
    def clear_surface(self) -> None:
        self.surface.fill((255, 255, 255))
        self.update_screen()

    def update_surface(self, cell: Cell) -> None:
        x: int = cell.col*self.SIZE
        y: int = cell.row*self.SIZE
        if cell.collapsed:
            self.surface.blit(Tilesets.get_tile_image(self.wave_func.tileset_type, cell.value), (x, y))
        else:
            pygame.draw.rect(self.surface, self.get_color(cell), (x, y, self.SIZE, self.SIZE))
        self.update_screen()
    
    def get_color(self, cell: Cell) -> tuple[int, int, int]:
        greyscale: int = remap(0, Tilesets.TILES_COUNT[self.wave_func.tileset_type], 0, 255, cell.get_entropy())
        return (greyscale, greyscale, greyscale)

    def mainloop(self) -> None:
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.quit()
                        return False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.clear_surface()
                                self.wave_func.start()
                                self.started = True
                            case pygame.K_SPACE:
                                self.started = not self.started
                            case pygame.K_TAB:
                                self.wave_func.change_tileset()
            
            if self.started:
                self.started = self.wave_func.step_next()

def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WaveFuncApp.WIDTH, WaveFuncApp.HEIGHT))
    app: Visualizer = WaveFuncApp(screen)
    app.mainloop()
    pygame.quit()

if __name__ == "__main__":
    main()
        