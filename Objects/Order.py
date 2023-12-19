class Order:

    def __init__(self, destination: tuple[int, int], nb_products: int, products_qty: list[int]):
        self.destination: tuple[int, int] = destination
        self.nb_products: int = nb_products
        self.products_qty: list[int] = products_qty
        self.fullfilled: bool = False
