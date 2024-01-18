def find_closest_warehouse_with_item_qty(
    Map, drone_index: int, item_type: int, qty: int
) -> int:
    """
    Return the index of the warehouse with the desired item_type and qty.
    If no warehouse matching criteria, Return -1
    """
    best_warehouse = (-1, -1)
    warehouses = Map.warehouses
    for current_warehouse in warehouses:
        if current_warehouse.stock[item_type] >= qty:
            current_dist = Map.calc_dist(
                Map.drones[drone_index], current_warehouse
            )
            if current_dist <= best_warehouse[1] or best_warehouse[1] == -1:
                best_warehouse = (current_warehouse, current_dist)

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


def find_best_order(Map, Drone):  # Might use this later
    """
    return the index of the best order for a drone to deliver choosed by amount of products that the drone can deliver and then by distance
    """
    orders = []
    # Order by qty then dist
    for index_order, order in enumerate(Map.orders):
        dist = Map.calc_dist(order, Drone)
        nb_prod_can_deliver = 0

        for prod_type, qty in enumerate(order.products_qty):
            nb_prod_can_deliver += min(qty, Drone.stock[prod_type])

        orders.append((index_order, nb_prod_can_deliver, dist))

    best = sorted(orders, key=lambda x: (-x[1], x[2]))[0]
    return best[0]


def makeCommand(action: str, Solution: list, drone_id: int, dest_id: int, product_type: int, qty: int) -> None:
    """
    Take an action either "L" or "D" and write a string to append into the list Solution
    exemple : makeCommand("L", [], 0, 1, 0, 2)
    Solution -> ["0 L 1 2 2"]
    return nothing
    """
    Solution.append(
        str(drone_id)+" "+str(action)+" "+str(dest_id) +
        " "+str(product_type)+" "+str(qty)
    )


def find_nearest_orders(Map, Order, available_orders, ideal_cluster_size):
    nearest_orders = []

    for available_order in available_orders:
        calc_dist = Map.calc_dist(Order, available_order)
        nearest_orders.append((calc_dist, available_order))

    nearest_orders = sorted(nearest_orders, key=lambda x: x[0])
    nearest_orders = [order[1] for order in nearest_orders]

    nearest_orders = nearest_orders[0: ideal_cluster_size - 1]

    return nearest_orders
