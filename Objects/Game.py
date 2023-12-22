import dataclasses

from Objects import Order, Drone, Warehouse, Map


@dataclasses.dataclass
class Game:
    map: Map
    warehouses: list[Warehouse]
    orders: list[Order]
    drones: list[Drone]
