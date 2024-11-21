import math
from enum import Enum

import numpy as np
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
#import kaleido

from sympy import symbols, Eq, solve


class SurfaceShape(Enum):
    FLAT = 0
    CONVEX = 1
    CONCAVE = 2


class OpticsObj:
    x: int | float | None
    y: int | float | None

    def __init__(self, x: int | float | None, y: int | float | None):
        self.x = x
        self.y = y



