from .sort import Sort

class BubbleSort(Sort):
    TYPE: str = "BubbleSort"
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