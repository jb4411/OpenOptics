from sympy import symbols, Eq, solve

from general import SurfaceShape, OpticsObj
from general import SurfaceShape as SS


class Lens(OpticsObj):
    shape: SurfaceShape
    n: int | float
    R_abs: int | float | None

    def __init__(self, x: int | float | None, y: int | float | None,
                 shape: SurfaceShape, n: int | float, R_abs: int | float | None = None):
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