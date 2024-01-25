class Drone:
    def __init__(self, id, position, stock=[]):
        self.id: int = id  # Represents the index of the drone
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock
