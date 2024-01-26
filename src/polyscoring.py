from math import ceil

from Objects.Map import Map
from polyparser import parse_challenge


def parse_solution_challenge(filenameIn: str, filenameOut: str):
    """Read a solution file and parse the informations in the Map class.
    """

    challenge: Map = parse_challenge(filenameIn)
    total = 1
    print(total)
    with open(filenameOut, "r") as f:
        # Read infos map
        nb_commands = int(f.readline())
        commands: dict[int, list[str, int, int, int]] = {}
        for _ in range(nb_commands):
            drone_id, action, dest_id, product_type, qty = [
                v for v in f.readline().split()
            ]
            if int(drone_id) not in commands.keys():
                commands[int(drone_id)] = [(str(action), int(dest_id),
                                            int(product_type), int(qty))]
            commands[int(drone_id)].append((str(action), int(dest_id),
                                            int(product_type), int(qty)))

    # solution = naive_approach_theo(filenameOut)

    # for ligne in commands:
        # int(drone_id), a = [v for ligne.split(" ")
        for drone_id, drone_action in commands.items():
            turn = 0
            for action in drone_action:
                if turn > challenge.nb_turns:
                    return
                if action[0] == "L":
                    turn += challenge.calc_dist(
                        challenge.drones[drone_id],
                        challenge.warehouses[action[1]])
                    challenge.warehouses[action[1]].stock[action[2]]\
                        -= action[3]
                    challenge.drones[drone_id].stock[action[2]] += action[3]
                    challenge.drones[drone_id].totalLoad += \
                        challenge.product_weights[action[2]] * action[3]
                    challenge.drones[drone_id].position = \
                        challenge.warehouses[action[1]].position
                elif action[0] == "D":
                    turn += challenge.calc_dist(
                        challenge.drones[drone_id],
                        challenge.orders[action[1]])
                    challenge.drones[drone_id].stock[action[2]] -= action[3]
                    challenge.drones[drone_id].totalLoad -= \
                        challenge.product_weights[action[2]] * action[3]
                    challenge.drones[drone_id].position = \
                        challenge.orders[action[1]].position
                    challenge.orders[action[1]].products_qty[action[2]] -= \
                        action[3]
                    if challenge.orders[action[1]].check_full_filled():
                        total += ceil(((
                            challenge.nb_turns - turn) / challenge.nb_turns
                        ) * 100)
                turn += 1
    print(total)


parse_solution_challenge("challenges/b_busy_day.in",
                         "solutions/solutions_theo/b_busy_day.out")
