from enum import IntEnum

class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType, goal: Cell | None = None) -> None:
        self.row: int = row
        self.col: int = col

        self.parent: Cell | None = None
        
        self.g: float | int = float("inf")
        self.h: float | int = 0 if goal is None else self.get_distance(goal)
        self.f: float | int = self.g + self.h

        self.type: CellType = cell_type
        
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
        return f"[({self.row}, {self.col}) : ({self.g}, {self.h}, {self.f})]"

class CellType(IntEnum):
    WALL = 0
    EMPTY = 1
    START = 2
    GOAL = 3
