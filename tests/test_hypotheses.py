"""Tests for hypothesis analysis."""

import pytest

from acf.hypotheses.analyzer import (
    HypothesisResult,
    evaluate_correlation,
    evaluate_threshold,
)


class TestEvaluateCorrelation:
    def test_supported_weak_correlation(self):
        result = evaluate_correlation(
            "H122.1",
            x_values=[1.0, 2.0, 3.0, 4.0, 5.0],
            y_values=[5.0, 5.0, 5.0, 5.0, 5.0],  # no correlation
            target_r=0.3,
            direction="less_than",
        )
        assert result.status == "supported"

    def test_not_supported_strong_correlation(self):
        result = evaluate_correlation(
            "H122.1",
            x_values=[1.0, 2.0, 3.0, 4.0, 5.0],
            y_values=[2.0, 4.0, 6.0, 8.0, 10.0],  # perfect correlation
            target_r=0.3,
            direction="less_than",
        )
        assert result.status == "not_supported"

    def test_insufficient_data(self):
        result = evaluate_correlation(
            "H122.1",
            x_values=[1.0, 2.0],
            y_values=[3.0, 4.0],
            target_r=0.3,
        )
        assert result.status == "insufficient_data"

    def test_greater_than_direction(self):
        result = evaluate_correlation(
            "H122.3",
            x_values=[1.0, 2.0, 3.0, 4.0, 5.0],
            y_values=[2.0, 4.0, 6.0, 8.0, 10.0],
            target_r=0.7,
            direction="greater_than",
        )
        assert result.status == "supported"


class TestEvaluateThreshold:
    def test_ge_pass(self):
        result = evaluate_threshold(
            "test", value=0.96, target=0.95,
            comparison="GE", description="Accuracy",
        )
        assert result.status == "supported"

    def test_ge_fail(self):
        result = evaluate_threshold(
            "test", value=0.80, target=0.95,
            comparison="GE", description="Accuracy",
        )
        assert result.status == "not_supported"

    def test_lt_pass(self):
        result = evaluate_threshold(
            "test", value=0.02, target=0.05,
            comparison="LT", description="Hallucination rate",
        )
        assert result.status == "supported"

    def test_result_has_evidence(self):
        result = evaluate_threshold(
            "H122.5", value=0.57, target=0.60,
            comparison="LT", description="L5-L6 accuracy",
        )
        assert result.evidence
        assert "0.570" in result.evidence
