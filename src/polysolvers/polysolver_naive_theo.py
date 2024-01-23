from polyparser import parse_challenge
from utils.functs import (
    sort_objects_by_distance_from_obj,
    find_closest_warehouse,
    qty_drone_can_load,
    makeCommand,
    find_closest_cluster_for_warehouse,
    calc_total_weight_order,
    sort_orders_by_weight,
    sort_clusters_by_distance_from_cluster,
    find_best_cluster
)


def naive_approach_theo(challenge):  # Closest clusters approach
    """
    The idea is to create clusters of closest orders
    and then to complete each cluster

    For each cluster we complete each order one by one by looking
    at the nearest warehouse with the needed quantity

    When we have completed a cluster we choose the nearest cluster
    and we repeat the process until there is no more clusters
    """
    solution = []
    challenge = parse_challenge(challenge)

    weightcoeff = 0.9
    distcoeff = 0.1

    # Need to be edited later to test different cluster sizes
    ideal_cluster_size = 2
    orders = challenge.orders

    for order in orders:

        weight_order = calc_total_weight_order(challenge, order)
        order.total_weight = weight_order

    orders = sort_orders_by_weight(orders)

    clustered_orders = []

    clusters = {}

    for weight_ind, order in enumerate(orders):

        order.ranking_weight = (len(orders) - weight_ind) / len(orders)

    # Creating clusters
    for current_order in orders:
        if current_order not in clustered_orders:

            num_cluster = len(clusters)
            clusters[num_cluster] = [
                [current_order], current_order.ranking_weight, 0, 0]
            # for clusters : clusters[2] = dist ranking
            # and clusters[3] ranking score
            clustered_orders.append(current_order)

            available_orders = [
                order for order in orders if order not in clustered_orders]

            if (len(available_orders) < ideal_cluster_size):
                # Case when we don't have enough orders
                # When we don't have enough orders, we add all the remaining
                # orders to the current cluster without restrictions

                for remaining_order in available_orders:
                    clusters[num_cluster][0].append(remaining_order)
                    clusters[num_cluster][1] += remaining_order.ranking_weight
                    clustered_orders.append(remaining_order)

            # We make clusters with ideal size using the nearest orders
            else:
                nearest_orders = sort_objects_by_distance_from_obj(
                    challenge,
                    current_order,
                    available_orders,
                    ideal_cluster_size
                )
                clusters[num_cluster][0].extend(nearest_orders)
                for order in nearest_orders:
                    clusters[num_cluster][1] += order.ranking_weight
                clustered_orders.extend(nearest_orders)

            clusters[num_cluster][1] /= len(clusters[num_cluster][0])

    current_drone_index = 0
    # Completing orders for each cluster
    cluster_id = find_closest_cluster_for_warehouse(
        challenge, challenge.warehouses[0], clusters)
    while len(clusters) != 0:
        cluster = clusters[cluster_id]

        tmp_cluster = cluster.copy()
        for order in cluster[0]:  # Should i create a cluster class ?
            current_drone_index = (
                current_drone_index + 1) % (len(challenge.drones))
            current_drone = challenge.drones[current_drone_index]
            for product_type in range(len(order.products_qty)):
                while order.products_qty[product_type] != 0:
                    quantity_able_to_load = qty_drone_can_load(
                        challenge, product_type, order.id
                    )

                    # Try to find a warehouse with the needed quantity, if
                    # there is not, try to find one with less quantity
                    current_warehouse, qty = find_closest_warehouse(
                        challenge,
                        current_drone.id,
                        product_type,
                        quantity_able_to_load
                    )

                    makeCommand(
                        "L",
                        solution,
                        current_drone.id,
                        current_warehouse.id,
                        product_type,
                        qty,
                    )
                    # On remove 1 objet de la warehouse
                    current_warehouse.stock[product_type] -= qty

                    makeCommand(
                        "D",
                        solution,
                        current_drone.id,
                        order.id,
                        product_type,
                        qty,
                    )
                    current_drone.position = order.position

                    # On remove 1 objet de l'order
                    order.products_qty[product_type] -= qty

        del clusters[cluster_id]
        if len(clusters) - 1 >= 0:
            calc_clusters_by_dist = sort_clusters_by_distance_from_cluster(
                challenge, tmp_cluster, clusters)

            for ind_dist, id_cluster in enumerate(calc_clusters_by_dist):
                cluster = clusters[id_cluster]
                cluster[2] = (len(clusters) - ind_dist) / len(clusters)
                cluster[3] = weightcoeff * cluster[1] + distcoeff * cluster[2]

            cluster_id = find_best_cluster(clusters)

    return solution
