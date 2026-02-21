import pygame, os, random
from utils import blitRotateCenter
class Tile:
    images: tuple[pygame.Surface] = None
    all_images: dict[str: tuple[pygame.Surface]] = {}
    connections: tuple[tuple[int]] #Up left down right
    all_connections: dict[str: tuple[tuple[int]]] = {}
    type_name: str
    type_names: list[str] = []
    colors: list[pygame.Color] = []

    def __init__(self, index: int) -> None:
        self.index: int = -1
    
    @classmethod
    def load_all_tilesets(cls) -> None:
        path: str = ".\\assets\\WFC"
        for f in os.listdir(path):
            cls.load_tileset(f.split('.')[0], f"{path}\\{f}")
            if cls.images is None:
                cls.images = cls.all_images[cls.type_name]
                cls.connections = cls.all_connections[cls.type_name]

    @classmethod
    def load_tileset(cls, fname: str, path: str) -> None:
        name, dims = fname.split('_')
        if not cls.type_names: cls.type_name = name
        cls.type_names.append(name)
        
        cols, num_tiles = map(int, dims.split('x'))
        tileset: pygame.Surface = pygame.image.load(path)
        cls.all_images[name] = []
        cls.all_connections[name] = []

        for i in range(num_tiles):
            cls.load_image(name, tileset, App.SIZE*(i%cols), App.SIZE*(i//cols))

        cls.all_images[name] = tuple(cls.all_images[name])
        cls.all_connections[name] = tuple(cls.all_connections[name])
    
    @classmethod
    def load_image(cls, name: str, tileset: pygame.Surface, x: int, y: int) -> None:
        tiles: list[pygame.Surface] = [pygame.Surface((App.SIZE, App.SIZE))]
        tiles[0].blit(tileset, (-x, -y))
        connections: list[tuple[int]] = [cls.get_connections(tiles[0])]

        for _ in range(3):
            new_tile: pygame.Surface = pygame.transform.rotate(tiles[-1], 90)
            conn: tuple[int] = cls.get_connections(new_tile)
            if conn in connections: break
            connections.append(conn)
            tiles.append(new_tile)

        connections: tuple[tuple[int]] = tuple(connections)
        cls.all_images[name].extend(tiles)
        cls.all_connections[name].extend(connections)
    
    @classmethod
    def get_connections(cls, tile: pygame.Surface) -> tuple[int]:
        connections: list[int] = []

        for d in range(4):
            connections.append([])
            for x, y in App.POSS[d]:
                color: pygame.Color = tile.get_at((x, y))
                if color not in cls.colors: cls.colors.append(color)
                color_id: int = cls.colors.index(color)
                connections[-1].append(color_id)
            connections[-1] = tuple(connections[-1])
        return tuple(connections)

    @classmethod
    def check_connections(cls, from_tile: int, to_tile: int, dir: int) -> bool:
        from_connections = cls.connections[from_tile][dir]
        to_connections = cls.connections[to_tile][dir^2]
        return all(i == j for i, j in zip(from_connections, to_connections))
    
    @classmethod
    def change_type(cls) -> None:
        cls.type_name = cls.type_names[(cls.type_names.index(cls.type_name) + 1)%len(cls.type_names)]
        cls.connections = cls.all_connections[cls.type_name]
        cls.images = cls.all_images[cls.type_name]

class Cell:
    def __init__(self, row: int, col: int):
        self.collapsed: bool = False
        self.options: list[int] = [i for i in range(App.MAXENTROPY)]
        self.row: int = row
        self.col: int = col
        self.tile: Tile = None
    
    def collapse(self) -> int:
        self.collapsed = True
        self.options = [random.choice(self.options)] if self.options else [0]
        self.tile = Tile.images[self.options[0]]
        return self.options[0]
    
    def update(self, from_dir: int, val: int) -> None:
        for i in self.options[:]:
            if not Tile.check_connections(val, i, from_dir):
                self.options.remove(i)
    
    def getInfoImg(self) -> pygame.Surface:
        infoImg: pygame.Surface = pygame.Surface((App.SIZE, App.SIZE))
        infoImg.fill((255,0,0))
        infoImg.blit(App.font.render(str(len(self.options)), True, (255, 255, 255)), (0, 0))
        return infoImg
    
    def __repr__(self) -> str:
        return f"Cell(({self.row}, {self.col}), {self.options})"

class App:
    ROWS: int = 12
    COLS: int = 18
    SIZE: int = 56
    HALF_SIZE: int = SIZE//2
    WIDTH: int = COLS * SIZE
    HEIGHT: int = ROWS * SIZE

    DEBUG: bool = False
    POSS: tuple = (((0, 0), (HALF_SIZE, 0), (SIZE - 1, 0)), ((0, 0), (0, HALF_SIZE), (0, SIZE - 1)), ((0, SIZE - 1), (HALF_SIZE, SIZE - 1), (SIZE - 1, SIZE - 1)), ((SIZE - 1, 0), (SIZE - 1, HALF_SIZE), (SIZE - 1, SIZE - 1)))

    MAXENTROPY: int
    DEFAULT: int = 1
    def __init__(self, WIN: pygame.Surface):
        self.WIN: pygame.Surface = WIN
        Tile.load_all_tilesets()
        App.MAXENTROPY = len(Tile.images)

        self.fps: int = 0
        self.clock = pygame.time.Clock()

        App.font: pygame.Font = pygame.font.Font("freesansbold.ttf", App.SIZE//2)

        pygame.display.set_caption("Wave Function Collapse")
        self.surf: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        self.surf_rect: pygame.Rect = self.surf.get_rect()
        win_rect: pygame.Rect = WIN.get_rect()
        self.surf_rect.center = (win_rect.width//2, win_rect.height//2)

        self.reset()
    
    def reset(self):
        self.resetGrid()
        self.surf.fill((255, 255, 255))
        self.update_win()
    
    def debug_draw(self) -> None:
        for i, img in enumerate(Tile.images):
            self.surf.blit(img, (App.SIZE*(i%App.COLS), App.SIZE*(i//App.COLS)))
    
    def update_neighbours(self, row, col, val):
        for i, dir in enumerate([[-1, 0], [0, -1], [1, 0], [0, 1]]):
            nrow, ncol = row+dir[0], col+dir[1]
            if 0 <= nrow < App.ROWS and 0 <= ncol < App.COLS and not self.grid[nrow][ncol].collapsed:
                self.grid[nrow][ncol].update(i, val)
    
    def get_least_entropy(self):
        self.least_entropy = self.MAXENTROPY
        self.collapsable_cells: list[Cell] = []
        for row in self.grid:
            for cell in row:
                if cell.collapsed or len(cell.options) < 1: continue
                elif len(cell.options) < self.least_entropy:
                    self.least_entropy = len(cell.options)
                    self.collapsable_cells = [cell]
                elif len(cell.options) == self.least_entropy:
                    self.collapsable_cells.append(cell)
        if self.least_entropy == self.MAXENTROPY:
            r: int = random.randrange(App.ROWS)
            c: int = random.randrange(App.COLS)
            self.collapsable_cells = [self.grid[r][c]]

    def next(self):
        self.get_least_entropy()
        if not len(self.collapsable_cells): return
        cell = self.collapsable_cells.pop(random.randrange(len(self.collapsable_cells)))
        if (len(cell.options)):
            self.update_neighbours(cell.row, cell.col, cell.collapse())
        self.draw(cell)
    
    def resetGrid(self) -> None:
        self.grid: list[list[Cell]] = [[Cell(i ,j) for j in range(App.COLS)] for i in range(App.ROWS)]
    
    def draw(self, cell: Cell) -> None:
        if cell.tile is None: return
        self.surf.blit(cell.tile, (cell.col*App.SIZE, cell.row*App.SIZE))
        self.update_win()
    
    def update_win(self) -> None:
        pygame.display.update(self.WIN.blit(self.surf, self.surf_rect))

    # def draw(self, cell: Cell) -> None:
    #     pygame.display.update(WIN.blit(cell.tile.img if cell.tile else Tile.TILES[self.DEFAULT].img, (cell.col*App.SIDE, cell.row*App.SIDE)))
    #     if App.DEBUG:
    #         for row in self.grid:
    #             for c in row:
    #                 if not c.collapsed: WIN.blit(c.getInfoImg(), (c.col*App.SIDE, c.row*App.SIDE))
    #         pygame.display.update()
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")
    
    def mainloop(self) -> bool:
        print("Starting Wave Function Collapse")
        print("ESC to Quit")
        print("Enter to reset")
        print("TAB to step by one in DEBUG mode")
        print("D to enter/exit DEBUG mode")
        print("SCROLL_WHEEL_UP to increase speed")
        print("SCROLL_WHEEL_UP to decrease speed")
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                return True
                            case pygame.K_RETURN:
                                self.reset()
                            case pygame.K_TAB:
                                self.next()
                            case pygame.K_d:
                                App.DEBUG = not App.DEBUG
                                if App.DEBUG:
                                    self.reset()
                            case pygame.K_c:
                                Tile.change_type()
                                self.reset()

                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case 4: self.fps += 10
                            case 5: self.fps = self.fps-10 if self.fps > 15 else max(self.fps-1, 0)
                        
            if not App.DEBUG: self.next()

if __name__ == "__main__":
    pygame.init()
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()