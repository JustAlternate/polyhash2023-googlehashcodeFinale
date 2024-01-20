#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polyparser import parse_challenge
from utils.functs import qty_drone_can_load, find_closest_warehouse, makeCommands, sort_objects_by_distance_from_obj

"""
Module de résolution du projet Poly#.
"""


def naive_approach_loic(challenge):
    """
    Naive approch that use every drones one by one and cycle through each orders
    one by one and each product_type one by one.
    """
    queue_load, queue_deliver = [], []

    Solution = []
    Map = parse_challenge(challenge)

    current_drone_index = 0
    current_drone = Map.drones[current_drone_index]

    # sort the orders list to have the closest orders first.
    sort_objects_by_distance_from_obj(
        Map, Map.drones[current_drone_index], Map.orders)

    for current_order in Map.orders:
        if queue_load != []:
            makeCommands(Solution, queue_load, queue_deliver)
            queue_deliver = []
            queue_load = []
        for product_type in range(len(current_order.products_qty)):
            while current_order.products_qty[product_type] != 0:

                if current_drone_index == len(Map.drones)-1:
                    # If we used every drones, we dequeue the queues to write the load action first then the deliver actions.
                    makeCommands(Solution, queue_load, queue_deliver)
                    queue_deliver = []
                    queue_load = []

                quantity_able_to_load = qty_drone_can_load(
                    Map, product_type, current_order.id
                )

                # Try to find a warehouse with the needed quantity, if there is not, try to find one with less quantity
                found_warehouse, qty_found = find_closest_warehouse(
                    Map, current_drone_index, product_type, quantity_able_to_load
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
                    current_drone_index + 1) % (len(Map.drones))

    # In case there is remaining command to make in the queues.
    makeCommands(Solution, queue_load, queue_deliver)
    queue_deliver = []
    queue_load = []
    return Solution
