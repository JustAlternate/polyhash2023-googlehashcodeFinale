from polyparser import parse_challenge
from utils.functs import (
    sort_objects_by_distance_from_obj,
    find_closest_warehouse,
    max_qty_allowed_to_load,
    makeCommand,
    find_closest_cluster_for_warehouse,
    calc_total_weight_order,
    sort_orders_by_weight,
    sort_clusters_by_distance_from_cluster,
    find_best_cluster
)

import copy
from typing import List


def naive_approach_theo(challenge: str) -> List[str]:
    """
    The idea is to create clusters of closest orders
    and then to complete each cluster.

    We use a system of ranking to sort the best clusters by
    the weight coefficient and distance coefficient.

    For each cluster we complete each order one by one by looking
    at the nearest warehouse with the needed quantity.

    When we complet a cluster we choose the best cluster
    and we repeat the process until there is no more clusters.
    """
    # Initialization
    solution = []
    challenge = parse_challenge(challenge)

    weightcoeff = 0.9  # The importance of weight in the ranking
    distcoeff = 0.1  # The importance of distance in the ranking
    ideal_cluster_size = 2  # 2 is the best for now

    orders = challenge.orders

    clustered_orders = []
    clusters = {}

    # We calculate the total weight of each order
    for order in orders:
        weight_order = calc_total_weight_order(challenge, order)
        order.total_weight = weight_order

    # We sort the orders by weight
    orders = sort_orders_by_weight(orders)

    # We calculate the ranking weight for each order (by position in the list)
    for weight_ind, order in enumerate(orders):
        order.ranking_weight = (len(orders) - weight_ind) / len(orders)

    # Creating clusters
    for current_order in orders:
        # if order not clustered
        if current_order not in clustered_orders:

            # We create a new cluster
            num_cluster = len(clusters)
            clusters[num_cluster] = [
                [current_order], current_order.ranking_weight, 0, 0]
            # by default the order is set in the cluster
            # clusters[num_cluster][0] = orders in the cluster
            # clusters[num_cluster][1] = ranking weight
            # clusters[num_cluster][2] = dist ranking
            # clusters[num_cluster][3] ranking score

            # We add the order to the clustered orders
            clustered_orders.append(current_order)

            # We fetch the available orders
            available_orders = [
                order for order in orders if order not in clustered_orders]

            # if there is not enough orders to make a cluster
            if (len(available_orders) < ideal_cluster_size):
                # We add all the remaining orders to the
                # current cluster without restrictions

                for remaining_order in available_orders:
                    clusters[num_cluster][0].append(remaining_order)
                    clusters[num_cluster][1] += remaining_order.ranking_weight
                    clustered_orders.append(remaining_order)

            # We make clusters with ideal size using the nearest orders
            else:
                # we fetch the nearest orders
                nearest_orders = sort_objects_by_distance_from_obj(
                    challenge,
                    current_order,
                    available_orders,
                    ideal_cluster_size
                )
                # We add the nearest orders to the cluster
                clusters[num_cluster][0].extend(nearest_orders)

                for order in nearest_orders:
                    clusters[num_cluster][1] += order.ranking_weight
                clustered_orders.extend(nearest_orders)

            # We calculate the average ranking weight for the cluster
            clusters[num_cluster][1] /= len(clusters[num_cluster][0])

    # Completing orders for each cluster

    # The first cluster chosen is the one with the highest ranking score
    cluster_id = find_closest_cluster_for_warehouse(
        challenge, challenge.warehouses[0], clusters)

    # We iterate through the drones to complete the clusters
    drone_index = 0
    while len(clusters) > 0:  # While there is clusters to complete

        # We choose the drone index
        if drone_index + 1 > len(challenge.drones) - 1:
            drone_index = 0
        else:
            drone_index += 1
        drone = challenge.drones[drone_index]

        # We fetch the cluster with its id
        cluster = clusters[cluster_id]
        # We create a copy of the cluster
        # that we are going to use to calculate
        # the next cluster
        tmp_cluster = copy.deepcopy(cluster)

        # While there is orders to complete in the cluster
        while len(cluster[0]) != 0:
            # We fetch the first order of the cluster
            order = cluster[0][0]

            # While the order is not completed
            while not order.check_full_filled():
                # The idea is to load fully the drone each time
                # to try to optimize the number of turns used

                # We reset the drone stock
                drone.reset_stock(len(order.products_qty))

                # We iterate through the products of the order
                for product_type in range(len(order.products_qty)):
                    qty_order = order.products_qty[product_type]

                    if qty_order > 0:  # If we need the product
                        # We look at how much we can load with the drone
                        max_qty_able_load = max_qty_allowed_to_load(
                            challenge, drone, product_type
                        )

                        # We choose the quantity to load
                        # if the drone can take more than the order needs
                        # we take the quantity needed
                        # else we take the max quantity the drone can take
                        qty = min(qty_order, max_qty_able_load)
                        if qty > 0:
                            warehouse, qty = find_closest_warehouse(
                                challenge,
                                drone.id,
                                product_type,
                                qty
                            )

                            # We move the drone to the warehouse
                            drone.position = warehouse.position

                            # We load the drone for the solution
                            makeCommand(
                                "L",
                                solution,
                                drone.id,
                                warehouse.id,
                                product_type,
                                qty,
                            )
                            # We update the stock of the drone
                            # and the warehouse
                            drone.stock[product_type] += qty
                            warehouse.stock[product_type] -= qty

                # We move the drone to the order
                drone.position = order.position
                for product_type, qty_prod in enumerate(drone.stock):
                    # if the drone has the product needed
                    if qty_prod > 0:
                        # We deliver the product
                        makeCommand(
                            "D",
                            solution,
                            drone.id,
                            order.id,
                            product_type,
                            qty_prod
                        )
                        order.products_qty[product_type] -= qty_prod

            # We remove the order from the cluster
            cluster[0].pop(0)
            # The next order will be the first of the cluster

        # Once we are done with the cluster
        # We calculate the ranking score for each cluster
        # and we choose the best cluster to go to
        del clusters[cluster_id]
        if len(clusters) - 1 >= 0:
            # Ranking by distance from the cluster
            calc_clusters_by_dist = sort_clusters_by_distance_from_cluster(
                challenge, tmp_cluster, clusters)

            # Updating the ranking
            for ind_dist, id_cluster in enumerate(calc_clusters_by_dist):
                cluster = clusters[id_cluster]
                cluster[2] = (len(clusters) - ind_dist) / len(clusters)
                cluster[3] = weightcoeff * \
                    cluster[1] + distcoeff * cluster[2]

            # We choose the best cluster according to the ranking
            cluster_id = find_best_cluster(clusters)

    return solution
