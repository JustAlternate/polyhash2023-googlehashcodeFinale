def find_closest_warehouse_with_item_quantity(Map, drone_index: int, item_type: int, qty: int) -> int:
    """
    Return the index of the warehouse with the desired item_type and qty.
    If no warehouse matching criteria, Return -1
    """
    best_warehouse = (-1, -1)
    warehouses = Map.warehouses
    for index_warehouse in range(len(warehouses)):
        current_warehouse = warehouses[index_warehouse]
        if current_warehouse.stock[item_type] >= qty:
            current_dist = Map.drones[drone_index].calc_dist(
                current_warehouse.position)
            if current_dist <= best_warehouse[1] or best_warehouse[1] == -1:
                best_warehouse = (index_warehouse, current_dist)

    return best_warehouse[0]


def quantity_drone_can_take(Map, product_type, order_index):
    """
    Return the max amount of product a drone can take for a specific product_type
    """
    current_order = Map.orders[order_index]
    qty_wanted = current_order.products_qty[product_type]
    product_type_weight = Map.product_weights[product_type]
    drone_max_payload = Map.max_payload

    return min(drone_max_payload // product_type_weight, qty_wanted)
