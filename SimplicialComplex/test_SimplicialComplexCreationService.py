import unittest

import pytest

from SimplicialComplex.SimplicialComplexCreationService import get_simplexes


class TestGetSimplexes(unittest.TestCase):
    def test_generate_simplices():
        assert False

    def test_reformat_simplexes():
        assert False

    def test_get_frequencies_of_simplexes():
        assert False

    def test_simple_case(self):
        percentage_time = 1
        simplex_dim = [2, 3, 1]
        simplex_vertices = [0, 1, 2, 3, 4, 5, 6]
        expected_result = [[0, 1], [2, 3, 4], [5]]
        result = get_simplexes(percentage_time, simplex_dim, simplex_vertices)
        self.assertEqual(result, expected_result)

    def test_empty_simplex_vertices(self):
        percentage_time = 0.5
        simplex_dim = [3, 2, 1]
        simplex_vertices = []
        expected_result = []
        result = get_simplexes(percentage_time, simplex_dim, simplex_vertices)
        self.assertEqual(result, expected_result)

    def test_parse_files():
        assert False

    def test_list_faces():
        assert False
