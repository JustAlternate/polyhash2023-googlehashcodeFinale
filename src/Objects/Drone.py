class Drone:
    def __init__(self, id, position, stock=[]):
        self.id: int = id  # Represents the index of the drone
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock
        self.total_load: int = 0
        self.order: int = 0

    def reset_stock(self, nb_products: int):
        self.stock = [0] * nb_products
