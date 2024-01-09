#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from polyparser import parse_challenge
import sys


def printR(txt): return ("\033[91m"+str(txt)+"\033[00m")
def printG(txt): return ("\033[92m"+str(txt)+"\033[00m")


def Map_visualizer_init(challenge):
    Map = parse_challenge(challenge)

    number_needed = max(len(str(len(Map.warehouses))),
                        len(str(len(Map.orders))))-1

    print("X = rien")
    print(printG("X")+" = order n°X")
    print(printR("X")+" = warehouse n°X")
    print("Les drones commencent toujours sur la warehouse n°0")

    TabMap = []  # X = rien , X en rouge = warehouse n°X, X en vert = order n°X
    for row in range(Map.rows - 1):
        TabMap.append([])
        for col in range(Map.cols):
            TabMap[row].append(("X", number_needed-1))

    for warehouse_index in range(len(Map.warehouses)):
        dest = Map.warehouses[warehouse_index].position
        TabMap[dest[0]][dest[1]] = (printR(warehouse_index), warehouse_index)

    for order_index in range(len(Map.orders)):
        dest = Map.orders[order_index].destination
        TabMap[dest[0]][dest[1]] = (printG(order_index), order_index)

    for row in TabMap:
        print("")
        print("|", end="")
        for item in row:
            print(item[0]+(str(" ")*(number_needed-len(str(item[1])))), end="")

            print("|", end="")
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python polyvisualizer challenges/ma_map.in")
    else:
        Map_visualizer_init(sys.argv[1])
