'''
Cellular Automata: Sand Simulation
'''
import pygame
from random import choice
from visualizations.utils import HSV_to_RGB

class Sand:
    COLOR: tuple[int] = (0, 0, 0)
    def __init__(self):
        self.reset()
        self.rad = 1
    
    def reset(self):
        App.instance.SURF.fill(self.COLOR)
        self.resetGrid()
        self.h: int = 0
        self.running: bool = True
        App.instance.update()

    def resetGrid(self):
        self.grid: list[list[int]] = [[0 for _ in range(App.COLS)] for _ in range(App.ROWS)]
    
    def swap(self, r1, c1, r2, c2):
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
        pygame.draw.rect(App.instance.SURF, self.COLOR, (c1*App.SIDE, r1*App.SIDE, App.SIDE, App.SIDE))
        pygame.draw.rect(App.instance.SURF, self.getColor(), (c2*App.SIDE, r2*App.SIDE, App.SIDE, App.SIDE))
        App.instance.update()

    def getColor(self) -> list[int]:
        return HSV_to_RGB(self.h, 1, 1)
    
    def next(self):
        for i in range(App.ROWS-2, -1, -1):
            for j in range(App.COLS):
                if not self.grid[i][j]: continue
                dir = choice([1, -1])
                if not self.grid[i+1][j]:
                    self.swap(i, j, i+1, j)
                elif j+dir >= 0 and j+dir < App.COLS and not self.grid[i][j+dir] and not self.grid[i+1][j+dir]:
                    self.swap(i, j, i+1, j+dir)
                elif j-dir >= 0 and j-dir < App.COLS and not self.grid[i][j-dir] and not self.grid[i+1][j-dir]:
                    self.swap(i, j, i+1, j-dir)
        
        self.h = (self.h + 1) % 360
    
    def place(self, pos, state):
        row, col = pos[1]//App.SIDE, pos[0]//App.SIDE
        if state:
            for i in range(max(row-self.rad, 0), min(row+self.rad+1, App.ROWS)):
                for j in range(max(col-self.rad, 0), min(col+self.rad+1, App.COLS)):
                    if not self.grid[i][j]:
                        self.grid[i][j] = 1
                        pygame.draw.rect(App.instance.SURF, self.getColor(), (j*App.SIDE, i*App.SIDE, App.SIDE, App.SIDE))
        else:
            if self.grid[row][col]:
                self.grid[row][col] = 0
                pygame.draw.rect(App.instance.SURF, self.COLOR, (col*App.SIDE, row*App.SIDE, App.SIDE, App.SIDE))
        App.instance.update()

class App:
    ROWS: int = 72
    COLS: int = 100
    SIDE: int = 10
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE
    instance = None
    def __init__(self, WIN: pygame.Surface) -> None:
        print("Starting the Cellular Automata: Sand simulation")
        print("ESC to Quit")
        print("R to reset the simulation")
        print("P to pause/continue")
        print("LEFT_CLICK to place sand")
        print("RIGHT_CLICK to delete sand")

        App.instance = self
        self.WIN: pygame.Surface = WIN
        WINRect: pygame.Rect = self.WIN.get_rect()
        self.SURF: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        pygame.display.set_caption("Sand Simulation")

        self.blitPos: tuple[int] = ((WINRect.width - App.WIDTH)//2, (WINRect.height - App.HEIGHT)//2)

        self.mouseState: int = 0
        self.sand: Sand = Sand()
    
    def update(self) -> None:
        pygame.display.update(self.WIN.blit(self.SURF, self.blitPos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualizations")
    
    def getMousePos(self) -> tuple[int]:
        pos: tuple[int] = pygame.mouse.get_pos()
        return [pos[0]-self.blitPos[0], pos[1]-self.blitPos[1]]
    
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
                            case pygame.K_r:
                                self.sand.reset()
                            case pygame.K_p:
                                self.sand.running = not self.sand.running
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self.mouseState = 2
                            case pygame.BUTTON_RIGHT:
                                self.mouseState = 1
                    
                    case pygame.MOUSEBUTTONUP:
                        self.mouseState = 0

            if self.mouseState:
                self.sand.place(self.getMousePos(), self.mouseState-1)
            if self.sand.running:
                self.sand.next()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()