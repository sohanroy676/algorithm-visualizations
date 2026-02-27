from abc import ABC, abstractmethod
from random import randint
from collections.abc import Callable

type DrawCallback = Callable[[list[int], set[int] | None, set[int] | None], None]

class Sort(ABC):
    TYPE: str = "Sorting"
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