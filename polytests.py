from Objects import *
from polyparser import *
from polysolver_naive_loic import naive_approach_loic
from polywriter import Writer
from utils.functs import *


def printR(txt): print("\033[91m {}\033[00m" .format(txt))
def printG(txt): print("\033[92m {}\033[00m" .format(txt))


def test_Drone():
    D = Drone(0, (0, 0), [1, 1, 1])
    assert (D.calc_dist((0, 0)) == 0)

    D = Drone(0, (0, 0), [1, 1, 1])
    assert (D.calc_dist((2, 2)) == 3)

    D = Drone(0, (0, 0), [1, 1, 1])
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
    assert (len(m.drones) == m.nb_drones)
    for i in range(m.nb_drones):
        assert (m.drones[i].position == m.warehouses[0].position)

    printG("Parser tests COMPLETED")


def test_find_closest_warehouse_with_item_qty():
    m = parse_challenge("challenges/test_utils.in")
    # Using test_utils challenge, closest warehouse for product type 0 and quantity 1 should be warehouse 0
    assert (find_closest_warehouse_with_item_qty(m, 0, 0, 1) == 0)
    # closest warehouse for product type 2 and quantity 1 should be warehouse 1
    assert (find_closest_warehouse_with_item_qty(m, 0, 2, 1) == 1)
    # closest warehouse for product type 1 and quantity 1 should be warehouse 0
    assert (find_closest_warehouse_with_item_qty(m, 0, 1, 1) == 0)
    # closest warehouse for product type 1 and quantity 999 should return -1
    assert (find_closest_warehouse_with_item_qty(m, 0, 1, 999) == -1)
    # closest warehouse for product type 3 and quantity 1 should return -1 cause product type 3 is in no warehouse
    assert (find_closest_warehouse_with_item_qty(m, 0, 3, 1) == -1)
    # closest warehouse for product type 1 and quantity 0 should return -1 cause this is an error
    assert (find_closest_warehouse_with_item_qty(m, 0, 1, 0) == 0)

    printG("Function find_closest_warehouse_with_item_qty tests COMPLETED")


def test_current_payload_drone():
    m = parse_challenge("challenges/test_utils.in")
    Drone = m.drones[0]
    Drone.stock = [1, 0, 0]
    assert (current_payload_drone(m, Drone) == m.product_weights[0]*1)
    Drone.stock = [0, 2, 0]
    assert (current_payload_drone(m, Drone) == m.product_weights[1]*2)
    Drone.stock = [0, 0, 0]
    assert (current_payload_drone(m, Drone) == 0)

    printG("Function current_payload_drone tests COMPLETED")


def test_naive_loic():
    solution = naive_approach_loic("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert (set(solution) == set([
            '1 L 0 0 1',
            '1 D 0 0 1',
            '1 L 1 2 1',
            '1 D 0 2 1',
            '2 L 0 0 1',
            '2 D 1 0 1',
            '0 L 1 2 1',
            '0 D 2 2 1'
            ]))

    printG("Solution naive loic tests COMPLETED")


def test_writer():
    # Testing if writer hasnt changed, if it have, you may want to update the solutions stored in solutions_test to pass this test
    Writer("challenges/a_example.in", "naive_loic")
    assert (set(open("solutions/a_example.out")) ==
            set(open("solutions_test/a_example.test")))

    Writer("challenges/b_busy_day.in", "naive_loic")
    assert (set(open("solutions/b_busy_day.out")) ==
            set(open("solutions_test/b_busy_day.test")))

    printG("Writer tests COMPLETED")


if __name__ == "__main__":
    test_Drone()
    test_parse_challenge()
    test_naive_loic()
    test_writer()
    test_find_closest_warehouse_with_item_qty()
    test_current_payload_drone()
