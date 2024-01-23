from Objects import Map, Drone
from polyparser import parse_challenge
from polywriter import Writer
from polysolvers import (naive_approach_loic,
                         naive_approach_theo,
                         naive_approach_amedeo)
from utils.functs import (
    current_payload_drone,
    find_closest_warehouse,
)


def printr(txt):
    print("\033[91m {}\033[00m".format(txt))


def printg(txt):
    print("\033[92m {}\033[00m".format(txt))


def test_drone():
    d0 = Drone(0, (0, 0), [1, 1, 1])
    assert Map.calc_dist(d0, d0) == 0

    d1 = Drone(1, (2, 2), [1, 1, 1])
    d2 = Drone(0, (0, 0), [1, 1, 1])
    assert Map.calc_dist(d1, d2) == 3

    d1 = Drone(0, (0, 0), [1, 1, 1])
    d2 = Drone(0, (0, 3), [1, 1, 1])
    assert Map.calc_dist(d1, d2) == 3

    printg("Drone class tests COMPLETED")


def test_parse_challenge():
    m = parse_challenge("challenges/a_example.in")
    assert m.rows == 100
    assert m.cols == 100
    assert m.nb_drones == 3
    assert m.nb_turns == 50
    assert m.max_payload == 500
    assert m.max_payload == 500
    assert m.product_weights == [100, 5, 450]
    assert m.warehouses[0].position == (0, 0)
    assert m.warehouses[0].stock == [5, 1, 0]
    assert m.warehouses[1].position == (5, 5)
    assert m.warehouses[1].stock == [0, 10, 2]
    assert m.orders[0].position == (1, 1)
    assert m.orders[0].nb_products == 2
    assert m.orders[0].products_qty == [1, 0, 1]
    assert m.orders[1].position == (3, 3)
    assert m.orders[1].nb_products == 1
    assert m.orders[1].products_qty == [1, 0, 0]
    assert m.orders[1].nb_products == 1
    assert m.orders[2].position == (5, 6)
    assert m.orders[2].nb_products == 1
    assert m.orders[2].products_qty == [0, 0, 1]
    assert len(m.drones) == m.nb_drones
    for i in range(m.nb_drones):
        assert m.drones[i].position == m.warehouses[0].position

    printg("Parser tests COMPLETED")


def test_find_closest_warehouse():
    m = parse_challenge("challenges/test_utils.in")
    # Using test_utils challenge, closest warehouse for product type 0 and
    # quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 0, 1)[0].id == 0
    # closest warehouse for product type 2 and quantity 1 should be warehouse 1
    assert find_closest_warehouse(m, 0, 2, 1)[0].id == 1
    # closest warehouse for product type 1 and quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 1, 1)[0].id == 0
    # closest warehouse for product type 0 and quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 0, 5)[0].id == 0
    printg("find_closest_warehouse tests COMPLETED")


def test_current_payload_drone():
    m = parse_challenge("challenges/test_utils.in")
    drone = m.drones[0]
    drone.stock = [1, 0, 0]
    assert current_payload_drone(m, drone) == m.product_weights[0] * 1
    drone.stock = [0, 2, 0]
    assert current_payload_drone(m, drone) == m.product_weights[1] * 2
    drone.stock = [0, 0, 0]
    assert current_payload_drone(m, drone) == 0

    printg("current_payload_drone tests COMPLETED")


def test_naive_loic():
    solution = naive_approach_loic("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "0 L 0 0 1",
            "1 L 1 2 1",
            "0 D 0 0 1",
            "1 D 0 2 1",
            "2 L 0 0 1",
            "2 D 1 0 1",
            "0 L 1 2 1",
            "0 D 2 2 1",
        ]
    )

    printg("Solution naive loic tests COMPLETED")


def test_naive_theo():
    solution = naive_approach_theo("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "1 L 0 0 1",
            "1 D 0 0 1",
            "1 L 1 2 1",
            "1 D 0 2 1",
            "2 L 0 0 1",
            "2 D 1 0 1",
            "0 L 1 2 1",
            "0 D 2 2 1"
        ]
    )

    printg("Solution naive theo tests COMPLETED")


def test_naive_amedeo():
    solution = naive_approach_amedeo("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "0 L 0 0 1",
            "1 L 1 2 1",
            "0 D 0 0 1",
            "1 D 0 2 1",
            "2 L 0 0 1",
            "2 D 1 0 1",
            "0 L 1 2 1",
            "0 D 2 2 1",
        ]
    )

    printg("Solution naive amedeo tests COMPLETED")


def test_writer():
    # Testing if writer hasnt changed, if it have, you may want to update the
    # solutions stored in solutions_test to pass this test
    Writer("challenges/a_example.in", "naive_loic")
    assert set(open("solutions/a_example.out")) == set(
        open("solutions_test/a_example_loic.test")
    )

    Writer("challenges/b_busy_day.in", "naive_loic")
    assert set(open("solutions/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_loic.test")
    )
    printg("Writer tests PASSED for naive_loic")

    Writer("challenges/a_example.in", "naive_theo")
    assert set(open("solutions/a_example.out")) == set(
        open("solutions_test/a_example_theo.test")
    )

    Writer("challenges/b_busy_day.in", "naive_theo")
    assert set(open("solutions/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_theo.test")
    )

    printg("Writer tests PASSED for naive_theo")

    Writer("challenges/a_example.in", "naive_amedeo")
    assert set(open("solutions/a_example.out")) == set(
        open("solutions_test/a_example_amedeo.test")
    )

    Writer("challenges/b_busy_day.in", "naive_amedeo")
    assert set(open("solutions/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_amedeo.test")
    )

    printg("Writer tests PASSED for naive_amedeo")

    printg("Writer tests COMPLETED")


if __name__ == "__main__":
    test_drone()
    test_parse_challenge()
    test_find_closest_warehouse()
    test_current_payload_drone()
    test_naive_loic()
    test_naive_theo()
    # test_naive_amedeo() car je vais repartir sur des base propre
    test_writer()
