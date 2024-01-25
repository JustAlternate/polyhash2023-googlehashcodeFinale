from Objects import Order


class Warehouse:
    def __init__(self, index: int, position: tuple[int, int], stock: list[int]):
        self.index = index  # Represents the index of the warehouse
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock  # Qty
        self.nearest_orders = list[Order]
        self.type_of_order = list[int]  # used by naive_amedeo

    def is_empty(self):
        return self.stock == [0 for i in range(len(self.stock))]
