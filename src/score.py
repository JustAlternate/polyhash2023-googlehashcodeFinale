from math import ceil, sqrt

from src.polyparser import parse_challenge


def parse_solution_challenge(filename: str):
    """Read a solution file and parse the informations in the Map class.
    """

    from src.Objects.Map import Map
    challenge : Map = parse_challenge(filename)
    turn = 0
    with open(filename, "r") as f:
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



        for drone_id,drone_action in commands:
            for action in drone_action:
                drone = challenge.drones[drone_action]
                if action[0] == "L":
                    challenge.calc_dist([action[1]],)
                    challenge.warehouses[action[1]].stock[action[2]] -= action[3]
                    challenge.drones[action[1]].stock[action[2]] += action[3]
                    challenge.drones[drone_id].totalLoad += challenge.product_weights[action[2]] * action[3]
                    challenge.orders[prodT] -= qtyL
                    drone.stock[action[2]] += action[3]
                    warehouse.stock[action[2]] -= action[3]
                elif action[0] == "D":
                    order = challenge.orders[action[1]]
                    drone = challenge.drones[drone_action]
                    drone.position = order.position
                    drone.stock[action[2]] -= action[3]
                    order.products_qty[action[2]] -= action[3]
                turn += 1

                turn = ceil(
                sqrt(
                    (action - object1.position[0]) ** 2
                    + (object2.position[1] - object1.position[1]) ** 2
                )


        return commands
