'''
Cellular Automata (2D) : Conway's Game of Life
'''
import pygame
from numpy import ndarray, array
from random import choices
from enum import IntEnum
from visualizations.utils import draw_grid_lines
from visualizations.visualizers.visualizer import Visualizer

class CellState(IntEnum):
    DEAD = 0
    ALIVE = 1

class Life:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self._random_choice_weights: tuple[float, float] = (0.8, 0.2)

        self.reset()

        self._next_grid: list[list[CellState]] = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def reset(self) -> None:
        self.running: bool = False
        self.reset_grid()
        self.saved: list[list[int]] = []

    def reset_grid(self, is_random: bool = False) -> None:
        self.current_grid: list[list[CellState]] = [
            [CellState.DEAD if not is_random else self._get_random_value() for _ in range(self.cols)]
            for _ in range(self.rows)]
    
    def _get_random_value(self) -> CellState:
        return choices((CellState.DEAD, CellState.ALIVE), weights = self._random_choice_weights, k = 1)[0]
    
    def place(self, row: int, col: int, value: CellState) -> None:
        self.current_grid[row][col] = value
    
    def _alive_neighbors_count(self, row: int, col: int) -> int:
        neighbors_alive: int = 0

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue

                new_row: int = row + dr
                new_col: int = col + dc
                if new_row >= self.rows:
                    new_row %= self.rows
                if new_col >= self.cols:
                    new_col %= self.cols

                if self.current_grid[new_row][new_col] == CellState.ALIVE:
                    neighbors_alive += 1
        
        return neighbors_alive

    def step_next(self) -> None:
        for row_index, row in enumerate(self.current_grid):
            for col_index, val in enumerate(row):
                neighbors_alive: int = self._alive_neighbors_count(row_index, col_index)
                match neighbors_alive:
                    case 2:
                        self._next_grid[row_index][col_index] = val
                    case 3:
                        self._next_grid[row_index][col_index] = 1
                    case _:
                        self._next_grid[row_index][col_index] = 0

        self.current_grid, self._next_grid = self._next_grid, self.current_grid
    
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

class LifeApp(Visualizer):
    NAME: str = "Life"
    ROWS: int = 140
    COLS: int = 200
    SIDE: int = 5
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE

    COLORS: tuple[tuple[int, int, int], ...] = ((100, 100, 100), (255, 255, 0), (150, 150, 150))
    COLORS_ARRAY: ndarray = array(((100, 100, 100), (255, 255, 0), (150, 150, 150)))
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.life: Life = Life(self.ROWS, self.COLS)
        self.fps: int = 0
        self.mouse_state: int = -1

        self.life_surface: pygame.Surface = pygame.Surface((self.COLS, self.ROWS)).convert()

        LifeApp.print_instructions()

    
    @staticmethod
    def print_instructions() -> None:
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
    
    def draw_grid(self) -> None:
        for i, row in enumerate(self.life.current_grid):
            for j, val in enumerate(row):
                if val == 0:
                    continue
                pygame.draw.rect(self.surface, self.COLORS[CellState.ALIVE], (j*self.SIDE, i*self.SIDE, self.SIDE, self.SIDE))
    
    def draw_grid_1(self) -> None:
        surface_array: ndarray = pygame.surfarray.pixels3d(self.life_surface)
        surface_array[:] = self.COLORS_ARRAY[self.life.current_grid].swapaxes(0, 1)
        del surface_array
        pygame.transform.scale_by(self.life_surface, self.SIDE, self.surface)

    def draw(self) -> None:
        self.surface.fill(self.COLORS[CellState.DEAD])
        self.draw_grid_1()
        draw_grid_lines(self.surface, self.ROWS, self.COLS, self.SIDE, self.COLORS[2])
        self.update_screen()
    
    def get_mouse_pos(self) -> tuple[int, int] | None:
        x, y = pygame.mouse.get_pos() 
        col: int = (x - self.blit_pos.x)//self.SIDE
        row: int = (y - self.blit_pos.y)//self.SIDE
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return None
        return (row, col)

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
                            case pygame.K_SPACE:
                                self.life.step_next()
                            case pygame.K_r:
                                self.life.reset_grid()
                            case pygame.K_TAB:
                                self.life.reset_grid(True)
                            case pygame.K_s:
                                self.life.save()
                            case pygame.K_l:
                                self.life.load()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self.mouse_state = CellState.ALIVE
                            case pygame.BUTTON_RIGHT:
                                self.mouse_state = CellState.DEAD
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                    
                    case pygame.MOUSEBUTTONUP:
                        self.mouse_state = -1
            
            if self.life.running:
                self.life.step_next()

            if self.mouse_state != -1:
                mouse_pos: tuple[int, int] | None = self.get_mouse_pos()
                if mouse_pos is not None:
                    self.life.place(*mouse_pos, CellState(self.mouse_state))

            self.draw()

def main() -> None:
    screen: pygame.Surface = pygame.display.set_mode((LifeApp.WIDTH, LifeApp.HEIGHT))
    app: Visualizer = LifeApp(screen)
    app.mainloop()
    pygame.quit() 

if __name__ == "__main__":
    main()