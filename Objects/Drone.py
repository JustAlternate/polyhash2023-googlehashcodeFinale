from Objects import Warehouse
from math import sqrt, ceil


class Drone:

    def __init__(self, id, position, stock=[]):
        self.id: int = id
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock

    def load(self, warehouse: Warehouse, product: int, qty: int):
        pass

    def deliver(self, destination: tuple[int, int], product: int, qty: int):
        pass

    def unload(self, warehouse: Warehouse, product: int, qty: int):
        pass

    def wait(self, nb_turns: int):
        pass

    def calc_dist(self, destination: tuple[int, int]):
        return ceil(sqrt((destination[0] - self.position[0]) ** 2 +
                         (destination[1] - self.position[1]) ** 2))
