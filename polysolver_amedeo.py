#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from math import ceil, sqrt

from Objects import Drone, Warehouse, Map, Order
from polyparser import parse_challenge

"""
Module de résolution du projet Poly#.
"""


class Destination:
    def __init__(self, position: tuple[int, int], game_map: Map):
        self.position: tuple[int, int] = position
        self.order_by_type: list[list[Order]] = [[] for _ in range(len(game_map.product_weights))]
        self.sum_qty_type: list[int] = [0 for _ in range(len(game_map.product_weights))]
        # Tri des distances entre la destination et toutes les warehouses
        self.index_nearby_warehouse = []
        for index_w, warehouse in enumerate(game_map.warehouses):
            self.index_nearby_warehouse.append(
                (calc_dist(warehouse.position, self.position), warehouse))
        self.index_nearby_warehouse.sort(key=lambda x: x[0])
        self.index_nearby_warehouse = [i[1] for i in self.index_nearby_warehouse]

    def add(self, order: Order):
        for product, qty in enumerate(order.products_qty):
            if order.products_qty[qty] > 0:
                self.order_by_type[product].append(order)
                self.sum_qty_type[product] += order.products_qty[product]
        return self


def calc_dist(origine: tuple[int, int], destination: tuple[int, int]):
    return ceil(sqrt((destination[0] - origine[0]) ** 2 +
                     (destination[1] - origine[1]) ** 2))


def naive_approach_amedeo(challenge):
    """
    Naive approch that use every drones one by one and cycle through each orders
    one by one and each product_type one by one.
    """

    solution = []
    game_map: Map = parse_challenge(challenge)

    warehouse_drones_distance_avec_chacun: list[dict[int, int]] = [{i: (game_map.drones[i]
                                                                        .calc_dist(game_map.warehouses[x].position)) for
                                                                    i in
                                                                    range(game_map.nb_drones)} for x in
                                                                   range(len(game_map.warehouses))]

    # resemble les orders qui ont la meme destination
    order_trier_par_destination = {}
    for order in game_map.orders:
        if order.destination not in order_trier_par_destination.keys():
            order_trier_par_destination[order.destination] = Destination(order.destination, game_map)
        order_trier_par_destination[order.destination].add(order)

    # pour une meme destination
    for destination in order_trier_par_destination.values():

        # pour chaque type de produit
        for product_type, product_qty in enumerate(destination.sum_qty_type):
            # preselection des warehouse avec le produit (on a deja trier par proximity)
            warehouse_with_the_product = []
            for warehouse in destination.index_nearby_warehouse:
                if warehouse.stock[product_type] > 0:
                    product_qty -= warehouse.stock[product_type]
                    warehouse_with_the_product.append(warehouse)
                if product_qty <= 0:
                    break

            # pour chaque order
            for order_current in destination.order_by_type[product_type]:
                # tant que pas finit
                while order_current.products_qty[product_type] > 0:
                    warehouse = warehouse_with_the_product[0]

                    # meilleur distance entre tous les drones et les warehouse
                    drone_index = min(warehouse_drones_distance_avec_chacun[warehouse.id].items(),
                                      key=lambda t: t[1])

                    drone_index = drone_index[0]

                    # le chargement est limité par le payload,
                    # les stock de la warehouse et le nombre element restant à expedier
                    quantity_to_load = min(game_map.max_payload // game_map.product_weights[product_type],
                                           game_map.warehouses[warehouse.id].stock[product_type],
                                           order_current.products_qty[product_type])

                    solution.append(
                        str(drone_index)
                        + " L "
                        + str(warehouse.id)
                        + " "
                        + str(product_type)
                        + " "
                        + str(quantity_to_load)
                    )
                    # On remove 1 objet de la warehouse
                    game_map.warehouses[warehouse.id].stock[product_type] -= quantity_to_load

                    if warehouse.stock[product_type] <= 0:
                        del warehouse_with_the_product[0]

                    solution.append(
                        str(drone_index)
                        + " D "
                        + str(order_current)
                        + " "
                        + str(product_type)
                        + " "
                        + str(quantity_to_load)
                    )
                    game_map.drones[drone_index].position = order_current.destination

                    # on met à jour la matrice
                    for i, v in enumerate(game_map.warehouses):
                        warehouse_drones_distance_avec_chacun[i][drone_index] = (
                            game_map.drones[drone_index].calc_dist(v.position))

                    # On remove 1 objet de order
                    order_current.products_qty[product_type] -= quantity_to_load

    return solution
