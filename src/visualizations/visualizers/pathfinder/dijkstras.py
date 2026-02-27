from heapq import heappush, heappop

from .cell import Cell, CellType
from .pathfinder import Pathfinder

class Dijkstras(Pathfinder):
    '''
    Equivalent to BFS as the grid has uniform cost (1) for all cells
    '''
    TYPE: str = "Dijkstras"
    def reset(self) -> None:
        super().reset()

        self._unvisited: list[Cell] = []
        self._visited: set[Cell] = set()
    
    def start_solve(self, grid: list[list[CellType]], start_pos: tuple[int, int], goal_pos: tuple[int, int]) -> None:
        self.goal_cell = Cell(goal_pos[0], goal_pos[1], CellType.GOAL)
        self.cells = [[
                (Cell(i, j, state) if state != CellType.GOAL else self.goal_cell)
                for j, state in enumerate(row)
            ] for i, row in enumerate(grid)]
        
        self.start_cell = self.cells[start_pos[0]][start_pos[1]]
        self.start_cell.g = 0
        self.start_cell.f = 0
        
        self._add_to_unvisited(self.start_cell)
        self.solve_started = True

    def step_next(self) -> None:
        self.current_cell: Cell = self._get_from_unvisited()
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
            if neighbor in self._visited: continue

            if not neighbor.update(self.current_cell):
                continue

            self._add_to_unvisited(neighbor)
            self.on_update(neighbor.row, neighbor.col, "OPEN")
    
    def _add_to_unvisited(self, cell: Cell) -> None:
        heappush(self._unvisited, cell)

    def _get_from_unvisited(self) -> Cell:
        return heappop(self._unvisited)