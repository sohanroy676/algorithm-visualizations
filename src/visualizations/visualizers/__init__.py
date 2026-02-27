from .visualizer import Visualizer

from .pathfinder import PathfinderApp
from .sorting import SortingApp
from .hilbert_curve import HilbertCurveApp
# from .life import LifeApp             # Shader
# from .marchsq import MarchSqApp       # Shader
from .nqueens import NQueensApp
# from .sand import SandApp             # Shader
from .sudoku import SudokuApp
# from .wavefunc import WaveFuncApp
from .wolfram_automata import WolframAutomataApp

_ALL = [PathfinderApp, SortingApp, HilbertCurveApp, NQueensApp, SudokuApp, WolframAutomataApp]

APPS = {app.NAME: app for app in _ALL}
