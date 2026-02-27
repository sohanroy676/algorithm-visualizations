'''
A* Path Finding Algorithm for 2D Grid without diagonal movement
'''
import pygame
from heapq import heappush, heappop
from enum import IntEnum
from typing import Callable
from .visualizer import Visualizer
from visualizations.utils import draw_grid_lines

class Cell:
    def __init__(self, row: int, col: int, goal: Cell | None = None) -> None:
        self.row: int = row
        self.col: int = col

        self.parent: Cell | None = None
        
        self.g: float | int = float("inf")
        self.h: float | int = 0 if goal is None else self.get_distance(goal)
        self.f: float | int = self.g + self.h
        
    def update(self, parent: Cell) -> bool:
        new_g: int = parent.g + 1
        if new_g >= self.g: return False
        self.parent = parent
        self.g = new_g
        self.f = self.h + self.g
        return True

    def get_distance(self, other: Cell) -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def __eq__(self, other: Cell) -> bool:
        return (self.row == other.row and self.col == other.col)

    def __hash__(self) -> int:
        return hash((self.row, self.col))
    
    def __lt__(self, other: Cell) -> bool:
        return (self.f, self.h) < (other.f, other.h)

    def __repr__(self) -> str:
        return f"({self.row}, {self.col}) : ({self.g}, {self.h}, {self.f})"

class CellState(IntEnum):
    WALL = 0
    EMPTY = 1
    START = 2
    GOAL = 3

class Astar:
    states = []
    def __init__(self, rows: int, cols: int, on_update: Callable[[int, int, tuple[int, int, int]], None] | None = None) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.on_update: Callable[[int, int, tuple[int, int, int]], None] | None = on_update
        self.reset()

    def reset(self) -> None:
        self.solve_started: bool = False
        self.current_cell: Cell | None = None
        self.goal_cell: Cell | None = None
        self.open: list[Cell] = []
        self.closed: set[Cell] = set()
        self.path: list = []
        self.reset_grid()

    def reset_grid(self) -> None:
        self.grid: list[list[int]] = [[CellState.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells: list[list[Cell]] | None = None
        self.start_pos: tuple[int, int] = (-1, -1)
        self.goal_pos: tuple[int, int] = (-1, -1)
    
    def place(self, row: int, col: int, state: int) -> None:
        self.grid[row][col] = state
        if state == CellState.START:
            self.start_pos = (row, col)
        elif state == CellState.GOAL:
            self.goal_pos = (row, col)
        self.on_update(row, col, AstarApp.COLORSLIST[state])
    
    def get_neighbors(self) -> list[tuple[int, int]]:
        row: int = self.current_cell.row
        col: int = self.current_cell.col
        
        neighbors: list[Cell] = [self.cells[neighbor_row][neighbor_col]
                                 for neighbor_row, neighbor_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
                                 if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and
                                    self.grid[neighbor_row][neighbor_col] != CellState.WALL]
        return neighbors

    def solve_start(self) -> None:
        self.goal_cell = Cell(*self.goal_pos)
        self.cells = [[
                (Cell(i, j, self.goal_cell) if state != CellState.GOAL else self.goal_cell)
                for j, state in enumerate(row)
            ] for i, row in enumerate(self.grid)]
        self.start_cell: Cell = self.cells[self.start_pos[0]][self.start_pos[1]]
        self.start_cell.g = 0
        self.start_cell.f = self.start_cell.h
        heappush(self.open, self.start_cell)
        self.solve_started = True

    def step_next(self) -> None:
        self.current_cell: Cell = self.get_from_open()
        if self.current_cell in self.closed:
            return
        
        self.closed.add(self.current_cell)

        if self.current_cell != self.start_cell and self.current_cell != self.goal_cell:
            self.on_update(self.current_cell.row, self.current_cell.col, AstarApp.COLORS["closed"])
        
        if self.current_cell == self.goal_cell:
            print(self.current_cell, self.start_cell, self.goal_cell)
            self.get_path()
            self.solve_started = False
            return
        
        for neighbor in self.get_neighbors():
            if neighbor in self.closed: continue

            if not neighbor.update(self.current_cell):
                continue

            heappush(self.open, neighbor)
            self.on_update(neighbor.row, neighbor.col, AstarApp.COLORS["open"])

    def get_path(self) -> None:
        self.path: list[Cell] = [self.current_cell]
        parent: Cell = self.current_cell.parent
        while parent is not None:
            self.path.append(parent)
            parent = parent.parent
        for cell in self.path:
            self.on_update(cell.row, cell.col, AstarApp.COLORS["goal"])

    def get_from_open(self) -> Cell:
        return heappop(self.open)

class AstarApp(Visualizer):
    NAME: str = "Pathfinder"
    SIDE: int = 50
    WIDTH: int = 1000
    HEIGHT: int = 700
    ROWS: int = HEIGHT//SIDE
    COLS: int = WIDTH//SIDE
    COLORS: dict[str: tuple[int]] = {"wall": (0, 0, 0), "empty": (255, 255, 255), "start": (0, 0, 255), "goal": (100, 200, 255), "open": (0, 255, 0), "closed": (255, 0, 0)}
    COLORSLIST: list[tuple[int]] = [i for i in COLORS.values()]

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.astar: Astar = Astar(self.ROWS, self.COLS, self.update_grid)
        self.placing_state: int = -1
        self.fps: int = 60
        self.is_shift_down: bool = False

        self.grid_lines_surface: pygame.Surface = pygame.Surface(self.surface_rect.size)
        self.cells_surface: pygame.Surface = pygame.Surface(self.surface_rect.size)
        self.reset_surf()

        AstarApp.__print_instructions()
    
    @staticmethod
    def __print_instructions() -> None:
        print("Starting the Visualisation for A* Pathfinding Algorithm")
        print("ESC to Quit")
        print("Enter to start solving")
        print("BACKSPACE | R to Clear")
        print("LEFT_CLICK to place Wall")
        print("RIGHT_CLICK to remove Wall")
        print("SHIFT + LEFT_CLICK to place the Start Point")
        print("SHIFT + RIGHT_CLICK to place the GOAL Point")
    
    def update_screen(self) -> None:
        self.surface.blit(self.cells_surface)
        self.surface.blit(self.grid_lines_surface)
        super().update_screen()
        
    def update_grid(self, row: int, col: int, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.cells_surface, color, (col*AstarApp.SIDE, row*AstarApp.SIDE, AstarApp.SIDE, AstarApp.SIDE))
        self.update_screen()
    
    def reset_surf(self) -> None:
        self.cells_surface.fill(AstarApp.COLORS["empty"])
        self.grid_lines_surface.fill((255, 255, 255))
        self.grid_lines_surface.set_colorkey((255, 255, 255))
        draw_grid_lines(self.grid_lines_surface, self.ROWS, self.COLS, self.SIDE, self.COLORS["wall"])
        self.update_screen()
    
    def reset(self) -> None:
        self.astar.reset()
        self.reset_surf()
    
    def get_mouse_pos(self) -> tuple[int]:
        x, y = pygame.mouse.get_pos()
        return ((y - self.blit_pos.y)//self.SIDE, (x - self.blit_pos.x)//self.SIDE)

    def on_mouse_down(self) -> None:
        row, col = self.get_mouse_pos()
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS: return
        state: CellState = CellState(self.placing_state + 2) if self.is_shift_down else self.placing_state
        self.astar.place(row, col, state)

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.astar.solve_start()
                            case pygame.K_BACKSPACE | pygame.K_r:
                                self.reset()
                            case pygame.K_LSHIFT | pygame.K_RSHIFT:
                                self.is_shift_down = True
                    
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_LSHIFT | pygame.K_RSHIFT:
                                self.is_shift_down = False
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self.placing_state = CellState.WALL
                            case pygame.BUTTON_RIGHT:
                                self.placing_state = CellState.EMPTY
                            case pygame.BUTTON_WHEELUP | pygame.BUTTON_WHEELDOWN:
                                if not self.astar.solveStarted:
                                    self.astar.place(AstarApp.get_mouse_pos(), CellState.START if event.button == 4 else CellState.GOAL)
                    
                    case pygame.MOUSEBUTTONUP:
                        self.placing_state = -1

            if self.astar.solve_started:
                self.astar.step_next()
            elif self.placing_state != -1:
                self.on_mouse_down()


if __name__ == "__main__":
    screen: pygame.Surface = pygame.display.set_mode((AstarApp.WIDTH, AstarApp.HEIGHT))
    app: Visualizer = AstarApp(screen)
    app.mainloop()
    pygame.quit()