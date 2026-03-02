import pygame
from .visualizer import Visualizer

class NQueens:
    def __init__(self, queens_count: int) -> None:
        self.queens_count: int = queens_count
        self.reset()
    
    def reset(self) -> None:
        self.queens: list[int] = [-1]*self.queens_count
        self.solving_row: int = 0
        self.cols: set[int] = set()
        self.diagonal1: set[int] = set() # Row - Col
        self.diagonal2: set[int] = set() # Row + Col
    
    def update(self) -> bool:
        if self.solving_row >= self.queens_count:
            return True
        self.step_next()
        return False

    def is_valid(self, row: int, col: int) -> bool:
        return col not in self.cols and row - col not in self.diagonal1 and row + col not in self.diagonal2

    def place_queen(self, row: int, col: int) -> None:
        self.queens[row] = col
        self.cols.add(col)
        self.diagonal1.add(row - col)
        self.diagonal2.add(row + col)
    
    def remove_queen(self, row: int, col: int) -> None:
        self.queens[row] = -1
        self.cols.remove(col)
        self.diagonal1.remove(row - col)
        self.diagonal2.remove(row + col)
    
    def get_first_possible(self, row: int, start: int) -> int:
        for col in range(start, self.queens_count):
            if self.is_valid(row, col):
                return col
        return -1

    def step_next(self) -> None:
        col: int = self.queens[self.solving_row]
        if (col != -1):
            self.remove_queen(self.solving_row, col)
        possible: int = self.get_first_possible(self.solving_row, col + 1)
        if (possible == -1):
            self.solving_row -= 1
            return
        self.place_queen(self.solving_row, possible)
        self.solving_row += 1

class NQueensApp(Visualizer):
    NAME: str = "NQueens"
    queens_count: int = 8
    CELL_SIZE: int = 50
    SURFACE_SIZE: int = queens_count*CELL_SIZE
    WIDTH: int = SURFACE_SIZE
    HEIGHT: int = SURFACE_SIZE
    COLORS: dict[str, tuple[int, int, int]]  = {"bg_light": (235, 236, 208), "bg_dark": (119, 149, 86)}

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.nqueens: NQueens = NQueens(NQueensApp.queens_count)

        self.queen_img: pygame.Surface = pygame.image.load(".\\assets\\W_Queen.png")
        self.queen_img.set_colorkey((181, 230, 29))
        self.queen_img = pygame.transform.scale(self.queen_img, (NQueensApp.CELL_SIZE, NQueensApp.CELL_SIZE))

        self.board_surface = pygame.Surface(self.surface_rect.size)
        self.draw_board_bg()
        self.fps: int = 10
        self.solving: bool = False
    
    def draw_board_bg(self) -> None:
        self.board_surface.fill(self.COLORS["bg_light"])

        for row in range(NQueensApp.queens_count):
            for col in range(NQueensApp.queens_count):
                if (row + col)&1 == 0: continue
                pygame.draw.rect(self.board_surface, self.COLORS["bg_dark"], (col*NQueensApp.CELL_SIZE, row*NQueensApp.CELL_SIZE, NQueensApp.CELL_SIZE, NQueensApp.CELL_SIZE))
    
    def draw_queens(self) -> None:
        for row, col in enumerate(self.nqueens.queens):
            if (col == -1):
                break
            self.surface.blit(self.queen_img, (col*NQueensApp.CELL_SIZE, row*NQueensApp.CELL_SIZE))

    def draw(self) -> None:
        self.surface.blit(self.board_surface, (0, 0))
        self.draw_queens()
        self.update_screen()

    def mainloop(self) -> bool:
        self.clock.tick(self.fps)
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
                                self.solving = True

                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10

            if self.solving:
                self.solving = not self.nqueens.update()
            self.draw()

if __name__ == "__main__":
    screen: pygame.Surface = pygame.display.set_mode((NQueensApp.SURFACE_SIZE, NQueensApp.SURFACE_SIZE))
    app: Visualizer = NQueensApp(screen)
    app.mainloop()
    pygame.quit()