from Objects import Drone


class Order:
    def __init__(self,
                 index,
                 position: tuple[int, int],
                 nb_products: int,
                 products_qty: list[int]):
        self.index: int = index  # Represents the real index of the order
        self.position: tuple[int, int] = position
        self.nb_products: int = nb_products
        self.products_qty: list[int] = products_qty
        self.total_weight: int = 0  # Used by naive_theo
        self.ranking_weight: float = 0.0  # Used by naive_theo
        self.drones: set[Drone] = set()  # Used by naive_amedeo

    def check_full_filled(self):
        return self.products_qty == [0] * len(self.products_qty)
