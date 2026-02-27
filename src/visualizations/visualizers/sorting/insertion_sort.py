from .sort import Sort

class InsertionSort(Sort):
    TYPE: str = "InsertionSort"
    def reset(self) -> None:
        super().reset()

        self.index1: int = -1
        self.index2: int = -1
        self.sorted: set[int] = set()
        
        self.on_update(self.array)

    def start(self) -> None:
        self.index1 = 0
        self.index2 = 0
        self.sorted.add(0)
    
    def step_next(self):
        if self.index2 > 0 and self.array[self.index2 - 1] > self.array[self.index2]:
            self.array[self.index2 - 1], self.array[self.index2] = self.array[self.index2], self.array[self.index2 - 1]
        
            self.sorted.remove(self.index2 - 1)
            self.sorted.add(self.index2)
            self.on_update(self.array, {self.index2 - 1}, self.sorted)

            self.index2 -= 1
        else:
            self.sorted.add(self.index2)
            self.index1 += 1
            self.index2 = self.index1
            self.on_update(self.array, {self.index1}, self.sorted)
            
            if self.index1 < self.array_length:
                return
            
            self.is_sorting = False
            self.index2 = -1

            self.on_update(self.array, sorted = self.sorted)