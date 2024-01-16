#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from math import ceil, sqrt

import Objects
from Objects import Drone, Warehouse
from polyparser import parse_challenge

"""
Module de résolution du projet Poly#.
"""


@dataclass
class Destination:
    position: tuple[int, int]
    index_orders: list[int]
    index_nearby_warehouse: list[int]


def quantity_drone_can_take(Map, product_type, current_order):
    """
    Return the max amount of product a drone can take for a specific product_type
    """
    qty_wanted = current_order.products_qty[product_type]
    product_type_weight = Map.product_weights[product_type]
    drone_max_payload = Map.max_payload

    return min(drone_max_payload // product_type_weight, qty_wanted)


def find_closest_warehouse(warehouses: list[Warehouse], drone: Drone, item_type: int) -> int:
    """
    Return the index of the warehouse with the desired item_type and qty.
    If no warehouse matching criteria, Return -1
    """
    best_warehouse = (-1, -1)
    for warehouse in warehouses:
        if warehouse.stock[item_type] >= qty:
            current_dist = drone.calc_dist(
                warehouse.position)
            if current_dist <= best_warehouse[1] or best_warehouse[1] == -1:
                best_warehouse = (warehouse, current_dist)

    return best_warehouse[0]


def calc_dist(origine: tuple[int, int], destination: tuple[int, int]):
    return ceil(sqrt((destination[0] - origine[0]) ** 2 +
                     (destination[1] - origine[1]) ** 2))


def naive_approach_autre(challenge):
    """
    Naive approch that use every drones one by one and cycle through each orders
    one by one and each product_type one by one.
    """

    solution = []
    game_map = parse_challenge(challenge)

    max_distance = ceil(sqrt(game_map.cols ** 2 + game_map.rows ** 2))

    warehouse_drones_distance_avec_chacun: list[dict[int, int]] = [{i: (game_map.drones[i]
                                                                        .calc_dist(game_map.warehouses[x].position)) for
                                                                    i in
                                                                    range(game_map.nb_drones)} for x in
                                                                   range(len(game_map.warehouses))]

    # resemble les orders qui ont la meme destination
    destinations: list[Destination] = []

    order_trier_par_destination = {}
    for index, order in enumerate(game_map.orders):
        if order.destination in order_trier_par_destination:
            order_trier_par_destination[order.destination].append(index)
        else:
            order_trier_par_destination[order.destination] = [index]

    # Tri des distances entre les warehouses et les destination des orders

    for destination, list_order in order_trier_par_destination.items():
        # on tri les warehouse
        destination_wharehouse_proche = []
        for index_w, warehouse in enumerate(game_map.warehouses):
            destination_wharehouse_proche.append((calc_dist(warehouse.position, destination), index_w))
        destination_wharehouse_proche.sort(key=lambda x: x[0])
        # metre les infos dans un endrois
        destinations.append(Destination(destination, list_order, [i[1] for i in destination_wharehouse_proche]))

    # faire tourner l'exo

    for destination in destinations:

        print("ues")

        for index_order_current in destination.index_orders:

            order = game_map.orders[index_order_current]

            for product_type, product_qty in enumerate(order.products_qty):

                # preselection des warehouse avec le produit (on a deja trier par proximity)
                warehouse_with_the_product = []
                for index_warehouse in destination.index_nearby_warehouse:
                    warehouse = game_map.warehouses[index_warehouse]
                    if warehouse.stock[product_type] > 0:
                        product_qty -= warehouse.stock[product_type]
                        warehouse_with_the_product.append((index_warehouse, warehouse.stock[product_type]))
                    if product_qty <= 0:
                        break
                warehouse_with_the_product.sort(key=lambda x: x[1])

                while order.products_qty[product_type] > 0:
                    print(order.products_qty[product_type])

                    # meilleur distance entre tous les drones et les warehouse
                    for warehouse_index, warehouse_stock in warehouse_with_the_product:
                        if warehouse_stock < 0:
                            continue
                        drone_index = min(warehouse_drones_distance_avec_chacun[warehouse_index].items(),
                                          key=lambda t: t[1])[0]

                        quantity_to_load = min(game_map.max_payload // game_map.product_weights[product_type],
                                               warehouse_stock, order.products_qty[product_type])

                        solution.append(
                            str(drone_index)
                            + " L "
                            + str(warehouse_index)
                            + " "
                            + str(product_type)
                            + " "
                            + str(quantity_to_load)
                        )
                        # On remove 1 objet de la warehouse
                        game_map.warehouses[warehouse_index].stock[product_type] -= quantity_to_load

                        solution.append(
                            str(drone_index)
                            + " D "
                            + str(warehouse_index)
                            + " "
                            + str(product_type)
                            + " "
                            + str(quantity_to_load)
                        )
                        game_map.drones[drone_index].position = order.destination

                        # on met à jour la matrice
                        for i, v in enumerate(game_map.warehouses):
                            warehouse_drones_distance_avec_chacun[i][drone_index] = (
                                game_map.drones[drone_index].calc_dist(v.position))

                        # On remove 1 objet de order
                        order.products_qty[product_type] -= quantity_to_load

    return solution


print(naive_approach_autre("../challenges/a_example.in"))
