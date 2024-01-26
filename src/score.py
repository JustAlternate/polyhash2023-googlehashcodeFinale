from math import ceil, sqrt

from Objects.Map import Map
from polyparser import parse_challenge


def parse_solution_challenge(filenameIn: str, filenameOut: str):
    """Read a solution file and parse the informations in the Map class.
    """

    challenge: Map = parse_challenge(filenameIn)
    turn = 0
    total = 0
    print(total)
    with open(filenameOut, "r") as f:
        # Read infos map
        nb_commands = int(f.readline())
        commands = {}
        drone_id, action, dest_id, product_type, qty = [
            int(v) for v in f.readline().split()
        ]
        commands[drone_id] = [(action, dest_id, product_type, qty)]
        for _ in range(nb_commands):
            drone_id, action, dest_id, product_type, qty = [
                int(v) for v in f.readline().split()
            ]
            commands[drone_id].append((action, dest_id, product_type, qty))

        for drone_id, drone_action in commands:
            for action in drone_action:
                if action[0] == "L":
                    turn += challenge.calc_dist(
                        challenge.drones[drone_id], challenge.warehouses[action[1]])
                    challenge.warehouses[action[1]
                                         ].stock[action[2]] -= action[3]
                    challenge.drones[drone_id].stock[action[2]] += action[3]
                    challenge.drones[drone_id].totalLoad += challenge.product_weights[action[2]] * action[3]
                    challenge.drones[drone_id].position = challenge.warehouses[action[1]].position
                    # challenge.orders[action[1]].products_qty[action[2]] -= action[3]
                elif action[0] == "D":
                    turn += challenge.calc_dist(
                        challenge.drones[drone_id], challenge.warehouses[action[1]])
                    challenge.drones[drone_id].stock[action[2]] -= action[3]
                    challenge.drones[drone_id].totalLoad -= challenge.product_weights[action[2]] * action[3]
                    challenge.drones[drone_id].position = challenge.orders[action[1]].position
                    # challenge.orders[action[1]].products_qty[action[2]] -= action[3]
                turn += 1
                if challenge.orders[action[1]].check_full_filled:
                    total += ((challenge.nb_turns - turn) /
                              challenge.nb_turns)*100
    print(total)


parse_solution_challenge("challenges/d_mother_of_all_warehouses.in",
                         "solutions/solutions_theo/d_mother_of_all_warehouses.out")
