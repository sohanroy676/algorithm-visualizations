'''
Visualizing the Sorting algorithms [BubbleSort, SelectionSort]
'''
import pygame
from random import randint

class Sort:
    types = ["Bubble", "Selection"]
    def __init__(self, _typeIdx):
        self.reset()
        self._typeIdx = _typeIdx
        pygame.display.set_caption(str(self))

    def reset(self):
        self.isSorting: bool = False
        self.getRandomList()
    
    def getRandomList(self):
        self.lst: list[int] = [randint(10, App.HEIGHT-10) for i in range(App.LEN)]

    def changeType(self):
        return eval(f"{Sort.types[(self._typeIdx+1)%len(Sort.types)]}Sort()")
    
    def __str__(self):
        return f"{Sort.types[self._typeIdx]}Sort"

class BubbleSort(Sort):
    def __init__(self):
        super().__init__(0)

    def reset(self):
        super().reset()
        self.i = self.j = -1
        self.drawLst()
    
    def drawLst(self):
        App.instance.SURF.fill(App.COLORS["bg"])
        for i, h in enumerate(self.lst):
            pygame.draw.rect(App.instance.SURF, App.COLORS["bar"] if i < App.LEN - self.i else App.COLORS["sorted"], (i*App.SIDE, App.HEIGHT-h, App.SIDE, h))
        if self.j >= 0:
            h = self.lst[self.j]
            pygame.draw.rect(App.instance.SURF, App.COLORS["select"], (self.j*App.SIDE, App.HEIGHT-h, App.SIDE, h))
        App.instance.update()

    def start(self):
        self.i = self.j = 0
    
    def next(self):
        if self.lst[self.j] > self.lst[self.j+1]:
            self.lst[self.j], self.lst[self.j+1] = self.lst[self.j+1], self.lst[self.j]
        
        self.j += 1
        if self.j >= App.LEN - self.i - 1:
            self.j = 0
            self.i += 1
            if self.i > App.LEN - 1:
                self.isSorting = False
                self.j = -1
        
        self.drawLst()

class SelectionSort(Sort):
    def __init__(self):
        super().__init__(1)
        
    def reset(self):
        super().reset()
        self.i = self.j = -1
        self.drawLst()
    
    def drawLst(self):
        App.instance.SURF.fill(App.COLORS["bg"])
        for i, h in enumerate(self.lst):
            pygame.draw.rect(App.instance.SURF, App.COLORS["bar"] if i > self.i else App.COLORS["sorted"], (i*App.SIDE, App.HEIGHT-h, App.SIDE, h))
        if self.j > 0:
            try:
                pygame.draw.rect(App.instance.SURF, App.COLORS["select"], (self.j*App.SIDE, App.HEIGHT-self.lst[self.j], App.SIDE, self.lst[self.j]))
            except IndexError:
                print(self.i, self.j)
            pygame.draw.rect(App.instance.SURF, App.COLORS["select"], (self.i*App.SIDE, App.HEIGHT-self.lst[self.i], App.SIDE, self.lst[self.i]))
        App.instance.update()

    def start(self):
        self.i = 0
        self.j = self.i + 1
    
    def next(self):
        if self.lst[self.i] > self.lst[self.j]:
            self.lst[self.i], self.lst[self.j] = self.lst[self.j], self.lst[self.i]
        
        self.j += 1
        if self.j >= App.LEN:
            self.i += 1
            self.j = self.i + 1
            if self.i >= App.LEN - 1:
                self.isSorting = False
                self.j = -1
        
        self.drawLst()

class App:
    WIDTH: int = 800
    HEIGHT: int = 600
    LEN: int = 200
    SIDE: int = WIDTH//LEN
    FPS: int = 60

    COLORS: dict[str: tuple[int]] = {"bg": (0, 0, 0), "bar": (230, 230, 230), "select": (255, 0 , 0), "sorted": (0, 255, 0)}

    instance = None

    def __init__(self, WIN: pygame.Surface) -> None:
        App.instance = self
        self.WIN: pygame.Surface = WIN
        WINRect: pygame.Rect = self.WIN.get_rect()
        self.SURF: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        pygame.display.set_caption("Sorting")

        self.blitPos: tuple[int] = ((WINRect.width - App.WIDTH)//2, (WINRect.height - App.HEIGHT)//2)

        self.clock = pygame.time.Clock()
        self.sort: Sort = SelectionSort()

    def update(self) -> None:
        pygame.display.update(self.WIN.blit(self.SURF, self.blitPos))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualizations")

    def mainloop(self) -> bool:
        print("Starting the visualisation of Sorting Algorithms")
        print("ESC to Quit")
        print("ENTER to start/pause sorting")
        print("R to reset")
        print("C | SPACE | TAB to change the sorting algorithm")
        print("SCROLL_WHEEL_UP to increase the speed of sorting")
        print("SCROLL_WHEEL_DOWN to decrease the speed of sorting")
        while True:
            self.clock.tick(App.FPS)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT: return False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.sort.isSorting = not self.sort.isSorting
                                if self.sort.isSorting:
                                    self.sort.start()
                            case pygame.K_r:
                                if not self.sort.isSorting:
                                    self.sort.reset()
                            case (pygame.K_c | pygame.K_SPACE | pygame.K_TAB):
                                if not self.sort.isSorting:
                                    self.sort = self.sort.changeType()

                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case 4: App.FPS += 10
                            case 5: App.FPS = max(App.FPS-10, 0)
                                
            if self.sort.isSorting:
                self.sort.next()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()