import pygame
from visualizations.utils import HSV_to_RGB, Vector2, remap
from .visualizer import Visualizer

class HilbertCurve:
    def __init__(self, order: int) -> None:
        self.set_order(order)
        self.reset()

    def set_order(self, order: int) -> None:
        self.order: int = order
        self.n: int = pow(2, order)
        self.points: int = self.n*self.n
    
    def reset(self) -> None:
        self.index: int = 0
        self.done: bool = False
    
    def get_point(self, i: int) -> Vector2:
        points: list[Vector2] = [Vector2(0, 0), Vector2(0, 1), Vector2(1, 1), Vector2(1, 0)]
        idx: int = i & 3
        point: Vector2 = points[idx]
        for j in range(1, self.order):
            length = pow(2, j)
            i >>= 2
            idx = i & 3
            if idx == 0: 
                point.x, point.y = point.y, point.x
            elif idx == 1:
                point.y += length
            elif idx == 2:
                point.y += length
                point.x += length
            elif idx == 3:
                point.x, point.y = length - point.y - 1, length - point.x - 1
                point.x += length
        return point

    def get_next_point(self) -> Vector2 | None:
        point: Vector2 = self.get_point(self.index)
        self.index += 1
        if self.index >= self.points:
            self.done = True
        return point


class HilbertCurveApp(Visualizer):
    NAME = "Hilbert"
    ORDER: int = 8
    SURFDIM: int = pow(2, ORDER+1)
    WIDTH: int = SURFDIM
    HEIGHT: int = SURFDIM

    def __init__(self, window: pygame.Surface) -> None:
        super().__init__(window)
        self.surface.fill((0, 0, 0))
        self.fps: int = 60

        self.hilber_curve: HilbertCurve = HilbertCurve(self.ORDER)
        self.line_length: int = 2
        self.prev_point: Vector2 = self.get_point()

        HilbertCurveApp.show_instructions()
    
    @staticmethod
    def show_instructions() -> None:
        print("Starting the visualisation for an N-order Hilbert Curve")
        print("S to save the image of the generated curve into 'assets' folder")

    def get_point(self) -> Vector2:
        point: Vector2 = self.hilber_curve.get_next_point()
        point *= self.line_length
        point += Vector2(self.line_length/2, self.line_length/2)
        return point

    def next_line(self) -> None:
        next_point: Vector2 = self.get_point()
        pygame.draw.line(self.surface, self.get_color(), tuple(self.prev_point), tuple(next_point))
        self.prev_point = next_point

    def get_color(self) -> tuple[int]:
        return HSV_to_RGB(remap(0, self.hilber_curve.points, 0, 360, self.hilber_curve.index), 1, 1)

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.fps)
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
                            case pygame.K_s:
                                pygame.image.save(self.SURF, f".\\assets\\hilbert_curve_{self.ORDER}.png")
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELUP: self.fps += 10
                            case pygame.BUTTON_WHEELDOWN: self.fps = max(self.fps-10, 0)

            if not self.hilber_curve.done:
                self.next_line()
            
            self.update_screen()

if __name__ == "__main__":
    window: pygame.Surface = pygame.display.set_mode((HilbertCurveApp.SURFDIM, HilbertCurveApp.SURFDIM))
    app: HilbertCurveApp = HilbertCurveApp(window)
    app.mainloop()
    pygame.quit()