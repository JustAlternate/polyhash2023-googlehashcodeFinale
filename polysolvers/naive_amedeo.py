#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from math import ceil, sqrt

from Objects import Drone, Warehouse, Map
from polyparser import parse_challenge

"""
Module de résolution du projet Poly#.
"""


@dataclass
class Destination:
    position: tuple[int, int]
    order_by_type: list[list[int]]
    sum_qty_type: list[int]
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
    game_map: Map = parse_challenge(challenge)

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

    # Tri des distances entre les warehouses

    for assembler_destination, trier_index_order in order_trier_par_destination.items():
        # on tri les warehouse
        destination_warehouse_proche = []
        for index_w, warehouse in enumerate(game_map.warehouses):
            destination_warehouse_proche.append((calc_dist(warehouse.position, assembler_destination), index_w))
        destination_warehouse_proche.sort(key=lambda x: x[0])

        # on rasembles les order par type de produit et on somme les poi
        order_by_type: list[list[int]] = list()
        sum_weight = []
        for i in range(len(game_map.product_weights)):
            sum = 0
            order = []
            for k, v in enumerate(game_map.orders):
                if k in trier_index_order and v.products_qty[i] != 0:
                    sum += v.products_qty[i]
                    order.append(k)
            order_by_type.append(order)
            sum_weight.append(sum)

        # on rassemble les destinations des orders
        destinations.append(
            Destination(assembler_destination, order_by_type, sum_weight, [i[1] for i in destination_warehouse_proche]))

    # faire tourner l'exo

    # pour une meme destination
    for destination in destinations:

        print("ues")

        # pour chaque type de produit
        for product_type, product_qty in enumerate(destination.sum_qty_type):

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
            warehouse_with_the_product = [i[0] for i in warehouse_with_the_product]

            # pour chaque order
            for index_order_current in destination.order_by_type[product_type]:
                order = game_map.orders[index_order_current]

                # tant que pas finit
                while order.products_qty[product_type] > 0:
                    print(order.products_qty[product_type])

                    warehouse_index = warehouse_with_the_product[0]

                    # meilleur distance entre tous les drones et les warehouse
                    drone_index = min(warehouse_drones_distance_avec_chacun[warehouse_index].items(),
                                      key=lambda t: t[1])
                    print(warehouse_drones_distance_avec_chacun[warehouse_index])
                    print("drone_index", drone_index)

                    drone_index = drone_index[0]

                    # le chargement est limité par le payload,
                    # les stock de la warehouse et le nombre element restant à expedier
                    quantity_to_load = min(game_map.max_payload // game_map.product_weights[product_type],
                                           game_map.warehouses[warehouse_index].stock[product_type],
                                           order.products_qty[product_type])

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

                    for index, test_warehouse_index in enumerate(warehouse_with_the_product):
                        print(game_map.warehouses[test_warehouse_index].stock[product_type])
                        if game_map.warehouses[test_warehouse_index].stock[product_type] <= 0:
                            del warehouse_with_the_product[index]

                    solution.append(
                        str(drone_index)
                        + " D "
                        + str(index_order_current)
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
                    print(game_map.drones[drone_index].position, drone_index)

    return solution


print(naive_approach_autre("../challenges/a_example.in"))
