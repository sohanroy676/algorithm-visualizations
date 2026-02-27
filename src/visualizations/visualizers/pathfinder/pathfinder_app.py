import pygame

from visualizations.visualizers.visualizer import Visualizer
from visualizations.utils import draw_grid_lines
from .pathfinder import Pathfinder
from .astar import Astar
from .dijkstras import Dijkstras
from .bfs import BFS
from .dfs import DFS
from .cell import CellType

class PathfinderApp(Visualizer):
    NAME: str = "Pathfinder"
    SIDE: int = 50
    WIDTH: int = 1000
    HEIGHT: int = 700
    ROWS: int = HEIGHT//SIDE
    COLS: int = WIDTH//SIDE
    
    COLORS: dict[str: tuple[int]] = {"WALL": (0, 0, 0), "EMPTY": (255, 255, 255), "START": (0, 0, 255), "GOAL": (100, 200, 255), "OPEN": (0, 255, 0), "CLOSED": (255, 0, 0)}

    PATHFINDERS: list[Pathfinder] = [Astar, BFS, DFS, Dijkstras]

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.pathfinder_index: int = -1
        self.change_pathfinder()

        self.grid_lines_surface: pygame.Surface = pygame.Surface(self.surface_rect.size)
        self.cells_surface: pygame.Surface = pygame.Surface(self.surface_rect.size)
        
        self.reset()

        # PathfinderApp._print_instructions()
    
    def change_pathfinder(self) -> None:
        self.pathfinder_index = (self.pathfinder_index + 1)%len(self.PATHFINDERS)
        self.pathfinder: Pathfinder = self.PATHFINDERS[self.pathfinder_index](self.ROWS, self.COLS, self.update_grid)
        pygame.display.set_caption(f"Pathfinder - {self.pathfinder.TYPE}")
    
    def reset(self) -> None:
        self.grid: list[list[CellType]] = [[CellType.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.start_pos: tuple[int, int] = (-1, -1)
        self.goal_pos: tuple[int, int] = (-1, -1)
        
        self.placing_state: int = -1
        self.fps: int = 60
        self.is_shift_down: bool = False

        self.pathfinder.reset()
        self.reset_surf()
    
    @staticmethod
    def _print_instructions() -> None:
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
        
    def update_grid(self, row: int, col: int, state: str) -> None:
        pygame.draw.rect(self.cells_surface, self.COLORS[state], (col*self.SIDE, row*self.SIDE, self.SIDE, self.SIDE))
        self.update_screen()
    
    def reset_surf(self) -> None:
        self.cells_surface.fill(self.COLORS["EMPTY"])
        self.grid_lines_surface.fill((255, 255, 255))
        self.grid_lines_surface.set_colorkey((255, 255, 255))
        draw_grid_lines(self.grid_lines_surface, self.ROWS, self.COLS, self.SIDE, self.COLORS["WALL"])
        self.update_screen()
    
    def get_mouse_pos(self) -> tuple[int]:
        x, y = pygame.mouse.get_pos()
        return ((y - self.blit_pos.y)//self.SIDE, (x - self.blit_pos.x)//self.SIDE)

    def place(self, row: int, col: int, state: CellType) -> None:
        self.grid[row][col] = state
        if state == CellType.START:
            self.start_pos = (row, col)
        elif state == CellType.GOAL:
            self.goal_pos = (row, col)
        self.update_grid(row, col, state._name_)

    def on_mouse_down(self) -> None:
        row, col = self.get_mouse_pos()
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS: return
        state: CellType = CellType(self.placing_state + 2) if self.is_shift_down else self.placing_state
        self.place(row, col, state)

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
                                self.pathfinder.start_solve(self.grid, self.start_pos, self.goal_pos)
                            case pygame.K_BACKSPACE | pygame.K_r:
                                self.reset()
                            case pygame.K_LSHIFT | pygame.K_RSHIFT:
                                self.is_shift_down = True
                            case pygame.K_TAB:
                                if not self.pathfinder.solve_started:
                                    self.change_pathfinder()
                    
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_LSHIFT | pygame.K_RSHIFT:
                                self.is_shift_down = False
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_LEFT:
                                self.placing_state = CellType.WALL
                            case pygame.BUTTON_RIGHT:
                                self.placing_state = CellType.EMPTY
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                                
                    
                    case pygame.MOUSEBUTTONUP:
                        self.placing_state = -1

            if self.pathfinder.solve_started:
                self.pathfinder.step_next()
            elif self.placing_state != -1:
                self.on_mouse_down()


def main() -> None:
    screen: pygame.Surface = pygame.display.set_mode((PathfinderApp.WIDTH, PathfinderApp.HEIGHT))
    app: Visualizer = PathfinderApp(screen)
    app.mainloop()
    pygame.quit()


if __name__ == "__main__":
    main()