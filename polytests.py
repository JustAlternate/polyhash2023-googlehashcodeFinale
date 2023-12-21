from Objects import *


def printR(txt): print("\033[91m {}\033[00m" .format(txt))
def printG(txt): print("\033[92m {}\033[00m" .format(txt))


def test_Drone():
    D = Drone((0, 0), [1, 1, 1])
    assert (D.calc_dist((0, 0)) == 0)

    D = Drone((0, 0), [1, 1, 1])
    assert (D.calc_dist((2, 2)) == 3)

    D = Drone((0, 0), [1, 1, 1])
    assert (D.calc_dist((0, 3)) == 3)

    printG("Drone tests COMPLETED")


if __name__ == "__main__":
    test_Drone()
