import pygame

class App:
    def __init__(self, WIN: pygame.Surface) -> None:
        self.WIN: pygame.Surface = WIN
        print("Starting Sudoku")
        print("ESC to quit")
        print("ENTER to start|pause solving")
        print("R to reset")
        print("SCROLL_WHEEL_UP|SCROLL_WHEEL_DOWN to change the placing number")
        print("LEFT_CLICK to place the seleced number")
        pygame.display.set_caption("Sudoku - Backtracking")
        
        self.cell_size: int = 50
        self.surf_size: int = self.cell_size*10
        self.surf: pygame.Surface = pygame.Surface((self.surf_size, self.surf_size))
        
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.surf_rect.center = (win_rect.width//2, win_rect.height//2)

        self.typeface: str = "freesansbold.ttf"
        self.font: pygame.Font = pygame.font.Font(self.typeface, self.cell_size)
        self.texts: dict[str] = {i: self.font.render(f'{i}', True, (0, 0, 0)) for i in range(10)}
        self.texts["speed"] = self.font.render("Speed", True, (0, 0, 0))

        self.selected_num: int = 1
        self.solving_speed: int = 0
        self.solving_speeds: dict[int: int] = [30, 60, 0]
        self.reset()
    
    def reset(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.solving: bool = False
        self.reset_solve()
    
    def reset_solve(self) -> None:
        self.solving_row: int = 0
        self.solving_col: int = 0
        self.solving_num: int = 1
        self.solving_history: list[tuple[int]] = []
    
    def get_valid_nums(self, row: int, col: int, num: int = 1) -> list[int]:
        return [i for i in range(num, 10) if self.is_valid(i, row, col)]

    def solving_next_pos(self) -> None:
        self.solving_col += 1
        if self.solving_col >= 9:
            self.solving_row += 1
            self.solving_col = 0
    
    def next(self) -> None:
        if self.solving_row >= 9:
            self.solving = False
            self.reset_solve()
            return
        if self.board[self.solving_row][self.solving_col]:
            self.solving_next_pos()
            return
        valid_nums: list[int] = self.get_valid_nums(self.solving_row, self.solving_col, self.solving_num)
        if valid_nums:
            num = valid_nums[0]
            self.board[self.solving_row][self.solving_col] = num
            self.solving_history.append((self.solving_row, self.solving_col, num))
            self.solving_num = 1
            self.solving_next_pos()
        else:
            self.solving_row, self.solving_col, self.solving_num = self.solving_history.pop()
            self.board[self.solving_row][self.solving_col] = 0
            self.solving_num += 1
    
    def mainloop(self) -> bool:
        clock: pygame.Clock = pygame.time.Clock()
        while True:
            clock.tick(self.solving_speeds[self.solving_speed])
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
                                if self.solving: self.reset_solve()
                            case pygame.K_r:
                                self.reset()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELUP:
                                self.selected_num = self.selected_num - 1 if self.selected_num > 0 else 9
                            case pygame.BUTTON_WHEELDOWN:
                                self.selected_num = (self.selected_num + 1)%10
                            case pygame.BUTTON_LEFT:
                                pos: tuple[int] = pygame.mouse.get_pos()
                                row: int = (pos[1] - self.surf_rect.y)//self.cell_size
                                col: int = (pos[0] - self.surf_rect.x)//self.cell_size
                                if 0 <= row < 9 and 0 <= col < 9 and not self.board[row][col]:
                                    self.place(self.selected_num, row, col)
                                elif row == 9 and 3 <= col < 3 + len(self.solving_speeds):
                                    self.solving_speed = col - 3
            if self.solving:
                self.next()
            self.draw()
    
    def is_valid(self, num: int, row: int, col: int) -> bool:
        start_row: int = (row//3)*3
        start_col: int = (col//3)*3
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num or self.board[start_row + i//3][start_col + i%3] == num:
                return False
        return True

    def place(self, num: int, row: int, col: int) -> None:
        if not self.is_valid(num, row, col): return
        self.board[row][col] = num

    def draw_grid(self):
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.surf, (0,0,0), (i*self.cell_size, 0), (i*self.cell_size, self.surf_size - self.cell_size), thickness)
            pygame.draw.line(self.surf, (0,0,0), (0, i*self.cell_size), (self.surf_size - self.cell_size, i*self.cell_size), thickness)
    
    def blit_num(self, num: int, row: int, col: int) -> int:
        self.surf.blit(self.texts[num], ((col + 0.25)*self.cell_size, (row + 0.1)*self.cell_size))

    def draw_board(self) -> None:
        if self.solving:
            for row, col, _ in self.solving_history:
                pygame.draw.rect(self.surf, (255, 165, 0), (col*self.cell_size, row*self.cell_size, self.cell_size, self.cell_size))
        
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if not col: continue
                self.blit_num(col, i, j)
                
    def draw(self) -> None:
        self.surf.fill((255, 255, 255))
        pygame.draw.rect(self.surf, (0, 255, 0), (self.cell_size*9, self.cell_size*self.selected_num, self.cell_size, self.cell_size))
        for i in range(10):
            self.blit_num(i, i, 9)
        self.draw_grid()
        self.draw_board()
        self.surf.blit(self.texts["speed"], (0, self.cell_size*9))
        pygame.draw.rect(self.surf, (0, 255, 0), ((3 + self.solving_speed)*self.cell_size, 9*self.cell_size, self.cell_size, self.cell_size))
        for i in range(len(self.solving_speeds)):
            self.blit_num(i, 9, 3 + i)
        pygame.display.update(self.WIN.blit(self.surf, self.surf_rect))
        
    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")

if __name__ == "__main__":
    pygame.init()
    WIN: pygame.Surface = pygame.display.set_mode((500, 500))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()