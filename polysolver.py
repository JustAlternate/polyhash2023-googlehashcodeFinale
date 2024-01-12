#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polyparser import parse_challenge

"""
Module de résolution du projet Poly#.
"""


def find_closest_warehouse_with_item_quantity(Map, drone_index: int, item_type: int, qty: int) -> int:
    """
    Return the index of the warehouse with the desired item_type and qty.
    If no warehouse matching criteria, Return -1
    """
    best_warehouse = (-1, -1)
    warehouses = Map.warehouses
    for index_warehouse in range(len(warehouses)):
        current_warehouse = warehouses[index_warehouse]
        if current_warehouse.stock[item_type] >= qty:
            current_dist = Map.drones[drone_index].calc_dist(
                current_warehouse.position)
            if current_dist <= best_warehouse[1] or best_warehouse[1] == -1:
                best_warehouse = (index_warehouse, current_dist)

    return best_warehouse[0]


def quantity_drone_can_take(Map, product_type, order_index):
    """
    Return the max amount of product a drone can take for a specific product_type
    """
    current_order = Map.orders[order_index]
    qty_wanted = current_order.products_qty[product_type]
    product_type_weight = Map.product_weights[product_type]
    drone_max_payload = Map.max_payload

    return min(drone_max_payload // product_type_weight, qty_wanted)


def naive_approach_loic(challenge):
    """
    Naive approch that use every drones one by one and cycle through each orders
    one by one and each product_type one by one.
    """

    Solution = []
    Map = parse_challenge(challenge)

    current_drone_index = 0
    for index_order in range(len(Map.orders)):

        # We change drone for a new order
        current_drone_index = (current_drone_index + 1) % (len(Map.drones))
        print(current_drone_index)
        current_drone = Map.drones[current_drone_index]
        current_order = Map.orders[index_order]

        for product_type in range(len(current_order.products_qty)):

            while current_order.products_qty[product_type] != 0:
                quantity_able_to_load = quantity_drone_can_take(
                    Map, product_type, index_order
                )

                # Try to find a warehouse with the needed quantity, if there is not, try to find one with less quantity
                index_warehouse = find_closest_warehouse_with_item_quantity(
                    Map, 0, product_type, quantity_able_to_load
                )

                # If no warehouse was found, try to find another one that have less quantity of the desired product
                while index_warehouse == -1:
                    quantity_able_to_load -= 1
                index_warehouse = find_closest_warehouse_with_item_quantity(
                    Map, 0, product_type, quantity_able_to_load
                )

                current_warehouse = Map.warehouses[index_warehouse]

                Solution.append(
                    str(current_drone_index)
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
                    str(current_drone_index)
                    + " D "
                    + str(index_order)
                    + " "
                    + str(product_type)
                    + " "
                    + str(quantity_able_to_load)
                )
                current_drone.position = current_order.destination

                # On remove 1 objet de l'order
                current_order.products_qty[product_type] -= quantity_able_to_load

    return Solution
