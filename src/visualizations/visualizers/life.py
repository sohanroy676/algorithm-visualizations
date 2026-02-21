'''
Cellular Automata (2D) : Conway's Game of Life
'''
import pygame, random
from utils import drawGridLines

class Life:
    def __init__(self) -> None:
        self.running: bool = False
        self.resetGrid()
        self.saved: list[list[int]] = []

    def resetGrid(self, rand: bool = False) -> None:
        self.grid: list[list[int]] = [[0 if not rand else random.choice([0, 1, 0, 0, 0]) for i in range(App.COLS)] for j in range(App.ROWS)]
    
    def place(self, pos: list[int], s: int) -> None:
        if 0 <= pos[0] < App.WIDTH and 0 <= pos[1] < App.HEIGHT:
            r, c = pos[1]//App.SIDE, pos[0]//App.SIDE
            self.grid[r][c] = s
    
    def numAlive(self, r: int, c: int) -> int:
        n: int = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not i and not j: continue
                newR: int = r+i
                newC: int = c+j
                if newR >= App.ROWS: newR %= App.ROWS
                if newC >= App.COLS: newC %= App.COLS
                if (self.grid[newR][newC]):
                    n += 1
        return n

    def next(self) -> None:
        nextGrid: list[list[int]] = [[0 for j in i] for i in self.grid]
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                n = self.numAlive(i, j)
                if  n == 3: 
                    nextGrid[i][j] = 1
                elif n == 2:
                    nextGrid[i][j] = val            
        for i, row in enumerate(nextGrid):
            for j, val in enumerate(row):
                self.grid[i][j] = val
    
    def save(self) -> None:
        self.saved: list[list[int]] = []
        for i, row in enumerate(self.grid):
            self.saved.append([])
            for j, val in enumerate(row):
                self.saved[i].append(val)
    
    def load(self) -> None:
        if not self.saved: return
        for i, row in enumerate(self.saved):
            for j, val in enumerate(row):
                self.grid[i][j] = val

class App:
    ROWS: int = 140
    COLS: int = 200
    SIDE: int = 5
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE

    COLORS: list[tuple[int]] = [(100, 100, 100), (255, 255, 0), (150, 150, 150)]
    def __init__(self, WIN: pygame.Surface) -> None:
        print("Starting Cellular Automata (2D) : Conway's Game of Life")
        print("ESC to Quit")
        print("ENTER to continue/pause the simulation")
        print("R to Reset")
        print("S to Save the simulation")
        print("L to Load the saved simulation")
        print("LEFT_CLICK to set the cell")
        print("RIGHT_CLICK to clear the cell")
        print("SCROLL_WHEEL_UP to increase the simulation speed")
        print("SCROLL_WHEEL_DOWN to decrease the simulation speed")
        self.WIN: pygame.Surface = WIN
        WINRect: pygame.Rect = self.WIN.get_rect()
        self.SURF: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")

        self.blitPos: tuple[int] = ((WINRect.width - App.WIDTH)//2, (WINRect.height - App.HEIGHT)//2)

        self.fps: int = 60
        self.mouseState: int = 0
        self.life: Life = Life()
        self.clock = pygame.time.Clock()

    def drawGrid(self) -> None:
        for i, row in enumerate(self.life.grid):
            for j, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.SURF, App.COLORS[1], (j*App.SIDE, i*App.SIDE, App.SIDE, App.SIDE))

    def draw(self) -> None:
        self.SURF.fill(App.COLORS[0])
        self.drawGrid()
        drawGridLines(self.SURF, App.ROWS, App.COLS, App.SIDE, App.COLORS[2])
        self.update()
    
    def update(self) -> None:
        pygame.display.update(self.WIN.blit(self.SURF, self.blitPos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualizations")
    
    def getMousePos(self) -> tuple[int]:
        pos: tuple[int] = pygame.mouse.get_pos()
        return [pos[0]-self.blitPos[0], pos[1]-self.blitPos[1]]

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT: return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.life.running = not self.life.running
                                self.fps = 10 if self.life.running else 30
                            case pygame.K_r:
                                self.life.resetGrid()
                            case pygame.K_s:
                                self.life.save()
                            case pygame.K_l:
                                self.life.load()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self.mouseState = 2
                            case pygame.BUTTON_RIGHT:
                                self.mouseState = 1
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                    
                    case pygame.MOUSEBUTTONUP:
                        self.mouseState = 0
            
            if self.life.running:
                self.life.next()
            if self.mouseState:
                self.life.place(self.getMousePos(), self.mouseState - 1)

            self.draw()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()