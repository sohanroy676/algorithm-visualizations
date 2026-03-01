from heapq import heappush, heappop
from collections import deque
from random import random, choice
from collections.abc import Callable

from .tileset import Tilesets

class Cell:
    def __init__(self, row: int, col: int, initial_mask: int) -> None:
        self.row: int = row
        self.col: int = col

        self.collapsed: bool = False
        self.possible_mask: int = initial_mask
        self.value: int | None = None
    
    def collapse(self) -> int:
        mask: int = self.possible_mask
        possible_tiles: list[int] = []
        while mask:
            tile_index: int = (mask & -mask).bit_length() - 1
            possible_tiles.append(tile_index)
            mask &= mask - 1
        
        self.collapsed = True
        
        self.value = choice(possible_tiles) if possible_tiles else 0
        self.possible_mask = 1 << self.value

        return self.value
        
    def get_entropy(self) -> int:
        return self.possible_mask.bit_count()

    def __repr__(self) -> str:
        return f"<({self.row}, {self.col}): {self.collapsed}, {self.value}>"

type HeapItemType = tuple[int, float, tuple[int, int]]

class WaveFunc:
    def __init__(self, rows: int, cols: int, on_update: Callable[[Cell], None]) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.on_update: Callable[[Cell], None] = on_update

        self.tileset_index: int = -1
        self.change_tileset()
    
    def change_tileset(self) -> None:
        self.tileset_index = (self.tileset_index + 1)%len(Tilesets.TILESETS)
        self.tileset_type: str = Tilesets.TILESETS[self.tileset_index]
    
    def reset(self) -> None:
        initial_mask: int = (1 << Tilesets.TILES_COUNT[self.tileset_type]) - 1
        self.grid: list[list[Cell]] = [[Cell(row, col, initial_mask) for col in range(self.cols)] for row in range(self.rows)]
        self.heap: list[HeapItemType] = []
        self.queue: deque[Cell] = deque()

        self.current_cell: Cell | None = None
    
    def start(self) -> None:
        self.reset()
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.push_cell_to_heap(self.grid[row][col])
    
    def push_cell_to_heap(self, cell) -> None:
        heappush(self.heap, (cell.get_entropy(), random(), (cell.row, cell.col)))
    
    def pop_cell_from_heap(self) -> HeapItemType:
        return heappop(self.heap)
    
    def step_next(self) -> bool:
        if not self.heap:
            return False
        
        entropy, _, (row, col) = self.pop_cell_from_heap()
        self.current_cell = self.grid[row][col]
        if self.current_cell.collapsed or entropy != self.current_cell.get_entropy() or self.current_cell.get_entropy() == 0:
            return True
        
        self.current_cell.collapse()
        self.on_update(self.current_cell)

        self.propagate_collapse()
        return True
    
    def get_neighbors(self, cell: Cell) -> list[tuple[int, Cell]]:
        neighbors: list[Cell] = []
        for direction, (dr, dc) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
            row: int = cell.row + dr
            col: int = cell.col + dc
            if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.grid[row][col].collapsed:
                continue
            neighbors.append((direction, self.grid[row][col]))
        return neighbors
    
    def propagate_collapse(self) -> None:
        self.queue.append(self.current_cell)
        while self.queue:
            cell: Cell = self.queue.popleft()
            
            for direction, neighbor in self.get_neighbors(cell):
                if not self.update_neighbor_domain(cell, neighbor, direction):
                    continue
                
                self.on_update(neighbor)
                self.queue.append(neighbor)
                self.push_cell_to_heap(neighbor)
    
    def update_neighbor_domain(self, cell: Cell, neighbor: Cell, direction: int) -> bool:
        old_mask: int = neighbor.possible_mask

        mask: int = cell.possible_mask
        allowed_mask: int = 0

        while mask:
            tile_index: int = (mask & -mask).bit_length() - 1
            allowed_mask |= Tilesets.get_tile_connection(self.tileset_type, tile_index, direction)
            mask &= mask - 1
        
        neighbor.possible_mask &= allowed_mask
        if old_mask == neighbor.possible_mask:
            return False
        return True
