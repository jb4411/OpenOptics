from sympy import symbols, Eq, solve

from general import OpticsObj, SurfaceShape
from general import SurfaceShape as SS

class Mirror(OpticsObj):
    shape: SurfaceShape
    R_abs: int | float | None

    def __init__(self, shape: SurfaceShape, R_abs: int | float | None = None,
                 x: int | float | None = None, y: int | float | None = None):
        super().__init__(x, y)

        self.shape = shape
        self.R_abs = R_abs

    def get_R(self):
        R = self.R_abs
        if self.shape == SS.CONVEX:
            R *= -1

        return R

    def get_focal_length(self, do=None, di=None, m=None, ho=None, hi=None):
        R = self.get_R()
        f = None
        if R is not None:
            f = R / 2
            return f

        R, f, do, di, m, ho, hi = spherical_mirror_equation(R, f, do, di, m, ho, hi)
        return f


def spherical_mirror_equation(R=None, f=None, do=None, di=None, m=None, ho=None, hi=None):
    solve_for = []
    if R is None:
        R = symbols('f')
        solve_for.append(R)
    if f is None:
        f = symbols('f')
        solve_for.append(f)
    if do is None:
        do = symbols('do')
        solve_for.append(do)
    if di is None:
        di = symbols('di')
        solve_for.append(di)
    if m is None:
        m = symbols('m')
        solve_for.append(m)
    if ho is None:
        ho = symbols('ho')
        solve_for.append(ho)
    if hi is None:
        hi = symbols('hi')
        solve_for.append(hi)

    eq2 = Eq((1 / do) + (1 / di), 1 / f)

    eq3a = Eq(m, hi / ho)
    eq3b = Eq(m, -di / do)
    eq3c = Eq(hi / ho, -di / do)

    eq4 = Eq(f, R / 2)

    equations = [eq2, eq3a, eq3b, eq3c, eq4]

    sol_dict = solve(equations, solve_for, dict=True)

    results = []
    for elem in [R, f, do, di, m, ho, hi]:
        if elem in sol_dict:
            results.append(sol_dict[elem])
        else:
            results.append(elem)

    return results