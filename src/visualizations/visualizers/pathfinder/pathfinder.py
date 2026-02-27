from abc import ABC, abstractmethod
from collections.abc import Callable

from .cell import Cell, CellType

class Pathfinder(ABC):
    TYPE: str = "Pathfinder"
    def __init__(self, rows: int, cols: int, on_update: Callable[[int, int, str], None] | None = None) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.on_update: Callable[[int, int, str], None] | None = on_update
        self.reset()
    
    def _get_neighbors(self, cell: Cell) -> list[tuple[int, int]]:
        row: int = cell.row
        col: int = cell.col
        
        neighbors: list[Cell] = [self.cells[neighbor_row][neighbor_col]
                                 for neighbor_row, neighbor_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
                                 if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and
                                    self.cells[neighbor_row][neighbor_col].type != CellType.WALL]
        return neighbors

    def get_path(self) -> None:
        cell: Cell = self.goal_cell
        while cell is not None:
            self.on_update(cell.row, cell.col, "GOAL")
            cell = cell.parent

    def reset(self) -> None:
        self.cells: list[list[Cell]] | None = None
        self.current_cell: Cell | None = None
        self.start_cell: Cell | None = None
        self.goal_cell: Cell | None = None

        self.solve_started: bool = False

    @abstractmethod
    def start_solve(self, grid: list[list[CellType]], start_pos: tuple[int, int], goal_pos: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def step_next(self) -> None:
        pass