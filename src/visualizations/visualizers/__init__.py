from .visualizer import Visualizer # Importing here to allow main to access it directly

from .pathfinder import PathfinderApp
from .sorting import SortingApp
from .wave_function_collapse import WaveFuncApp
from .hilbert_curve import HilbertCurveApp
from .life import LifeApp
from .marchsq import MarchSQApp
from .nqueens import NQueensApp
from .sand import SandApp
from .sudoku import SudokuApp
from .wolfram_automata import WolframAutomataApp

_ALL = [PathfinderApp, SortingApp, WaveFuncApp, HilbertCurveApp, LifeApp, MarchSQApp, NQueensApp, SandApp, SudokuApp, WolframAutomataApp]

APPS = {app.NAME: app for app in _ALL}
