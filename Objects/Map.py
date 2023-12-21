class Map:

    def __init__(self, rows: int, cols: int, nb_drones: int, nb_turns: int, max_payload: int,
                 product_weights: list[int]):
        self.rows: int = rows
        self.cols: int = cols
        self.nb_drones: int = nb_drones
        self.nb_turns: int = nb_turns
        self.max_payload: int = max_payload
        self.product_weights: list[int] = product_weights
