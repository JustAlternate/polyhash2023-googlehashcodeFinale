from Objects import *
from polyparser import *


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


def test_parse_challenge():
    m = parse_challenge("challenges/a_example.in")
    assert (m.rows == 100)
    assert (m.cols == 100)
    assert (m.nb_drones == 3)
    assert (m.nb_turns == 50)
    assert (m.max_payload == 500)
    assert (m.max_payload == 500)
    assert (m.product_weights == [100, 5, 450])
    assert (m.warehouses[0].position == (0, 0))
    assert (m.warehouses[0].stock == [5, 1, 0])
    assert (m.warehouses[1].position == (5, 5))
    assert (m.warehouses[1].stock == [0, 10, 2])
    assert (m.orders[0].destination == (1, 1))
    assert (m.orders[0].nb_products == 2)
    assert (m.orders[0].products_qty == [1, 0, 1])
    assert (m.orders[1].destination == (3, 3))
    assert (m.orders[1].nb_products == 1)
    assert (m.orders[1].products_qty == [1, 0, 0])
    assert (m.orders[1].nb_products == 1)
    assert (m.orders[2].destination == (5, 6))
    assert (m.orders[2].nb_products == 1)
    assert (m.orders[2].products_qty == [0, 0, 1])

    printG("Parser tests COMPLETED")


if __name__ == "__main__":
    test_Drone()
    test_parse_challenge()
