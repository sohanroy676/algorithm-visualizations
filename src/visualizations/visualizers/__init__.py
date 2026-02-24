from .visualizer import Visualizer
from .hilbert_curve import HilbertCurveApp
from .sudoku import SudokuApp
from .nqueens import NQueensApp

__ALL = [HilbertCurveApp, SudokuApp, NQueensApp]

APPS = {app.NAME: app for app in __ALL}
