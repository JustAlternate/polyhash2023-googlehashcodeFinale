#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Objects import *

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""

def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, 'r') as f:
        # Read infos map
        rows, columns, drone_count, deadline, max_load = [
            int(v) for v in f.readline().split()]
        # Read infos product
        nb_product = int(f.readline())
        type_of_product = [int(v) for v in f.readline().split()]
        challenge = Map(rows, columns, drone_count,
                        deadline, max_load, type_of_product)

        # Read infos warehouse
        nb_warehouse = int(f.readline())
        for _ in range(nb_warehouse):
            x, y = [int(v) for v in f.readline().split()]
            position = (x, y)
            stock = [0 for _ in range(nb_product)]
            for product, nb in enumerate([int(v) for v in f.readline().split()]):
                stock[product] += nb
            challenge.warehouses.append(Warehouse(position, stock))

        # Read infos order
        nb_order = int(f.readline())
        for order in range(nb_order):
            x, y = [int(v) for v in f.readline().split()]
            position = (x, y)
            nb_item = int(f.readline())
            types = [int(v) for v in f.readline().split()]
            item_types = [0 for x in range(nb_product)]
            for item in types:
                item_types[item] += 1
            challenge.orders.append(Order(position, nb_item, item_types))

    return challenge
