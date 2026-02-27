from .visualizer import Visualizer

# from .astar import AstarApp
from .pathfinder import PathfinderApp
from .hilbert_curve import HilbertCurveApp
# from .life import LifeApp             # Shader
# from .marchsq import MarchSqApp       # Shader
from .nqueens import NQueensApp
# from .sand import SandApp             # Shader
from .sort import SortingApp
from .sudoku import SudokuApp
# from .wavefunc import WaveFuncApp     # Shader
# from .wolframca import WolframcaApp   # Shader

__ALL = [PathfinderApp, HilbertCurveApp, NQueensApp, SortingApp, SudokuApp]

APPS = {app.NAME: app for app in __ALL}
