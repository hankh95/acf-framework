"""Tests for statistical utility functions."""

import math

import pytest

from acf.utils.stats import mean, std_dev, pearson_correlation, percentile


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_single_value(self):
        assert mean([42]) == 42.0

    def test_empty(self):
        assert mean([]) == 0.0


class TestStdDev:
    def test_basic(self):
        result = std_dev([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(result - 2.0) < 0.01

    def test_constant(self):
        assert std_dev([5, 5, 5, 5]) == 0.0

    def test_insufficient_data(self):
        assert std_dev([1]) == 0.0
        assert std_dev([]) == 0.0


class TestPearsonCorrelation:
    def test_perfect_positive(self):
        r = pearson_correlation([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        assert abs(r - 1.0) < 0.001

    def test_perfect_negative(self):
        r = pearson_correlation([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])
        assert abs(r - (-1.0)) < 0.001

    def test_no_correlation(self):
        r = pearson_correlation([1, 2, 3, 4, 5], [3, 3, 3, 3, 3])
        assert r == 0.0

    def test_insufficient_data(self):
        assert pearson_correlation([1], [2]) == 0.0
        assert pearson_correlation([], []) == 0.0


class TestPercentile:
    def test_median(self):
        assert percentile([1, 2, 3, 4, 5], 50) == 3.0

    def test_min_max(self):
        assert percentile([1, 2, 3, 4, 5], 0) == 1.0
        assert percentile([1, 2, 3, 4, 5], 100) == 5.0

    def test_empty(self):
        assert percentile([], 50) == 0.0
