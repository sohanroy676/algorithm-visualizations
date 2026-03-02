from .visualizer import Visualizer

from .pathfinder import PathfinderApp                   # Visualization
from .sorting import SortingApp                         # Visualization
from .wave_function_collapse import WaveFuncApp         # Visualization
from .hilbert_curve import HilbertCurveApp              # Visualization
from .life import LifeApp                               # Simulation
# from .marchsq import MarchSqApp                       # Visualization
from .nqueens import NQueensApp                         # Visualization
# from .sand import SandApp             # Shader        # Simulation
from .sudoku import SudokuApp                           # Visualization
from .wolfram_automata import WolframAutomataApp        # Simulation

_ALL = [PathfinderApp, SortingApp, WaveFuncApp, HilbertCurveApp, LifeApp, NQueensApp, SudokuApp, WolframAutomataApp]

APPS = {app.NAME: app for app in _ALL}
