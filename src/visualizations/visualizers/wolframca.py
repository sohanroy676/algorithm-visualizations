'''
Cellular Automata (1D) : Wolfram
'''
import pygame
from utils import HSVToRGB, remap
from math import pi, cos, sin

class App:
    fps: int = 60
    ROWS: int = 800
    COLS: int = 1000
    SIDE: int = 1
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE
    COLORS: tuple[int] = [(255, 255, 255), (0, 0, 0)]
    def __init__(self, WIN: pygame.Surface):
        print("Starting 1D Wolfram Cellular Automata")
        print("ESC to Quit")
        print("ENTER to start/pause the simulation")
        print("UP_ARROW | RIGHT_ARROW to increase the rule no.")
        print("DOWN_ARROW | LEFT_ARROW to decrease the rule no.")
        print("[HOLD TAB] enter number [RELEASE TAB] to change rule to that no.")
        print("S to save the rule image into 'assets' folder")
        print("SCROLL_WHEEL_UP")

        self.running: bool = False
        self.row: int = 0
        self.getColor = self.getColor2

        self.tabDown: bool = False
        self.newRule: str = ""
        self.clock = pygame.time.Clock()

        self.WIN: pygame.Surface = WIN
        self.surf: pygame.Surface = pygame.Surface((App.WIDTH, App.HEIGHT))
        win_rect: pygame.Rect = WIN.get_rect()
        self.rect: pygame.Rect = self.surf.get_rect()
        self.rect.center = (win_rect.width//2, win_rect.height//2)

        self.changeRule(0)
    
    def changeRule(self, newRule):
        self.surf.fill(self.getColor(True))
        self.resetList()
        self.row = 0
        self.loadRules(newRule)
        self.draw()
        pygame.display.set_caption(f"Wolfram Cellular Automata: Rule-{self.ruleNum}")

    def loadRules(self, ruleNum):
        self.ruleNum = ruleNum
        self.rules = []
        for _ in range(8):
            self.rules.append(ruleNum & 1)
            ruleNum >>= 1
    
    def getColor1(self, bg: bool = False, col: int = None):
        return App.COLORS[int(bg)]
    
    def getColor2(self, bg: bool = False, col: int = None) -> list[int]:
        if bg: return (0, 0, 0)
        h = (self.row)%360
        if col:
            s = abs(cos(pi*(App.COLS/2 - col)/180))
            s = remap(0, 1, 0.3, 1, s)
            h = remap(0, 1, 0, 360, sin(pi*h/180))
        else: s = 1
        c = [int(i) for i in HSVToRGB(h, s, 1)]
        return c
    
    def applyRules(self, n1, n2, n3) -> int:
        return self.rules[n1*4 + n2*2 + n3]

    def getNeighbors(self, i) -> list[int]:
        return [self.list[i-1], self.list[i], (self.list[(i+1)%App.COLS])]

    def resetList(self):
        self.list = [0 for i in range(App.COLS)]
        self.list[App.COLS//2] = 1
    
    def next(self):
        if self.row >= App.ROWS:
            return
        nextList = []

        self.row += 1
        for i in range(App.COLS):
            nextList.append(self.applyRules(*self.getNeighbors(i)))
        self.list = nextList[:]
        self.draw()
    
    def draw(self):
        for i, val in enumerate(self.list):
            if val:
                pygame.draw.rect(self.surf, self.getColor(col = i), (i*App.SIDE, self.row*App.SIDE, App.SIDE, App.SIDE))
        pygame.display.update(self.WIN.blit(self.surf, self.rect))
    
    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")
    
    def mainloop(self) -> None:
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
                                self.running = not self.running
                            case pygame.K_TAB:
                                self.tabDown = True
                                newRule = ""
                            case pygame.K_UP | pygame.K_RIGHT:
                                self.changeRule((self.ruleNum+1)%256)
                            case pygame.K_DOWN | pygame.K_LEFT:
                                self.changeRule((self.ruleNum-1) if self.ruleNum > 0 else 255)
                            case pygame.K_s:
                                pygame.image.save(self.surf, f"assets\\wca{self.ruleNum}.png")
                            case _:
                                if self.tabDown and event.unicode.isdigit():
                                    newRule += event.unicode
                    
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_TAB:
                                if newRule:
                                    self.tabDown = False
                                    self.changeRule(int(newRule))
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10

            if self.running:
                self.next()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()