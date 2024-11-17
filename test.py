from compound_optical_system import CompoundSystem
from lens import ThinLens, Lens
from general import SurfaceShape as SS
from mirror import Mirror


def test_CompoundSystem():
    system = CompoundSystem()

    ho = 3  # cm
    do = 25  # cm
    D12 = 5  # cm

    n_lens = 1.55
    R1_abs = 22  # cm
    R2_abs = 22  # cm
    lens1 = ThinLens(Lens(SS.CONVEX, n_lens, R1_abs), Lens(SS.CONCAVE, n_lens, R2_abs))

    R_mirror_abs = 40  # cm
    mirror = Mirror(SS.CONCAVE, R_mirror_abs)

    system.add_object(ho)
    system.add_optic(lens1, do)
    system.add_optic(mirror, D12)

    system.evaluate()



def main():
    test_CompoundSystem()


if __name__ == '__main__':
    main()
