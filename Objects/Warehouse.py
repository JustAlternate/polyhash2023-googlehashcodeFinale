from Objects.Order import *


class Warehouse:
    def __init__(self, id: int, position: tuple[int, int], stock: list[int]):
        self.id = id  # Represents the index of the warehouse
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock  # Qty
        self.nearest_orders = list[Order]

    def is_empty(self):
        return self.stock == [0 for i in range(len(self.stock))]
