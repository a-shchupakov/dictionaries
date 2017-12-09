import unittest
from dictionaries import *


dicts = [LinearSearchDict, BinarySearchDict, BinaryTreeDict, BalancedBinaryTreeDict, HashDict]
data = [(1, '1'), (2, '2'), (3, '3')]


class TestDict(unittest.TestCase):
    def add_get_test(self, dict_):
        d = dict_()

        for key, value in data:
            d[key] = value

        for key, value in data:
            self.assertEqual(value, d[key])

    def extract_items_test(self, dict_):
        d = dict_()

        for key, value in data:
            d[key] = value
        items = sorted(d.items(), key=lambda x: x[0])

        self.assertListEqual(items, data)

    def test_dicts(self):
        for dict_ in dicts:
            self.add_get_test(dict_)
            self.extract_items_test(dict_)
