import pygame
from opensimplex import noise3
from math import ceil
from visualizations.utils import Vector2
from visualizations.visualizers import Visualizer

class MarchSQApp(Visualizer):
    NAME: str = "MarchSQ"
    WIDTH: int = 800
    HEIGHT: int = 720
    STEP: int = 10
    HALFSTEP: int = STEP // 2
    RADIUS: int = 5
    ROWS: int = 1 + HEIGHT // STEP
    COLS: int = 1 + WIDTH // STEP

    offsets: list[float] = [0, 0, 0]
    INCREMENTS: list[float] = [0.1, 0.1, 0.1]

    COLORS: tuple[tuple[int]] = ((100, 100, 100), (255, 255, 255))

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.paused: bool = False
        self.grid: list[list[float]] = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        MarchSQApp.print_instructions()
    
    @staticmethod
    def print_instructions() -> None:
        print("Starting the Marching Squares")
        print("ESC to Quit")
        print("Enter to pause/continue")

    def draw_line(self, v1: Vector2, v2: Vector2) -> None:
        pygame.draw.line(self.surface, self.COLORS[1], v1.get_pos(), v2.get_pos())

    def draw_nodes(self) -> None:
        for i in range(self.ROWS):
            for j in range(self.COLS):
                pygame.draw.circle(self.surface, (255 * (self.grid[i][j] + 1) / 2, 255 * (self.grid[i][j] + 1) / 2, 255 * (self.grid[i][j] + 1) / 2), (j * self.STEP, i * self.STEP), self.RADIUS)

    @staticmethod
    def get_state(a: int, b: int, c: int, d: int) -> int:
        return a * 8 + b * 4 + c * 2 + d

    def march(self, i: int, j: int) -> None:
        x: int = j * self.STEP
        y: int = i * self.STEP
        a: Vector2 = Vector2(x + self.HALFSTEP, y)
        b: Vector2 = Vector2(x + self.STEP, y + self.HALFSTEP)
        c: Vector2 = Vector2(x + self.HALFSTEP, y + self.STEP)
        d: Vector2 = Vector2(x, y + self.HALFSTEP)
        state: int = MarchSQApp.get_state(ceil(self.grid[i][j]), ceil(self.grid[i][j+1]), ceil(self.grid[i+1][j+1]), ceil(self.grid[i+1][j]))
        match state:
            case 0b0001 | 0b1110:
                self.draw_line(c, d)
            case 0b0010 | 0b1101:
                self.draw_line(b, c)
            case 0b0011 | 0b1100:
                self.draw_line(b, d)
            case 0b0100 | 0b1011:
                self.draw_line(a, b)
            case 0b0101 :
                self.draw_line(a, d)
                self.draw_line(b, c)
            case 0b0110 | 0b1001:
                self.draw_line(a, c)
            case 0b0111 | 0b1000:
                self.draw_line(a, d)
            case 0b1010:
                self.draw_line(a, b)
                self.draw_line(c, d)

    def get_random_grid(self) -> None:
        self.offsets[1] = 0
        
        for i in range(self.ROWS):
            self.offsets[0] = 0
            
            for j in range(self.COLS):
                self.grid[i][j] = noise3(*self.offsets)
                self.offsets[0] += self.INCREMENTS[0]
            
            self.offsets[1] += self.INCREMENTS[1]
        
        self.offsets[2] += self.INCREMENTS[2]

    def step_next(self) -> None:
        self.get_random_grid()

        for row in range(self.ROWS - 1):
            for col in range(self.COLS - 1):
                self.march(row, col)

    def mainloop(self) -> bool:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                return True
                            case pygame.K_RETURN:
                                self.paused = not self.paused
            
            if not self.paused:
                self.surface.fill(self.COLORS[0])
                self.step_next()
                self.update_screen()

def main() -> None:
    screen: pygame.Surface = pygame.display.set_mode((MarchSQApp.WIDTH, MarchSQApp.HEIGHT))
    app: Visualizer = MarchSQApp(screen)
    app.mainloop()
    pygame.quit()


if __name__ == "__main__":
    main()