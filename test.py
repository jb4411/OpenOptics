from compound_optical_system import CompoundSystem
from constants import n_flint_glass, n_crown_glass, n_polystyrene
from lens import ThinLens, Lens, get_double_convex, get_double_concave
from general import SurfaceShape as SS
from mirror import Mirror


def test_activity_8_p1():
    system = CompoundSystem()

    ho = 3  # cm
    do = 25  # cm
    D12 = 5  # cm

    n_lens = 1.55
    R_abs = 22  # cm
    lens1 = get_double_convex(n_lens, n_lens, R_abs, R_abs)

    R_mirror_abs = 40  # cm
    mirror = Mirror(SS.CONCAVE, R_mirror_abs)

    system.add_object(ho)
    system.add_optic(lens1, do)
    system.add_optic(mirror, D12)

    system.evaluate()


def test_activity_8_p2():
    system = CompoundSystem()

    ho = 3  # cm
    system.add_object(ho)

    do = 15 # cm
    D12 = 10 # cm
    D23 = 15 # cm
    D34 = 5 # cm

    n_lens1 = n_flint_glass
    l1_R_abs = 35 # cm
    lens1 = get_double_concave(n_lens1, n_lens1, l1_R_abs, l1_R_abs)
    system.add_optic(lens1, do)

    n_lens2 = n_crown_glass
    l2_R_abs = 15 # cm
    lens2 = get_double_convex(n_lens2, n_lens2, l2_R_abs, l2_R_abs)
    system.add_optic(lens2, D12)


    R_mirror_abs = 18 # cm
    mirror = Mirror(SS.CONVEX, R_mirror_abs)
    system.add_optic(mirror, D23)

    system.evaluate()


    # if mirror not there
    print("\n\nIf the mirror was not present:")
    system2 = CompoundSystem()

    ho = 3  # cm
    system2.add_object(ho)

    system2.add_optic(lens1, do)
    system2.add_optic(lens2, D12)

    n_lens3 = n_polystyrene
    l3_R_abs = 20  # cm
    lens3 = ThinLens(Lens(SS.CONVEX, n_lens3, l3_R_abs), Lens(SS.FLAT, n_lens3))
    system2.add_optic(lens3, D23 + D34)

    system2.evaluate()



def main():
    test_activity_8_p2()


if __name__ == '__main__':
    main()
