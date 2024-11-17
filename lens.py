from enum import Enum

from sympy import symbols, Eq, solve

from general import SurfaceShape, OpticsObj
from general import SurfaceShape as SS


class LensType(Enum):
    BI_CONVEX = 2
    PLANO_CONVEX = 4
    MENISCUS_CONVEX = 6

    BI_CONCAVE = 1
    PLANO_CONCAVE = 3
    MENISCUS_CONCAVE = 5

CONVERGING_LENS = {LensType.BI_CONVEX, LensType.PLANO_CONVEX, LensType.MENISCUS_CONVEX}
DIVERGING_LENS = {LensType.BI_CONCAVE, LensType.PLANO_CONCAVE, LensType.MENISCUS_CONCAVE}


class Lens(OpticsObj):
    shape: SurfaceShape
    n: int | float
    R_abs: int | float | None

    def __init__(self, shape: SurfaceShape, n: int | float, R_abs: int | float | None = None,
                 x: int | float | None = None, y: int | float | None = None):
        super().__init__(x, y)

        self.shape = shape
        self.n = n
        self.R_abs = R_abs

    def get_R(self, ray_x):
        R = self.R_abs
        if R is None:
            return R

        if ray_x < self.x:
            if self.shape == SS.CONCAVE:
                R *= -1
        elif ray_x > self.x:
            if self.shape == SS.CONVEX:
                R *= -1

        return R

    def get_C(self):
        if self.shape == SS.CONCAVE:
            return self.x - self.R_abs
        elif self.shape == SS.CONVEX:
            return self.x + self.R_abs
        else:
            return None


class ThinLens(OpticsObj):
    lens1: Lens
    lens2: Lens

    def __init__(self, x: int | float | None, y: int | float | None,
                 lens1: Lens, lens2: Lens):
        super().__init__(x, y)

        self.lens1 = lens1
        self.lens2 = lens2

    def get_Rs(self, ray_x):
        if ray_x <= self.x:
            R1 = self.lens1.get_R(ray_x)
            R2 = self.lens2.get_R(ray_x)
        else:
            R1 = self.lens2.get_R(ray_x)
            R2 = self.lens1.get_R(ray_x)

        return R1, R2

    def get_Cs(self):
        return self.lens1.get_C(), self.lens2.get_C()


def full_lens_makers_equation(f=None, n1=None, n2=None, R1=None, R2=None):
    solve_for = []
    if f is None:
        f = symbols('f')
        solve_for.append(f)
    if n1 is None:
        n1 = symbols('n1')
        solve_for.append(n1)
    if n2 is None:
        n2 = symbols('n2')
        solve_for.append(n2)
    if R1 is None:
        R1 = symbols('R1')
        solve_for.append(R1)
    if R2 is None:
        R2 = symbols('R2')
        solve_for.append(R2)

    eq = Eq(1 / f, ((n2 / n1) - 1) * ((1 / R1) - (1 / R2)))
    sol_dict = solve(eq, solve_for, dict=True)

    results = []
    for elem in [f, n1, n2, R1, R2]:
        if elem in sol_dict:
            results.append(sol_dict[elem])
        else:
            results.append(elem)

    return results


def lens_makers_equation(f=None, n=None, R1=None, R2=None):
    return full_lens_makers_equation(f=f, n1=1, n2=n, R1=R1, R2=R2)


def all_lens_equations(f=None, n1=None, n2=None, R1=None, R2=None, do=None, di=None, m=None, ho=None, hi=None):
    solve_for = []
    if f is None:
        f = symbols('f')
        solve_for.append(f)
    if n1 is None:
        n1 = symbols('n1')
        solve_for.append(n1)
    if n2 is None:
        n2 = symbols('n2')
        solve_for.append(n2)
    if R1 is None:
        R1 = symbols('R1')
        solve_for.append(R1)
    if R2 is None:
        R2 = symbols('R2')
        solve_for.append(R2)
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

    eq = Eq(1 / f, ((n2 / n1) - 1) * ((1 / R1) - (1 / R2)))
    eq4 = Eq((1 / do) + (1 / di), 1 / f)

    eq5a = Eq(m, hi / ho)
    eq5b = Eq(m, -di / do)
    eq5c = Eq(hi / ho, -di / do)

    equations = [eq, eq4, eq5a, eq5b, eq5c]

    sol_dict = solve(equations, solve_for, dict=True)

    results = []
    for elem in [f, n1, n2, R1, R2, do, di, m, ho, hi]:
        if elem in sol_dict:
            results.append(sol_dict[elem])
        else:
            results.append(elem)

    return results
