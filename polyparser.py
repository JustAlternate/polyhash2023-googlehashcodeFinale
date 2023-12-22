#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""
from Objects import Map, Warehouse, Order, Game


def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, 'r') as f:
        # Read infos map
        rows, columns, drone_count, deadline, max_load = [int(v) for v in f.readline().split()]
        # Read infos product
        nb_product = int(f.readline())
        type_of_product = [int(v) for v in f.readline().split()]
        Game.map = Map(rows, columns, drone_count, deadline, max_load, type_of_product)

        # Read infos warehouse
        nb_warehouse = int(f.readline())
        for wh in range(nb_warehouse):
            for v in f.read().split():
                position = (int(v[0]), int(v[1]))
            stock = list()
            for v in enumerate(f.read().split()):
                stock[v[0]] = int(v[1])
            Game.warehouses = Warehouse(position, stock)

        # Read infos order
        nb_order = int(f.readline())
        for order in range(nb_order):
            for v in f.read().split():
                position = (int(v[0]), int(v[1]))
            nb_item = int(f.readline())
            type_item = [int(v) for v in f.readline().split()]
            Game.orders = Order(position, nb_item, type_item)

    return Game
