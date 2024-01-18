from polyparser import parse_challenge
from utils.functs import (
    find_nearest_orders,
    find_closest_warehouse_with_item_qty,
    qty_drone_can_load,
    makeCommand
)


def naive_approach_theo(challenge):
    Solution = []
    Map = parse_challenge(challenge)

    ideal_cluster_size = 5  # Need to be edited later to test different cluster sizes

    orders = set(Map.orders)

    clustered_orders = set()

    clusters = {}

    # Creating clusters
    for current_order in orders:
        if current_order not in clustered_orders:
            num_cluster = len(clusters)

            clusters[num_cluster] = [current_order]
            clustered_orders.add(current_order)

            available_orders = orders - clustered_orders

            if (
                len(available_orders) < ideal_cluster_size
            ):  # Case when we don't have enough orders
                # When we don't have enough orders, we add all the remaining orders to the current cluster without restrictions
                for remaining_order in available_orders:
                    clusters[num_cluster].append(remaining_order)
                    clustered_orders.add(remaining_order)

            else:  # We make clusters with ideal size using the nearest orders
                nearest_orders = find_nearest_orders(
                    Map, current_order, available_orders, ideal_cluster_size
                )
                clusters[num_cluster].extend(nearest_orders)
                clustered_orders.update(nearest_orders)

    current_drone_index = 0
    # Completing orders for each cluster
    for cluster in clusters.values():
        for order in cluster:  # Should i create a cluster class ?
            current_drone_index = (current_drone_index + 1) % (len(Map.drones))
            current_drone = Map.drones[current_drone_index]
            for product_type in range(len(order.products_qty)):
                while order.products_qty[product_type] != 0:
                    quantity_able_to_load = qty_drone_can_load(
                        Map, product_type, order.id
                    )

                    # Try to find a warehouse with the needed quantity, if there is not, try to find one with less quantity
                    current_warehouse = find_closest_warehouse_with_item_qty(
                        Map, current_drone.id, product_type, quantity_able_to_load
                    )

                    # If no warehouse was found, try to find another one that have less quantity of the desired product
                    while current_warehouse == -1:
                        quantity_able_to_load -= 1
                        current_warehouse = find_closest_warehouse_with_item_qty(
                            Map, current_drone.id, product_type, quantity_able_to_load
                        )

                    makeCommand("L", current_drone.id, current_warehouse.id,
                                product_type, quantity_able_to_load)
                    # On remove 1 objet de la warehouse
                    current_warehouse.stock[product_type] -= quantity_able_to_load

                    makeCommand("D", current_drone.id, current_order.id,
                                product_type, quantity_able_to_load)
                    current_drone.position = order.position

                    # On remove 1 objet de l'order
                    order.products_qty[product_type] -= quantity_able_to_load

    return Solution
