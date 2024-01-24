"""
Module de résolution du projet Poly#.
"""
from polyparser import parse_challenge
from utils.functs import sort_objects_by_distance_from_obj, makeCommands, qty_drone_can_load, find_closest_warehouse


def naive_approach_loic(fichier_challenge):
    """
    Naive approch that use every drones one by one and cycle through each
    orders one by one and each product_type one by one.
    """
    queue_load, queue_deliver = [], []

    solution = []
    challenge = parse_challenge(fichier_challenge)

    current_drone_index = 0
    current_drone = challenge.drones[current_drone_index]

    # sort the orders list to have the closest orders first.
    sort_objects_by_distance_from_obj(
        challenge, challenge.drones[current_drone_index], challenge.orders)

    for current_order in challenge.orders:
        if queue_load != []:
            makeCommands(solution, queue_load, queue_deliver)
            queue_deliver = []
            queue_load = []
        for product_type in range(len(current_order.products_qty)):
            while current_order.products_qty[product_type] != 0:

                if current_drone_index == len(challenge.drones) - 1:
                    # If we used every drones, we dequeue the queues to write
                    # the load action first then the deliver actions.
                    makeCommands(solution, queue_load, queue_deliver)
                    queue_deliver = []
                    queue_load = []

                quantity_able_to_load = qty_drone_can_load(
                    challenge, product_type, current_order.id
                )

                # Try to find a warehouse with the needed quantity, if there is
                # not, try to find one with less quantity
                found_warehouse, qty_found = find_closest_warehouse(
                    challenge,
                    current_drone_index,
                    product_type,
                    quantity_able_to_load,
                )

                queue_load.append(
                    [current_drone_index, found_warehouse.id,
                     product_type, qty_found]
                )
                queue_deliver.append(
                    [current_drone_index, current_order.id,
                     product_type, qty_found]
                )

                current_drone.position = current_order.position
                # Remove x objetcs from the order
                current_order.products_qty[product_type] -= qty_found
                # Remove x objetcs from the warehouse
                found_warehouse.stock[product_type] -= qty_found

                # Change drone
                current_drone_index = (
                                              current_drone_index + 1) % (len(challenge.drones))

    # In case there is remaining command to make in the queues.
    makeCommands(solution, queue_load, queue_deliver)
    queue_deliver = []
    queue_load = []
    return solution
