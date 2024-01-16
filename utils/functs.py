def find_closest_warehouse_with_item_qty(
    Map, drone_index: int, item_type: int, qty: int
) -> int:
    """
    Return the index of the warehouse with the desired item_type and qty.
    If no warehouse matching criteria, Return -1
    """
    best_warehouse = (-1, -1)
    warehouses = Map.warehouses
    for index_warehouse in range(len(warehouses)):
        current_warehouse = warehouses[index_warehouse]
        if current_warehouse.stock[item_type] >= qty:
            current_dist = Map.drones[drone_index].calc_dist(current_warehouse.position)
            if current_dist <= best_warehouse[1] or best_warehouse[1] == -1:
                best_warehouse = (index_warehouse, current_dist)

    return best_warehouse[0]


def qty_drone_can_load(Map, product_type: int, order_index: int):
    """
    Return the max amount of product a drone can take for a specific product_type assuming that the drone is empty
    """
    current_order = Map.orders[order_index]
    qty_wanted = current_order.products_qty[product_type]
    product_type_weight = Map.product_weights[product_type]
    drone_max_payload = Map.max_payload

    return min(drone_max_payload // product_type_weight, qty_wanted)


def current_payload_drone(Map, Drone) -> int:
    """
    Return current payload of a specifc drone
    """
    product_weights = Map.product_weights
    current_load = sum(
        [qty * product_weights[ind] for ind, qty in enumerate(Drone.stock)]
    )

    return current_load


def max_qty_allowed_to_load(Map, Drone, product_type: int) -> int:
    """
    Return max qty that a drone can take for a specifc product and checking the current drone payload
    """
    product_weight = Map.product_weights[product_type]
    current_payload = current_payload_drone(Map, Drone)
    max_payload = Map.max_payload
    allowed_payload = max_payload - current_payload

    return allowed_payload // product_weight


def find_best_order(Map, Drone):
    """
    Return the best order for a drone to deliver choosed by amount of products that the drone can deliver and then by distance
    """
    orders = []
    # Order by qty then dist
    for index_order, order in enumerate(Map.orders):
        dist = Drone.calc_dist(order.destination)
        nb_prod_can_deliver = 0

        for prod_type, qty in enumerate(order.products_qty):
            nb_prod_can_deliver += min(qty, Drone.stock[prod_type])

        orders.append((index_order, nb_prod_can_deliver, dist))

    best = sorted(orders, key=lambda x: (-x[1], x[2]))[0]
    return best[0]
