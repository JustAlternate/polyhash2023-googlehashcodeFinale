#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Module de résolution du projet Poly#.
"""

from Objects import Map, Order
from polyparser import parse_challenge


class Destination:
    def __init__(self, position: tuple[int, int], game_map: Map):
        self.position: tuple[int, int] = position
        self.order_by_type: list[list[Order]] = \
            [[] for _ in range(len(game_map.product_weights))]
        self.sum_qty_type: list[int] = \
            [0 for _ in range(len(game_map.product_weights))]
        # Tri des distances entre la destination et toutes les warehouses
        self.index_nearby_warehouse = []
        for index_w, warehouse in enumerate(game_map.warehouses):
            self.index_nearby_warehouse.append(
                (Map.calc_dist(warehouse, self), warehouse))
        self.index_nearby_warehouse.sort(key=lambda x: x[0])
        self.index_nearby_warehouse = \
            [i[1] for i in self.index_nearby_warehouse]

    def add(self, order: Order):
        for product, qty in enumerate(order.products_qty):
            if order.products_qty[qty] > 0:
                self.order_by_type[product].append(order)
                self.sum_qty_type[product] += order.products_qty[product]
        return self


def naive_amedeo(challenge):
    """
    Naive approach that use every drones one by one
    and cycle through each orders
    one by one and each product_type one by one.
    """

    solution = []
    gameM: Map = parse_challenge(challenge)

    warehouseDroneDist: list[dict[int, int]] = [{i: (Map.calc_dist(
        gameM.drones[i], gameM.warehouses[x])) for i in range(gameM.nb_drones)}
        for x in range(len(gameM.warehouses))]

    # resemble les orders qui ont la meme destination
    order_trier_par_destination = {}
    for order in gameM.orders:
        if order.position not in order_trier_par_destination.keys():
            order_trier_par_destination[order.position] = Destination(
                order.position, gameM)
        order_trier_par_destination[order.position].add(order)

    # pour une meme destination
    for destination in order_trier_par_destination.values():

        # pour chaque type de produit
        for prodT, product_qty in enumerate(destination.sum_qty_type):
            # preselection des warehouse avec le produit
            # (on a deja trier par proximity)
            warehouseWithP = []
            for warehouse in destination.index_nearby_warehouse:
                if warehouse.stock[prodT] > 0:
                    product_qty -= warehouse.stock[prodT]
                    warehouseWithP.append(warehouse)
                if product_qty <= 0:
                    break

            # pour chaque order
            for ordC in destination.order_by_type[prodT]:
                # tant que pas finit
                while ordC.products_qty[prodT] > 0:
                    warehouse = warehouseWithP[0]

                    # meilleur distance entre tous les drones et les warehouse
                    droneCI = min(
                        warehouseDroneDist[warehouse.id].items(),
                        key=lambda t: t[1])

                    droneCI = droneCI[0]

                    # le chargement est limité par le payload,
                    # les stock de la warehouse
                    # et le nombre element restant à expedier
                    qtyL = min(
                        gameM.max_payload // gameM.product_weights[prodT],
                        gameM.warehouses[warehouse.id].stock[prodT],
                        ordC.products_qty[prodT])

                    solution.append(
                        str(droneCI)
                        + " L "
                        + str(warehouse.id)
                        + " "
                        + str(prodT)
                        + " "
                        + str(qtyL)
                    )
                    # On remove 1 objet de la warehouse
                    gameM.warehouses[warehouse.id].stock[prodT] -= qtyL

                    if warehouse.stock[prodT] <= 0:
                        del warehouseWithP[0]

                    solution.append(
                        str(droneCI)
                        + " D "
                        + str(ordC.id)
                        + " "
                        + str(prodT)
                        + " "
                        + str(qtyL)
                    )
                    gameM.drones[droneCI].position = ordC.position

                    # on met à jour la matrice
                    for i, v in enumerate(gameM.warehouses):
                        warehouseDroneDist[i][droneCI] = (
                            Map.calc_dist(gameM.drones[droneCI], v))

                    # On remove 1 objet de order
                    ordC.products_qty[prodT] -= qtyL

    return solution
