from collections import deque

from .cell import Cell, CellType
from .pathfinder import Pathfinder

class DFS(Pathfinder):
    TYPE: str = "DFS"
    def reset(self) -> None:
        super().reset()

        self._stack: deque[Cell] | None = None
        self._visited: set[Cell] | None = None

    def start_solve(self, grid: list[list[CellType]], start_pos: tuple[int, int], goal_pos: tuple[int, int]) -> None:
        self.goal_cell = Cell(goal_pos[0], goal_pos[1], CellType.GOAL)
        self.cells = [[
                (Cell(i, j, state) if state != CellType.GOAL else self.goal_cell)
                for j, state in enumerate(row)
            ] for i, row in enumerate(grid)]

        self.start_cell = self.cells[start_pos[0]][start_pos[1]]
        self._stack = deque([self.start_cell])
        self._visited = set()

        self.solve_started = True

    def step_next(self) -> None:
        self.current_cell: Cell = self._get_from_stack()
        
        if self.current_cell in self._visited:
            return
        
        self._visited.add(self.current_cell)

        if self.current_cell != self.start_cell and self.current_cell != self.goal_cell:
            self.on_update(self.current_cell.row, self.current_cell.col, "CLOSED")
        
        if self.current_cell == self.goal_cell:
            self.get_path()
            self.solve_started = False
            return
        
        for neighbor in self._get_neighbors(self.current_cell):
            if neighbor in self._visited:
                continue
            neighbor.parent = self.current_cell
            self._add_to_stack(neighbor)
            self.on_update(neighbor.row, neighbor.col, "OPEN")
    
    def _get_from_stack(self) -> Cell:
        return self._stack.pop()

    def _add_to_stack(self, cell: Cell) -> None:
        self._stack.append(cell)