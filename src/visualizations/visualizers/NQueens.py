import pygame

class NQueens_BitManip:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.reset()
    
    def reset(self) -> None:
        self.bitboard: int = 0
        self.history: list[int] = []        
        self.queens: list[int] = []
        self.queens_len: int = len(self.queens)
        self.start: int = 0

    def place(self, row: int, col: int) -> None:
        if self.bitboard & (1 << (row * self.n + col)): return
        self.queens.append(col)
        self.history.append(self.bitboard)
        self.queens_len += 1
        #Horizontal
        mask: int = int('1'*self.n, 2) << (row * self.n)
        #Vertical
        mask |= int(('0'*(self.n - 1) + '1')*self.n, 2) << col
        #Major Diagonal
        for i in range(self.n):
            diag = 1 << i
            if row < col:
                diag <<= col - row
            elif row > col:
                diag >>= row - col
            diag &= int('1'*self.n, 2)
            mask |= diag << i*self.n
        #Minor Diagonal
        for i in range(self.n):
            diag = 1 << (self.n - i - 1)
            if row + col + 1 < self.n:
                diag >>= self.n - row - col - 1
            elif row + col + 1 > self.n:
                diag <<= row + col - self.n + 1
            diag &= int('1'*self.n, 2)
            mask |= diag << i*self.n
        self.bitboard |= mask
    
    def get_possible(self, row: int, start: int = 0) -> list[int]:
        return [i for i in range(start, self.n) if not (self.bitboard & (1 << (row*self.n + i)))]

    def get_not_possible(self, row: int) -> list[int]:
        return [i for i in range(self.n) if (self.bitboard & (1 << (row*self.n + i)))]
    
    def next(self) -> None:
        possible: list[int] = self.get_possible(self.queens_len, self.start)
        if (not possible):
            self.bitboard = self.history.pop()
            self.start = self.queens.pop() + 1
            self.queens_len -= 1
            return
        self.place(self.queens_len, possible[0])
        self.start = 0
    
    def update(self) -> None:
        if self.queens_len < self.n:
            self.next()
            if self.queens_len == self.n:
                print("Solution: " + str(self.queens))
                return True
        return False

class NQueens:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.reset()
    
    def reset(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.history: list[list[list[int]]] = []
        self.queens: list[int] = []
        self.queens_len: int = len(self.queens)
        self.start: int = 0
    
    def update(self) -> bool:
        if self.queens_len < self.n:
            self.next()
            if self.queens_len == self.n:
                print("Solution: " + str(self.queens))
                return True
        return False
    
    def place(self, row: int, col: int) -> None:
        if self.board[row][col]: return
        self.queens.append(col)
        self.history.append([i[:] for i in self.board])
        self.queens_len += 1
        
        for i in range(self.n):
            self.board[row][i] = 1 # Horizontal
            self.board[i][col] = 1 # Vertical
        
        # Major Diagonal
        diag: int = min(row, col)
        diag_row: int = row - diag
        diag_col: int = col - diag
        for i in range(self.n):
            if diag_row >= self.n or diag_col >= self.n: break
            self.board[diag_row][diag_col] = 1
            diag_row += 1
            diag_col += 1
        
        # Minor diagonal
        diag = min(row, self.n - col - 1)
        diag_row = row - diag
        diag_col = col + diag
        for i in range(self.n):
            if diag_row >= self.n or diag_col < 0: break
            self.board[diag_row][diag_col] = 1
            diag_row += 1
            diag_col -= 1
    
    def get_possible(self, row: int, start: int = 0) -> list[int]:
        return [i for i in range(start, self.n) if not self.board[row][i]]

    def get_not_possible(self, row: int) -> list[int]:
        return [i for i in range(self.n) if self.board[row][i]]

    def next(self) -> None:
        possible: list[int] = self.get_possible(self.queens_len, self.start)
        if (not possible):
            self.board = self.history.pop()
            self.start = self.queens.pop() + 1
            self.queens_len -= 1
            return
        self.place(self.queens_len, possible[0])
        self.start = 0

class App:
    n: int = 8
    cell_size: int = 50
    surf_size: int = n*cell_size
    def __init__(self, WIN: pygame.Surface) -> None:
        print("Starting the N-Queens Visualisation")
        
        # self.vis: NQueens | NQueens_BitManip = NQueens_BitManip(self.n)
        self.vis: NQueens | NQueens_BitManip = NQueens(App.n)

        self.WIN: pygame.Surface = WIN
        pygame.display.set_caption("N-Queens Visualisation")

        self.img: pygame.Surface = pygame.image.load("assets\\W_Queen.png")
        self.img.set_colorkey((181, 230, 29))
        self.img = pygame.transform.scale(self.img, (App.cell_size, App.cell_size))

        self.surf: pygame.Surface = pygame.Surface((App.surf_size, App.surf_size))
        self.rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.rect.center = (win_rect.width//2, win_rect.height//2)

        self.board: pygame.Surface = pygame.Surface((App.surf_size, App.surf_size))
        self.board.fill((235, 236, 208))

        for r in range(App.n):
            for c in range(App.n):
                if (r + c)%2 == 0: continue
                pygame.draw.rect(self.board, (119, 149, 86), (c*App.cell_size, r*App.cell_size, App.cell_size, App.cell_size))

        self.timer: int = 0
        self.time: int = 500
    
    def draw_queens(self) -> None:
        for row, col in enumerate(self.vis.queens):
            self.surf.blit(self.img, (col*App.cell_size, row*App.cell_size))
    
    def draw_queen_moves(self) -> None:
        for r in range(App.n):
            for c in self.vis.get_not_possible(r):
                pygame.draw.rect(self.surf, (255, 0, 0), (c*App.cell_size, r*App.cell_size, App.cell_size, App.cell_size))

    def draw(self) -> None:
        self.surf.blit(self.board, (0, 0))
        self.draw_queen_moves()
        self.draw_queens()
        self.WIN.blit(self.surf, self.rect)
        pygame.display.update()
    
    def test_time(self) -> None:
        from time import time
        vis_bitm: NQueens_BitManip = NQueens_BitManip(App.n)
        start: int = time()
        while not vis_bitm.update():
            pass
        end: int = time()
        print(f"BitManipulation took {end - start}")

        vis_norm: NQueens = NQueens(self.n)
        start = time()
        while not vis_norm.update():
            pass
        end = time()
        print(f"Normal took: {end - start}")

    def mainloop(self) -> bool:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                return True
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case 4:
                                self.time = max(self.time - 10, 1)
                            case 5:
                                self.time += 10

            self.timer += 1
            if self.timer >= self.time:
                self.vis.update()
                self.timer %= self.time
            self.draw()
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualisation")

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.surf_size, App.surf_size))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()