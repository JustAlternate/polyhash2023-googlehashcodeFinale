from unittest import TestCase

from Objects import Map
from polyparser import parse_challenge


class Test(TestCase):
    def test_parse_challenge(self):
        test = parse_challenge("challenges/a_example.in")
        self.assertEqual(test.rows, 100)
        self.assertEqual(test.cols, 100)
        self.assertEqual(test.nb_drones, 3)
        self.assertEqual(test.nb_turns, 50)
        self.assertEqual(test.max_payload, 500)
        self.assertEqual(test.product_weights, [100, 5, 450])

        self.assertEqual(test.warehouses[0].position, (0, 0))
        self.assertEqual(test.warehouses[0].stock, [5, 1, 0])

        self.assertEqual(test.warehouses[1].position, (5, 5))
        self.assertEqual(test.warehouses[1].stock, [0, 10, 2])

        self.assertEqual(test.orders[0].destination, (1, 1))
        self.assertEqual(test.orders[0].nb_products, 2)
        self.assertEqual(test.orders[0].products_qty, [2, 0])

        self.assertEqual(test.orders[1].destination, (3, 3))
        self.assertEqual(test.orders[1].nb_products, 1)
        self.assertEqual(test.orders[1].products_qty, [0])

        self.assertEqual(test.orders[2].destination, (5, 6))
        self.assertEqual(test.orders[2].nb_products, 1)
        self.assertEqual(test.orders[2].products_qty, [2])
