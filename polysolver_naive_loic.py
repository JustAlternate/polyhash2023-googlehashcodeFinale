#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polyparser import parse_challenge
from utils.functs import qty_drone_can_load, find_closest_warehouse, makeCommand

"""
Module de résolution du projet Poly#.
"""


def naive_approach_loic(challenge):
    """
    Naive approch that use every drones one by one and cycle through each orders
    one by one and each product_type one by one.
    """

    Solution = []
    Map = parse_challenge(challenge)

    current_drone_index = 0
    for current_order in Map.orders:
        # We change drone for a new order
        current_drone_index = (current_drone_index + 1) % (len(Map.drones))
        current_drone = Map.drones[current_drone_index]

        for product_type in range(len(current_order.products_qty)):
            while current_order.products_qty[product_type] != 0:
                quantity_able_to_load = qty_drone_can_load(
                    Map, product_type, current_order.id
                )

                # Try to find a warehouse with the needed quantity, if there is not, try to find one with less quantity
                current_warehouse, qty_able_to_load = find_closest_warehouse(
                    Map, current_drone.id, product_type, quantity_able_to_load
                )

                makeCommand("L", Solution, current_drone.id,
                            current_warehouse.id, product_type, quantity_able_to_load)
                # On remove 1 objet de la warehouse
                current_warehouse.stock[product_type] -= quantity_able_to_load
                makeCommand("D", Solution, current_drone.id,
                            current_order.id, product_type, quantity_able_to_load)
                current_drone.position = current_order.position
                # On remove 1 objet de l'order
                current_order.products_qty[product_type] -= quantity_able_to_load

    return Solution
