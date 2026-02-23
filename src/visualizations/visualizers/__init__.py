from .visualizer import Visualizer
from .hilbert_curve import HilbertCurveApp
from .sudoku import SudokuApp

__ALL = [HilbertCurveApp, SudokuApp]

APPS = {app.NAME: app for app in __ALL}
