class Drone:
    def __init__(self, id, position, stock=[]):
        self.id: int = id  # Represents the index of the drone
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock

    def reset_stock(self, nb_products: int):
        self.stock = [0] * nb_products
