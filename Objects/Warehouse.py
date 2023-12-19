class Warehouse:

    def __init__(self, position: tuple[int, int], stock: list[int]):
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock  # Qty
