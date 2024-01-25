from copy import deepcopy


class Cluster:

    def __init__(self, cluster_id, weight_coeff, dist_coeff):
        self.cluster_id = cluster_id

        self.weight_coeff = weight_coeff
        self.dist_coeff = dist_coeff

        self.orders = []

        self.weight_ranking = 0
        self.dist_ranking = 0
        self.score_ranking = 0

        self.position = None

    def calc_weight_ranking(self):
        self.weight_ranking = 0
        for order in self.orders:
            self.weight_ranking += order.weight_ranking

        self.weight_ranking /= len(self.orders)

    def append_orders(self, orders):
        if isinstance(orders, list):
            self.orders.extend(orders)
        else:
            self.orders.append(orders)
        if len(self.orders) > 0:
            self.calc_weight_ranking()
            self.position = self.orders[0].position

    def get_first_order(self):
        if len(self.orders) > 0:
            return self.orders[0]

    def del_order_full_filled(self, order):
        self.orders.remove(order)

    def calc_score_ranking(self):
        self.score_ranking = self.weight_ranking * \
            self.weight_coeff + self.dist_ranking * self.dist_coeff

    def calc_dist_ranking(self, dist_pos, nb_clusters):
        self.dist_ranking = (nb_clusters - dist_pos) / nb_clusters
        self.calc_score_ranking()

    def copy_cluster(self):
        return deepcopy(self)

    def are_orders_full_filled(self):
        return len(self.orders) == 0
