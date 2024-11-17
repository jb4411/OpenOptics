from lens import ThinLens, full_lens_makers_equation, all_lens_equations
from mirror import Mirror, spherical_mirror_equation


class CompoundSystem:
    ho: int | float

    def __init__(self):
        self.distances = []
        self.optics = []

    def add_object(self, ho):
        self.ho = ho

    def add_optic(self, optic, distance_from_last_element: int | float):
        x = 0
        y = 0
        if len(self.optics) > 0:
            x = self.optics[-1].x
            y = self.optics[-1].y

        x += distance_from_last_element

        optic.x = x
        optic.y = y
        self.optics.append(optic)

        self.distances.append(distance_from_last_element)

    def evaluate_system(self, n_atm=1):
        idx = 0
        j = 1
        dij = 0
        ray_x = 0
        inc = 1
        suffix = ''
        #hoj = self.ho
        hij = self.ho

        # start of loop
        doj = self.distances[idx] - dij
        optic = self.optics[idx]

        if isinstance(optic, ThinLens):
            # TODO - deal with len made of two different materials
            R1, R2 = optic.get_Rs(ray_x)
            #f, n1, n2, R1, R2 = full_lens_makers_equation(n1=n_atm, n2=optic.lens1.n, R1=R1, R2=R2)
            f, n1, n2, R1, R2, do, di, m, ho, hi = all_lens_equations(n1=n_atm, n2=optic.lens1.n, R1=R1, R2=R2,
                                                                      do=doj, ho=hij)
            dij = di
            hij = hi
            fj = f
            show_relative_output(idx, j, doj, dij, fj, suffix, "lens")

        elif isinstance(optic, Mirror):
            suffix += "'"
            inc *= -1
            R = optic.get_R()
            R, f, do, di, m, ho, hi = spherical_mirror_equation(R=R, do=doj, ho=hij)
            dij = di
            hij = hi
            fj = f
            show_relative_output(idx, j, doj, dij, fj, suffix, "mirror")

        # end of loop
        ray_x += self.distances[idx]
        idx += inc
        j += inc

def show_relative_output(idx, j, doj, dij, fj, suffix, name):
    if doj < 0:
        obj_type = "VIRTUAL object"
    else:
        obj_type = "REAL object"

    if dij < 0:
        img_type = "VIRTUAL image"
    else:
        img_type = "REAL image"

    print(f"{'\n' if idx > 0 else ''}Relative to {name} {j}:")
    print(f"\tdo({j}{suffix}) = {doj}, {obj_type}, f({j}) = {fj}")
    print(f"\tdi({j}{suffix}) = {dij}, {img_type}")