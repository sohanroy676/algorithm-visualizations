# from .astar import Astar
from .hilbert_curve import HilbertCurveApp
from .visualizer import Visualizer

_ALL = [HilbertCurveApp]

APPS = {app.NAME: app for app in _ALL}
