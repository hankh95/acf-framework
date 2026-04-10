"""Tests for ACF scoring engine (v1.1 — 10 dimensions, per-dimension gating)."""

import pytest

from acf.scoring.profile import (
    ACFProfile,
    ACFDimensionScore,
    V11_WEIGHTS,
    CERTIFICATION_THRESHOLDS,
    CERTIFICATION_LABELS,
)
from acf.scoring.scorer import (
    score_action_capability,
    score_autonomy,
    score_breadth,
    score_compositional_generalization,
    score_depth,
    score_factual_grounding,
    score_formal_reasoning,
    score_gba,
    score_knowledge_transparency,
    score_service_orientation,
    BLOOM_DEPTH_MAP,
)


class TestACFDimensionScore:
    def test_to_dict(self):
        score = ACFDimensionScore(
            dimension="depth",
            score=72.5,
            sub_level="L4",
            evidence="Strong L1-L4",
        )
        d = score.to_dict()
        assert d["score"] == 72.5
        assert d["sub_level"] == "L4"
        assert d["dimension"] == "depth"

    def test_score_rounded_in_dict(self):
        score = ACFDimensionScore(
            dimension="breadth", score=72.333, sub_level="B3",
        )
        assert score.to_dict()["score"] == 72.3


class TestV11Weights:
    def test_weights_sum_to_one(self):
        total = sum(V11_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001, f"Weights sum to {total}, expected 1.0"

    def test_ten_dimensions(self):
        assert len(V11_WEIGHTS) == 10

    def test_no_zero_weights(self):
        for name, w in V11_WEIGHTS.items():
            assert w > 0, f"Dimension {name} has zero weight"

    def test_depth_and_fg_highest(self):
        assert V11_WEIGHTS["depth"] == 0.15
        assert V11_WEIGHTS["factual_grounding"] == 0.15

    def test_action_capability_weight(self):
        assert V11_WEIGHTS["action_capability"] == 0.10


class TestACFProfileAggregate:
    def test_weighted_aggregate(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        # All dimensions at 80 -> weighted aggregate = 80
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=80.0, sub_level="X",
            )
        assert abs(profile.aggregate_score - 80.0) < 0.01

    def test_weighted_aggregate_asymmetric(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        # Only depth (15%) at 100, rest at 0 -> aggregate = 15
        profile.dimensions["depth"] = ACFDimensionScore(
            dimension="depth", score=100.0, sub_level="L6",
        )
        for dim in V11_WEIGHTS:
            if dim != "depth":
                profile.dimensions[dim] = ACFDimensionScore(
                    dimension=dim, score=0.0, sub_level="X0",
                )
        assert abs(profile.aggregate_score - 15.0) < 0.01

    def test_empty_profile(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        assert profile.aggregate_score == 0.0

    def test_partial_dimensions(self):
        """If only some dimensions are present, aggregate uses only those weights."""
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        profile.dimensions["depth"] = ACFDimensionScore(
            dimension="depth", score=100.0, sub_level="L6",
        )
        profile.dimensions["breadth"] = ACFDimensionScore(
            dimension="breadth", score=100.0, sub_level="B4",
        )
        # depth=100*0.15 + breadth=100*0.10 = 25, total_weight=0.25
        # aggregate = 25.0
        assert abs(profile.aggregate_score - 25.0) < 0.01


class TestACFCertificationGating:
    def test_acf6_all_95(self):
        profile = ACFProfile(
            system_id="test", system_type="neurosymbolic", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=95.0, sub_level="X",
            )
        assert profile.certification_level == "ACF-6"

    def test_acf3_all_70(self):
        profile = ACFProfile(
            system_id="test", system_type="neurosymbolic", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=70.0, sub_level="X",
            )
        assert profile.certification_level == "ACF-3"

    def test_acf1_all_50(self):
        """All-50: meets ACF-1 but not ACF-2 (fg needs 60)."""
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=50.0, sub_level="X",
            )
        assert profile.certification_level == "ACF-1"

    def test_acf0_all_10(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=10.0, sub_level="X",
            )
        assert profile.certification_level == "ACF-0"

    def test_lowest_dimension_gates_level(self):
        """All dims at ACF-5 level except breadth at 50 -> gates to ACF-2."""
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=80.0, sub_level="X",
            )
        profile.dimensions["breadth"].score = 50.0
        assert profile.certification_level == "ACF-2"

    def test_ac_gates_acf3(self):
        """ACF-3 requires AC >= 50. If AC is 45, should be ACF-2."""
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=70.0, sub_level="X",
            )
        profile.dimensions["action_capability"].score = 45.0
        assert profile.certification_level == "ACF-2"

    def test_missing_dimension_treated_as_zero(self):
        """If a dimension is missing, it's treated as 0 for gating."""
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        # Only 9 dimensions, missing action_capability
        for dim in V11_WEIGHTS:
            if dim != "action_capability":
                profile.dimensions[dim] = ACFDimensionScore(
                    dimension=dim, score=95.0, sub_level="X",
                )
        # Missing AC (treated as 0) gates to ACF-0
        assert profile.certification_level == "ACF-0"


class TestCertificationLabels:
    def test_all_labels(self):
        for level in ["ACF-0", "ACF-1", "ACF-2", "ACF-3", "ACF-4", "ACF-5", "ACF-6"]:
            assert CERTIFICATION_LABELS[level] is not None


class TestActionCapability:
    def test_perfect_execution(self):
        score = score_action_capability(1.0, 1.0, 1.0)
        assert abs(score.score - 100.0) < 0.01
        assert score.sub_level == "AC4"

    def test_typical_nusy(self):
        # Paper 128: PER=0.80, SCR=0.90, ACR=0.85 -> 61.2
        score = score_action_capability(0.80, 0.90, 0.85)
        assert abs(score.score - 61.2) < 0.1
        assert score.sub_level == "AC3"

    def test_expert_system(self):
        # Paper 128: PER=0.95, SCR=0.95, ACR=0.95 -> 85.7
        score = score_action_capability(0.95, 0.95, 0.95)
        assert abs(score.score - 85.7) < 0.1
        assert score.sub_level == "AC4"

    def test_low_execution(self):
        # PER=0.20, SCR=0.30, ACR=0.40 -> 2.4
        score = score_action_capability(0.20, 0.30, 0.40)
        assert score.score < 5.0
        assert score.sub_level == "AC0"

    def test_ac1_threshold(self):
        # Need composite >= 15: PER*SCR*ACR >= 0.15
        score = score_action_capability(0.50, 0.50, 0.60)
        assert score.score == 15.0
        assert score.sub_level == "AC1"

    def test_zero_per(self):
        score = score_action_capability(0.0, 0.90, 0.90)
        assert score.score == 0.0


class TestScorerFunctions:
    def test_breadth_basic(self):
        score = score_breadth(8, 10, 3, 4, 5)
        assert score.dimension == "breadth"
        assert score.score > 0

    def test_depth_basic(self):
        score = score_depth({"L1": 0.9, "L2": 0.8, "L3": 0.7})
        assert score.dimension == "depth"
        assert score.score > 0

    def test_action_capability_in_scorer(self):
        score = score_action_capability(0.80, 0.90, 0.85)
        assert score.dimension == "action_capability"

    def test_create_profile_with_action_capability(self):
        from acf.scoring.scorer import ACFScorer

        profile = ACFScorer.create_profile(
            "test-system",
            "neurosymbolic",
            "1.0",
            breadth=score_breadth(8, 10, 3, 4, 5),
            depth=score_depth({"L1": 0.9, "L2": 0.8, "L3": 0.7}),
            action_capability=score_action_capability(0.80, 0.90, 0.85),
        )
        assert "action_capability" in profile.dimensions
        assert profile.dimensions["action_capability"].score > 0


class TestRoundtripSerialization:
    def test_roundtrip_with_action_capability(self):
        profile = ACFProfile(
            system_id="my-system",
            system_type="neurosymbolic",
            version="1.1.0",
        )
        for dim in V11_WEIGHTS:
            profile.dimensions[dim] = ACFDimensionScore(
                dimension=dim, score=70.0, sub_level="X",
                evidence="test", confidence="measured",
            )

        d = profile.to_dict()
        restored = ACFProfile.from_dict(d)

        assert restored.system_id == "my-system"
        assert len(restored.dimensions) == 10
        assert abs(restored.aggregate_score - profile.aggregate_score) < 0.1
        assert restored.certification_level == profile.certification_level

    def test_roundtrip_preserves_ac(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        profile.dimensions["action_capability"] = ACFDimensionScore(
            dimension="action_capability", score=61.2,
            sub_level="AC3", evidence="PER=80%, SCR=90%, ACR=85%",
        )
        d = profile.to_dict()
        restored = ACFProfile.from_dict(d)
        assert abs(restored.dimensions["action_capability"].score - 61.2) < 0.1
