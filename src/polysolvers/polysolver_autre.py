#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de résolution du projet Poly#.
"""
from src.Objects import Map
from src.polyparser import parse_challenge
from src.utils.functs import sort_objects_by_distance_from_obj, makeCommand


# class Destination:
#     def __init__(self, position: tuple[int, int], game_map: Map):
#         self.position: tuple[int, int] = position
#         self.order_by_type: list[list[Order]] = \
#             [[] for _ in range(len(game_map.product_weights))]
#         self.sum_qty_type: list[int] = \
#             [0 for _ in range(len(game_map.product_weights))]
#         # Tri des distances entre la destination et toutes les warehouses
#         self.index_nearby_warehouse = []
#         for index_w, warehouse in enumerate(game_map.warehouses):
#             self.index_nearby_warehouse.append(
#                 (Map.calc_dist(warehouse, self), warehouse))
#         self.index_nearby_warehouse.sort(key=lambda x: x[0])
#         self.index_nearby_warehouse = \
#             [i[1] for i in self.index_nearby_warehouse]
#
#     def add(self, order: Order):
#         for product, qty in enumerate(order.products_qty):
#             if order.products_qty[qty] > 0:
#                 self.order_by_type[product].append(order)
#                 self.sum_qty_type[product] += order.products_qty[product]
#         return self


def naive_approach_autre(challenge):
    """
    Naive approach that use every drones one by one
    and cycle through each orders
    one by one and each product_type one by one.
    """

    solution = []
    gameM: Map = parse_challenge(challenge)

    # warehouseDroneDist: list[dict[int, int]] = [{i: (Map.calc_dist(
    # gameM.drones[i], gameM.warehouses[x])) for i in range(gameM.nb_drones)}
    # for x in range(len(gameM.warehouses))]

    # order_by_type: list[list[Order]] = \
    #     [[] for _ in range(len(gameM.product_weights))]
    # type_by_warehouse: list[list[int]] = \
    #     [[] for _ in range(len(gameM.warehouses))]
    oWeightSort = sorted(gameM.orders, key=lambda x: x.total_weight)
    # for order in oWeightSort:
    #     for product_type, _ in enumerate(order.products_qty):
    #         if order.products_qty[product_type] > 0:
    #             order_by_type[product_type].append(order)

    # on trie les warehouse par distance par rapport à warehouse 0
    # On prend la premiere warehouse
    # on regarde les produit qu'ont peut finir directe et prendre tout les loads sont ecrit et les delivry aussi
    # si il reste des produit ou des dronne on refait
    # le calcule avec les produit restant ref la 2eme warehouse on recommence
    # on prend les produit restant et on les met dans la 2eme warehouse

    dPointer = 0

    wDistSort = sort_objects_by_distance_from_obj(
        gameM, gameM.warehouses[0], gameM.warehouses)

    # pour une meme warehouse
    #    for wCurent in wDistSort:

    # on trie les meilleur order a faire pour les produit disponible
    # for prodT, product_qty in enumerate(wCurent.stock):
    #     if product_qty > 0:
    #         type_by_warehouse[wCurent].append(prodT)

    # prendre les meilleur order pour les produit disponible
    # order_by_type
    # type_by_warehouse
    # oWeightSort
    # wDistSort

    commendL: list[tuple[int, int, int, int]] = []
    commendD: list[tuple[int, int, int, int]] = []

    # wPointerInit = 0
    # pour chaque ordre
    for oCurent in oWeightSort:
        dPointer = (dPointer + 1) % gameM.nb_drones - 1
        dCurent = gameM.drones[dPointer]
        dCurent.order = oCurent.id
        # wPointer = wPointerInit
        wPointer = 0
        wCurent = wDistSort[wPointer]
        print("order : ", oCurent.id, "drone : ", dCurent.id, "warehouse : ", wCurent.id)

        # si on peut finir les orders avec la warehouse
        for prodT, _ in enumerate(oCurent.products_qty):
            while oCurent.products_qty[prodT] > 0:
                # si le produit ne contient pas le produit on passe au plus proche
                if wCurent.stock[prodT] <= 0:
                    wPointer = (wPointer + 1) % len(wDistSort)
                    wCurent = wDistSort[wPointer]
                    continue
                print("prod", "warehouse :", wPointer, "type :", prodT, "qty :", oCurent.products_qty[prodT])
                # si on a envoyé tous les drones on les envoye et on reprend le premier
                # (pourais faire le plus proche nope car il faut aussi trier les warehouse)
                while dCurent.total_load + gameM.product_weights[prodT] >= gameM.max_payload:
                    if (dPointer + 1) % gameM.nb_drones == 0:
                        videDrone(commendL, commendD, solution, dCurent, gameM, oCurent)
                    dPointer = (dPointer + 1) % gameM.nb_drones
                    dCurent = gameM.drones[dPointer]
                    print("drone : ", dPointer)

                # le chargement est limité par le payload,
                # le stock de la warehouse
                # et le nombre element restant à expediter
                qtyL = min(
                    gameM.max_payload // gameM.product_weights[prodT],
                    wCurent.stock[prodT],
                    oCurent.products_qty[prodT])

                commendL.append((dCurent.id, wCurent.id, prodT, qtyL))

                # On remove 1 objet de la warehouse
                wCurent.stock[prodT] -= qtyL

                # On ajoute 1 objet au drone
                dCurent.stock[prodT] += qtyL
                dCurent.total_load += gameM.product_weights[prodT] * qtyL

                print("total", dCurent.id, dCurent.total_load)

                # On suprime 1 objet a faire a l'order
                oCurent.products_qty[prodT] -= qtyL

        videDrone(commendL, commendD, solution, dCurent, gameM, oCurent)

    return solution


def videDrone(commendL, commendD, solution, dCurent, gameM, oCurent):
    print("vidage")
    for prodT, prodQTY in enumerate(dCurent.stock):
        if prodQTY > 0:
            commendD.append((dCurent.id, oCurent.id, prodT, prodQTY))
            # On remove 1 objet de order
            oCurent.products_qty[prodT] -= prodQTY
            # On ajoute 1 objet au drone
            dCurent.stock[prodT] -= prodQTY
            dCurent.total_load -= gameM.product_weights[prodT] * prodQTY
    for c in commendL:
        makeCommand("L", solution, *c)
    commendL.clear()
    for c in commendD:
        makeCommand("D", solution, *c)
    commendD.clear()
