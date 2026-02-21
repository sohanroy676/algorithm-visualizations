import pygame, opensimplex
from math import ceil
from utils import Vec2

class App:
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

    def __init__(self, WIN: pygame.Surface) -> None:
        print("Starting the Marching Squares")
        print("ESC to Quit")
        print("Enter to pause/continue")

        self.WIN: pygame.Surface = WIN
        WINRect: pygame.Rect = self.WIN.get_rect()
        self.SURF: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        pygame.display.set_caption("Marching Squares")

        self.blitPos: tuple[int] = ((WINRect.width - App.WIDTH)//2, (WINRect.height - App.HEIGHT)//2)

        self.paused: bool = False
        self.grid: list[list[float]] = [[0 for j in range(App.COLS)] for i in range(App.ROWS)]

    def line(self, v1: Vec2, v2: Vec2) -> None:
        pygame.draw.line(self.SURF, App.COLORS[1], v1.getPos(), v2.getPos())

    def drawNodes(self) -> None:
        for i in range(App.ROWS):
            for j in range(App.COLS):
                pygame.draw.circle(self.SURF, (255 * (self.grid[i][j] + 1) / 2, 255 * (self.grid[i][j] + 1) / 2, 255 * (self.grid[i][j] + 1) / 2), (j * App.STEP, i * App.STEP), App.RADIUS)

    def getState(a: int, b: int, c: int, d: int) -> int:
        return a * 8 + b * 4 + c * 2 + d

    def march(self, i: int, j: int) -> None:
        x: int = j * App.STEP
        y: int = i * App.STEP
        a: Vec2 = Vec2(x + App.HALFSTEP, y)
        b: Vec2 = Vec2(x + App.STEP, y + App.HALFSTEP)
        c: Vec2 = Vec2(x + App.HALFSTEP, y + App.STEP)
        d: Vec2 = Vec2(x, y + App.HALFSTEP)
        state: int = App.getState(ceil(self.grid[i][j]), ceil(self.grid[i][j+1]), ceil(self.grid[i+1][j+1]), ceil(self.grid[i+1][j]))
        match state:
            case 0b0001 | 0b1110:
                self.line(c, d)
            case 0b0010 | 0b1101:
                self.line(b, c)
            case 0b0011 | 0b1100:
                self.line(b, d)
            case 0b0100 | 0b1011:
                self.line(a, b)
            case 0b0101 :
                self.line(a, d)
                self.line(b, c)
            case 0b0110 | 0b1001:
                self.line(a, c)
            case 0b0111 | 0b1000:
                self.line(a, d)
            case 0b1010:
                self.line(a, b)
                self.line(c, d)

    def randGrid(self) -> None:
        App.offsets[1] = 0
        for i in range(App.ROWS):
            App.offsets[0] = 0
            for j in range(App.COLS):
                self.grid[i][j] = opensimplex.noise3(*App.offsets)
                App.offsets[0] += App.INCREMENTS[0]
            App.offsets[1] += App.INCREMENTS[1]
        App.offsets[2] += App.INCREMENTS[2]

    def next(self) -> None:
        self.randGrid()
        for i in range(App.ROWS-1):
            for j in range(App.COLS-1):
                self.march(i, j)
    
    def update(self) -> None:
        pygame.display.update(self.WIN.blit(self.SURF, self.blitPos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualizations")

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
                self.SURF.fill(App.COLORS[0])
                self.next()
                self.update()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()