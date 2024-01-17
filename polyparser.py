#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Objects import *

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""


def parse_challenge(filename: str) -> Map:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, "r") as f:
        # Read infos map
        rows, columns, drone_count, deadline, max_load = [
            int(v) for v in f.readline().split()
        ]
        # Read infos product
        nb_product = int(f.readline())
        product_weights = [int(v) for v in f.readline().split()]
        challenge = Map(rows, columns, drone_count, deadline, max_load, product_weights)

        # Read infos warehouse
        nb_warehouse = int(f.readline())
        for id_warehouse in range(nb_warehouse):
            x, y = [int(v) for v in f.readline().split()]
            position = (x, y)
            stock = [0 for _ in range(nb_product)]
            for product, nb in enumerate([int(v) for v in f.readline().split()]):
                stock[product] += nb
            challenge.warehouses.append(Warehouse(id_warehouse, position, stock))

        # Read infos order
        nb_order = int(f.readline())
        for id_order in range(nb_order):
            x, y = [int(v) for v in f.readline().split()]
            position = (x, y)
            nb_item = int(f.readline())
            types = [int(v) for v in f.readline().split()]
            item_types = [0 for x in range(nb_product)]
            for item in types:
                item_types[item] += 1
            challenge.orders.append(Order(id_order, position, nb_item, item_types))

        # Spawn drones at warehouse0 position
        challenge.drones = [
            Drone(
                id_drone, challenge.warehouses[0].position, [0 for product in range(nb_product)]
            )
            for id_drone in range(challenge.nb_drones)
        ]

    return challenge
