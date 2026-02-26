'''
Visualizing the Sorting algorithms [BubbleSort, SelectionSort]
'''
import pygame
from random import randint
from abc import ABC, abstractmethod
from collections.abc import Callable
from .visualizer import Visualizer

type DrawCallback = Callable[[list[int], set[int] | None, set[int] | None], None]

class Sort(ABC):
    SORT_TYPE: str = "Sorting"
    def __init__(self, array_length: int, array_min: int, array_max: int, on_update: DrawCallback) -> None:
        self.array_length: int = array_length
        self.array_min: int = array_min
        self.array_max: int = array_max
        
        self.on_update: DrawCallback = on_update

        self.reset()

    def reset(self) -> None:
        self.is_sorting: bool = False
        self.get_random_array()
    
    def get_random_array(self) -> None:
        self.array: list[int] = [randint(self.array_min, self.array_max) for i in range(self.array_length)]

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def step_next(self) -> None:
        pass

class BubbleSort(Sort):
    SORT_TYPE: str = "BubbleSort"
    def reset(self) -> None:
        super().reset()

        self.index1: int = -1
        self.index2: int = -1
        self.sorted: set[int] = set()
        
        self.on_update(self.array)

    def start(self) -> None:
        self.index1 = self.array_length
        self.index2 = 0
    
    def step_next(self) -> None:
        if self.array[self.index2] > self.array[self.index2 + 1]:
            self.array[self.index2], self.array[self.index2 + 1] = self.array[self.index2 + 1], self.array[self.index2]
        
        self.on_update(self.array, selected = {self.index2, self.index2 + 1}, sorted = self.sorted)

        self.index2 += 1
        if self.index2 < self.index1 - 1:
            return
        self.index2 = 0
        
        self.sorted.add(self.index1)
        
        self.index1 -= 1
        if self.index1 > 1:
            return
        
        self.is_sorting = False
        self.index2 = -1
        self.sorted.add(0)
        self.sorted.add(1)
        self.on_update(self.array, sorted = self.sorted)
        

class SelectionSort(Sort):
    SORT_TYPE: str = "SelectionSort"
    def reset(self) -> None:
        super().reset()

        self.index1: int = -1
        self.index2: int = -1
        self.sorted: set[int] = set()
        
        self.on_update(self.array)

    def start(self) -> None:
        self.index1 = 0
        self.index2 = 0
    
    def step_next(self):
        if self.array[self.index1] > self.array[self.index2]:
            self.array[self.index1], self.array[self.index2] = self.array[self.index2], self.array[self.index1]
            
        self.on_update(self.array, selected = {self.index1, self.index2}, sorted = self.sorted)
        
        self.index2 += 1
        if self.index2 < self.array_length:
            return
        
        self.sorted.add(self.index1)
        self.index1 += 1
        self.index2 = self.index1 + 1

        if self.index1 < self.array_length - 1:
            return
        
        self.is_sorting = False
        self.index2 = -1

        self.sorted.add(self.index1)
        self.on_update(self.array, sorted = self.sorted)


class SortingApp(Visualizer):
    NAME: str = "Sorting"
    WIDTH: int = 800
    HEIGHT: int = 600
    
    SORTING_ALGORITHMS: list[Sort] = [BubbleSort, SelectionSort]
    
    COLORS: dict[str, tuple[int, int, int]] = {"bg": (0, 0, 0), "bar": (230, 230, 230), "selected": (255, 0 , 0), "sorted": (0, 255, 0)}

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.array_length: int = 200
        self.array_min: int = 10
        self.array_max: int = self.HEIGHT - self.array_min
        self.bars_width: int = self.WIDTH//self.array_length

        self.sort_index: int = 1
        self.change_sort()

        self.fps: int = 0

        SortingApp.__print_instructions()

    @staticmethod
    def __print_instructions() -> None:
        print("Starting the visualisation of Sorting Algorithms")
        print("ESC to Quit")
        print("ENTER to start/pause sorting")
        print("R to reset")
        print("C | SPACE | TAB to change the sorting algorithm")
        print("SCROLL_WHEEL_UP to increase the speed of sorting")
        print("SCROLL_WHEEL_DOWN to decrease the speed of sorting")
    
    def draw(self, array: list[int], selected: set[int] | None = None, sorted: set[int] | None = None) -> None:
        if selected is None:
            selected = set()
        if sorted is None:
            sorted = set()
        
        self.surface.fill(self.COLORS["bg"])
        for idx, height in enumerate(array):
            color: str = "bar"
            if idx in sorted:
                color = "sorted"
            elif idx in selected:
                color = "selected"
            pygame.draw.rect(self.surface, self.COLORS[color],
                             (idx*self.bars_width, self.HEIGHT - height, self.bars_width, height))
        
        self.update_screen()
    
    def change_sort(self) -> None:
        self.sort_index = (self.sort_index + 1)%len(self.SORTING_ALGORITHMS)
        self.sort: Sort = self.SORTING_ALGORITHMS[self.sort_index](self.array_length, self.array_min, self.array_max, self.draw)
        pygame.display.set_caption(f"Sorting - {self.sort.SORT_TYPE}")

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT: return False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                           
                            case pygame.K_RETURN:
                                self.sort.is_sorting = not self.sort.is_sorting
                                if self.sort.is_sorting:
                                    self.sort.start()
                           
                            case pygame.K_r:
                                self.sort.reset()
                            
                            case (pygame.K_c | pygame.K_SPACE | pygame.K_TAB):
                                if not self.sort.is_sorting:
                                    self.change_sort()

                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case pygame.BUTTON_WHEELUP: self.fps += 10
                            case pygame.BUTTON_WHEELDOWN: self.fps = max(self.fps - 10, 0)
                                
            if self.sort.is_sorting:
                self.sort.step_next()

if __name__ == "__main__":
    screen: pygame.Surface = pygame.display.set_mode((SortingApp.WIDTH, SortingApp.HEIGHT))
    app: Visualizer = SortingApp(screen)
    app.mainloop()
    pygame.quit()