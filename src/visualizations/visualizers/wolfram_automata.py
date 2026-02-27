'''
Cellular Automata (1D) : Wolfram
'''
import pygame
from visualizations.utils import HSV_to_RGB, remap
from math import pi, cos, sin

from .visualizer import Visualizer

class WolframAutomataApp(Visualizer):
    NAME: str = "Wolfram"
    ROWS: int = 720
    COLS: int = 1000
    SIDE: int = 1
    WIDTH: int = COLS * SIDE
    HEIGHT: int = ROWS * SIDE
    COLORS: tuple[int] = [(255, 255, 255), (0, 0, 0)]
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        
        self.row: int = 0
        self.get_color = self.get_color_1

        self.running: bool = False
        self.is_tab_down: bool = False
        self.new_rule: str = ""

        self.fps: int = 60

        self.change_rule(90)

        WolframAutomataApp._print_instructions()
    
    @staticmethod
    def _print_instructions() -> None:
        print("Starting 1D Wolfram Cellular Automata")
        print("ESC to Quit")
        print("ENTER to start/pause the simulation")
        print("UP_ARROW | RIGHT_ARROW to increase the rule no.")
        print("DOWN_ARROW | LEFT_ARROW to decrease the rule no.")
        print("[HOLD TAB] enter number [RELEASE TAB] to change rule to that no.")
        print("S to save the rule image into 'assets' folder")
        print("SCROLL_WHEEL_UP")
    
    def change_rule(self, new_rule: str):
        self.surface.fill(self.get_color(True))
        self.reset_list()
        self.row = 0
        self.load_rules(new_rule)
        self.draw()
        pygame.display.set_caption(f"Wolfram Cellular Automata: Rule-{self.rule_num}")

    def load_rules(self, rule_num: int):
        self.rule_num: int = rule_num
        self.rules = []
        for _ in range(8):
            self.rules.append(rule_num & 1)
            rule_num >>= 1
    
    def get_color_1(self, bg: bool = False, col = None):
        return WolframAutomataApp.COLORS[int(bg)]
    
    def get_color_2(self, bg: bool = False, col: int = None) -> list[int]:
        if bg: return (0, 0, 0)
        h = (self.row)%360
        if col:
            s = abs(cos(pi*(self.COLS/2 - col)/180))
            s = remap(0, 1, 0.3, 1, s)
            h = remap(0, 1, 0, 360, sin(pi*h/180))
        else: s = 1
        c = [int(i) for i in HSV_to_RGB(h, s, 1)]
        return c
    
    def apply_rules(self, n1, n2, n3) -> int:
        return self.rules[n1*4 + n2*2 + n3]

    def get_neighbors(self, i) -> list[int]:
        return [self.list[i-1], self.list[i], (self.list[(i+1)%self.COLS])]

    def reset_list(self):
        self.list = [0 for i in range(self.COLS)]
        self.list[self.COLS//2] = 1
    
    def step_next(self):
        if self.row >= self.ROWS:
            return
        next_list: list[int] = []

        self.row += 1
        for i in range(self.COLS):
            next_list.append(self.apply_rules(*self.get_neighbors(i)))
        self.list = next_list
        self.draw()
    
    def draw(self):
        for i, val in enumerate(self.list):
            if val == 0:
                continue
            pygame.draw.rect(self.surface, self.get_color(col = i), (i*self.SIDE, self.row*self.SIDE, self.SIDE, self.SIDE))
        
        self.update_screen()
    
    def save_surface(self) -> None:
        pygame.image.save(self.surface, f".\\assets\\WCA\\rule_{self.rule_num}.png")
    
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
                                self.is_tab_down = True
                                self.new_rule = ""
                            case pygame.K_UP | pygame.K_RIGHT:
                                self.change_rule((self.rule_num+1)%256)
                            case pygame.K_DOWN | pygame.K_LEFT:
                                self.change_rule((self.rule_num-1) if self.rule_num > 0 else 255)
                            case pygame.K_s:
                                self.save_surface()
                            case _:
                                if self.is_tab_down and event.unicode.isdigit():
                                    self.new_rule += event.unicode
                    
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_TAB:
                                if self.new_rule:
                                    self.is_tab_down = False
                                    self.change_rule(int(self.new_rule))
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELDOWN:
                                self.fps = max(self.fps - 10, 0)
                            case pygame.BUTTON_WHEELUP:
                                self.fps += 10

            if self.running:
                self.step_next()

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((WolframAutomataApp.WIDTH, WolframAutomataApp.HEIGHT))
    app: WolframAutomataApp = WolframAutomataApp(WIN)
    app.mainloop()
    pygame.quit()