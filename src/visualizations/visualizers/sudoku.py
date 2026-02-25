'''
Sudoku + Solver with backtracking algorithm
'''
import pygame
from .visualizer import Visualizer

class Sudoku:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.reset_solve()
    
    def reset_solve(self) -> None:
        self.solving_row: int = 0
        self.solving_col: int = 0
        self.solving_num: int = 1
        self.solving_history: list[tuple[int, int, int]] = []
    
    def get_valid_nums(self) -> list[int]:
        # Gets all the valid numbers for a cell
        return [i for i in range(self.solving_num, 10) if self.is_valid(i, self.solving_row, self.solving_col)]

    def next_pos(self) -> None:
        # Go to the next cell position
        self.solving_col += 1
        if self.solving_col >= 9:
            self.solving_row += 1
            self.solving_col = 0
    
    def step_next(self) -> bool:
        if self.solving_row >= 9:
            self.reset_solve()
            return True
        
        # Skipping the cells which already have some value
        if self.board[self.solving_row][self.solving_col]:
            self.next_pos()
            return False
        
        valid_nums: list[int] = self.get_valid_nums()
        if valid_nums:
            # Place the smalles valid number and go to the next cell
            num = valid_nums[0]
            self.board[self.solving_row][self.solving_col] = num
            self.solving_history.append((self.solving_row, self.solving_col, num))
            self.solving_num = 1
            self.next_pos()
        else:
            # If a cell has no possible numbers, backtrack
            self.solving_row, self.solving_col, self.solving_num = self.solving_history.pop()
            self.board[self.solving_row][self.solving_col] = 0
            self.solving_num += 1
        
        return False
    
    def is_valid(self, num: int, row: int, col: int) -> bool:
        # Checks the row, col and the 3x3 grid
        start_row: int = (row//3)*3
        start_col: int = (col//3)*3
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num or self.board[start_row + i//3][start_col + i%3] == num:
                return False
        return True

    def place(self, num: int, row: int, col: int) -> None:
        if num > 0 and not self.is_valid(num, row, col): return
        self.board[row][col] = num


class SudokuApp(Visualizer):
    NAME: str = "Sudoku"
    CELL_SIZE: int = 50
    SURFACE_SIZE: int = CELL_SIZE*10
    WIDTH: int = SURFACE_SIZE
    HEIGHT: int = SURFACE_SIZE
    
    TYPEFACE: str = "freesansbold.ttf"
    COLORS: dict[str, tuple[int, int, int]] = {"fg": (0, 0, 0), "bg": (255, 255, 255), "history": (255, 165, 0), "selected": (0, 255, 0)}

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Initializing the font and text Surfaces
        self.font: pygame.Font = pygame.font.Font(SudokuApp.TYPEFACE, SudokuApp.CELL_SIZE)
        self.texts: dict[str, pygame.Surface] = {i: self.font.render(f'{i}', True, self.COLORS["fg"]) for i in range(10)}
        self.texts["speed"] = self.font.render("Speed", True, self.COLORS["fg"])

        self.sudoku: Sudoku = Sudoku()
        self.reset()

        self.selected_num: int = 1
        self.solving_speed_index: int = 0
        self.solving_speeds: dict[int: int] = [30, 60, 0]
        SudokuApp.__print_instructions()
    
    def reset(self) -> None:
        self.solving: bool = False
        self.sudoku.reset()
    
    @staticmethod
    def __print_instructions():
        print("Starting Sudoku")
        print("ESC to quit")
        print("ENTER to start|pause solving")
        print("R to reset")
        print("SCROLL_WHEEL_UP|SCROLL_WHEEL_DOWN to change the placing number")
        print("LEFT_CLICK to place the seleced number")
    
    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.solving_speeds[self.solving_speed_index])
            
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.quit()
                        return False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.solving = not self.solving
                                if self.solving: self.sudoku.reset_solve()
                            case pygame.K_r:
                                self.reset()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELUP:
                                self.selected_num = self.selected_num - 1 if self.selected_num > 0 else 9
                            case pygame.BUTTON_WHEELDOWN:
                                self.selected_num = (self.selected_num + 1)%10
                            case pygame.BUTTON_LEFT:
                                self.on_click()

            if self.solving:
                self.solving = not self.sudoku.step_next()
                
            self.draw()
    
    def on_click(self) -> None:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        row: int = (mouse_pos[1] - self.blit_pos.y)//self.CELL_SIZE
        col: int = (mouse_pos[0] - self.blit_pos.x)//self.CELL_SIZE
        if 0 <= row < 9 and 0 <= col < 9 and (self.selected_num == 0 or self.sudoku.board[row][col] == 0):
            self.sudoku.place(self.selected_num, row, col)
        elif row == 9 and 3 <= col < 3 + len(self.solving_speeds):
            self.solving_speed_index = col - 3

    def draw_grid(self) -> None:
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.surface, self.COLORS["fg"], (i*self.CELL_SIZE, 0), (i*self.CELL_SIZE, self.HEIGHT - self.CELL_SIZE), thickness)
            pygame.draw.line(self.surface, self.COLORS["fg"], (0, i*self.CELL_SIZE), (self.WIDTH - self.CELL_SIZE, i*self.CELL_SIZE), thickness)
    
    def blit_num(self, num: int, row: int, col: int) -> int:
        self.surface.blit(self.texts[num], ((col + 0.25)*self.CELL_SIZE, (row + 0.1)*self.CELL_SIZE))

    def draw_board(self) -> None:
        if self.solving:
            # Background for the cells which are placed by the backtracking algorithm
            for row, col, _ in self.sudoku.solving_history:
                pygame.draw.rect(self.surface, self.COLORS["history"], (col*self.CELL_SIZE, row*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
        
        for i, row in enumerate(self.sudoku.board):
            for j, col in enumerate(row):
                if not col: continue
                self.blit_num(col, i, j)

    def draw(self) -> None:
        self.surface.fill(self.COLORS["bg"])
        
        # Background for the selected number on the right numbers panel
        pygame.draw.rect(self.surface, self.COLORS["selected"], (self.CELL_SIZE*9, self.CELL_SIZE*self.selected_num, self.CELL_SIZE, self.CELL_SIZE))
        
        # Numbers for the right numbers panel
        for i in range(10):
            self.blit_num(i, i, 9)
        
        self.draw_grid()
        self.draw_board()
        self.surface.blit(self.texts["speed"], (0, self.CELL_SIZE*9))
        
        # Background for the selected speed
        pygame.draw.rect(self.surface, self.COLORS["selected"], ((3 + self.solving_speed_index)*self.CELL_SIZE, 9*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
        
        # Speed options
        for i in range(len(self.solving_speeds)):
            self.blit_num(i, 9, 3 + i)
        
        self.update_screen()

if __name__ == "__main__":
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((500, 500))
    app: SudokuApp = SudokuApp(screen)
    app.mainloop()
    pygame.quit()