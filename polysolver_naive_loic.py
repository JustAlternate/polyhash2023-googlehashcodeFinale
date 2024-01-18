#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polyparser import parse_challenge
from utils.functs import qty_drone_can_load, find_closest_warehouse_with_item_qty

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
                index_warehouse = find_closest_warehouse_with_item_qty(
                    Map, current_drone.id, product_type, quantity_able_to_load
                )

                # If no warehouse was found, try to find another one that have less quantity of the desired product
                while index_warehouse == -1:
                    quantity_able_to_load -= 1
                index_warehouse = find_closest_warehouse_with_item_qty(
                    Map, current_drone.id, product_type, quantity_able_to_load
                )

                current_warehouse = Map.warehouses[index_warehouse]

                Solution.append(
                    str(current_drone.id)
                    + " L "
                    + str(index_warehouse)
                    + " "
                    + str(product_type)
                    + " "
                    + str(quantity_able_to_load)
                )
                # On remove 1 objet de la warehouse
                current_warehouse.stock[product_type] -= quantity_able_to_load

                Solution.append(
                    str(current_drone.id)
                    + " D "
                    + str(current_order.id)
                    + " "
                    + str(product_type)
                    + " "
                    + str(quantity_able_to_load)
                )
                current_drone.position = current_order.position

                # On remove 1 objet de l'order
                current_order.products_qty[product_type] -= quantity_able_to_load

    return Solution
