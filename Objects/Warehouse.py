class Warehouse:
    def __init__(self, position: tuple[int, int], stock: list[int]):
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock  # Qty

    def is_empty(self):
        return self.stock == [0 for i in range(len(self.stock))]
