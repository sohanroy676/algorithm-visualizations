'''
Cellular Automata: Sand Simulation
'''
import pygame
from numpy import ndarray, array
from random import choice
from visualizations.utils import HSV_to_RGB
from visualizations.visualizers.visualizer import Visualizer

class Sand:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows: int = rows
        self.cols: int = cols

        self.reset()
    
    def reset(self) -> None:
        self.reset_grid()
        self.h: int = 0
        self.running: bool = True

    def reset_grid(self) -> None:
        self.grid: list[list[int]] = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def _swap_cells(self, row1: int, col1: int, row2: int, col2: int) -> None:
        self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]
    
    def _can_cell_swap(self, row: int, new_col: int) -> bool:
        return new_col >= 0 and new_col < self.cols and self.grid[row][new_col] == self.grid[row + 1][new_col] == 0
    
    def step_next(self):
        direction = choice([1, -1])

        for row in range(self.rows - 2, -1, -1):
            for col in range(self.cols):
                if self.grid[row][col] == 0: continue
                
                if self.grid[row + 1][col] == 0:
                    self._swap_cells(row, col, row + 1, col)

                elif self._can_cell_swap(row, col + direction):
                    self._swap_cells(row, col, row + 1, col + direction)

                elif self._can_cell_swap(row, col - direction):
                    self._swap_cells(row, col, row + 1, col - direction)
    
    def place(self, row: int, col: int, value: int) -> None:
        self.grid[row][col] = value

class SandApp(Visualizer):
    NAME: str = "Sand"
    ROWS: int = 72
    COLS: int = 100
    SIDE: int = 10
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE

    COLORS_ARRAY: ndarray | None = None

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        if SandApp.COLORS_ARRAY is None:
            SandApp.COLORS_ARRAY = array([tuple(map(int, HSV_to_RGB(hue, 1, 1))) for hue in range(360)])
            SandApp.COLORS_ARRAY[0] = (0, 0, 0)

        self.sand: Sand = Sand(self.ROWS, self.COLS)
        self._sand_surface: pygame.Surface = pygame.Surface((self.COLS, self.ROWS)).convert()
        self._brush_radius: int = 1

        self.reset()

        SandApp.print_instructions()
    
    def reset(self) -> None:
        self._placing_value: int = 1
        self._placing_value_timer: int = 0
        self._placing_value_update_rate: int = 5
        self._mouse_state: int = -1
        self.sand.reset()
    
    def _update_placing_value(self) -> None:
        self._placing_value_timer += 1
        if self._placing_value_timer < self._placing_value_update_rate:
            return
        self._placing_value_timer = 0
        self._placing_value = (self._placing_value + 1)%358 + 1
    
    @staticmethod
    def print_instructions() -> None:
        print("Starting the Cellular Automata: Sand simulation")
        print("ESC to Quit")
        print("R to reset the simulation")
        print("P to pause/continue")
        print("LEFT_CLICK to place sand")
        print("RIGHT_CLICK to delete sand")
    
    def get_mouse_pos(self) -> tuple[int, int] | None:
        x, y = pygame.mouse.get_pos()
        col: int = (x - self.blit_pos.x)//self.SIDE
        row: int = (y - self.blit_pos.y)//self.SIDE
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return None
        return (row, col)
    
    def draw_grid(self) -> None:
        pixels: ndarray = pygame.surfarray.pixels3d(self._sand_surface)
        pixels[:] = self.COLORS_ARRAY[self.sand.grid].swapaxes(0, 1)
        del pixels
        pygame.transform.scale_by(self._sand_surface, self.SIDE, self.surface)
    
    def on_mouse_down(self) -> None:
        center_row, center_col = self.get_mouse_pos()
        for row in range(max(center_row - self._brush_radius, 0), min(center_row + self._brush_radius + 1, self.ROWS)):
            for col in range(max(center_col - self._brush_radius, 0), min(center_col + self._brush_radius + 1, self.COLS)):
                if self.sand.grid[row][col] == 0:
                    self.sand.place(row, col, self._placing_value if self._mouse_state == 1 else 0)

    def draw(self) -> None:
        self.draw_grid()
        self.update_screen()
    
    def mainloop(self) -> bool:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_r:
                                self.reset()
                            case pygame.K_p:
                                self.sand.running = not self.sand.running
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self._mouse_state = 1
                            case pygame.BUTTON_RIGHT:
                                self._mouse_state = 0
                    
                    case pygame.MOUSEBUTTONUP:
                        self._mouse_state = -1

            if self._mouse_state != -1:
                self.on_mouse_down()

            if self.sand.running:
                self.sand.step_next()
                self._update_placing_value()
            
            self.draw()

def main() -> None:
    screen: pygame.Surface = pygame.display.set_mode((SandApp.WIDTH, SandApp.HEIGHT))
    app: Visualizer = SandApp(screen)
    app.mainloop()
    pygame.quit()

if __name__ == "__main__":
    main()