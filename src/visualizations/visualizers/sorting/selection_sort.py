from .sort import Sort

class SelectionSort(Sort):
    TYPE: str = "SelectionSort"
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