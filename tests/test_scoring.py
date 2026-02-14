"""Tests for ACF scoring engine."""

import pytest

from acf.scoring.profile import ACFProfile, ACFDimensionScore


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


class TestACFProfile:
    def test_aggregate_score(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        profile.dimensions["breadth"] = ACFDimensionScore(
            dimension="breadth", score=80.0, sub_level="B3",
        )
        profile.dimensions["depth"] = ACFDimensionScore(
            dimension="depth", score=60.0, sub_level="L3",
        )
        assert profile.aggregate_score == 70.0

    def test_empty_profile(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        assert profile.aggregate_score == 0.0

    def test_certification_levels(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        # ACF-1: < 20
        profile.dimensions["dim1"] = ACFDimensionScore(
            dimension="dim1", score=10.0, sub_level="1",
        )
        assert profile.certification_level == "ACF-1"

        # ACF-3: >= 40
        profile.dimensions["dim1"].score = 45.0
        assert profile.certification_level == "ACF-3"

        # ACF-6: >= 90
        profile.dimensions["dim1"].score = 95.0
        assert profile.certification_level == "ACF-6"

    def test_certification_label(self):
        profile = ACFProfile(
            system_id="test", system_type="llm", version="1.0",
        )
        profile.dimensions["dim1"] = ACFDimensionScore(
            dimension="dim1", score=95.0, sub_level="6",
        )
        assert profile.certification_label == "PhD / Board Certified"

    def test_roundtrip_serialization(self):
        profile = ACFProfile(
            system_id="my-system",
            system_type="neurosymbolic",
            version="2.0.0",
        )
        profile.dimensions["breadth"] = ACFDimensionScore(
            dimension="breadth", score=45.0, sub_level="B2",
            evidence="3 domains", confidence="measured",
        )
        profile.dimensions["depth"] = ACFDimensionScore(
            dimension="depth", score=78.0, sub_level="L4",
        )

        d = profile.to_dict()
        restored = ACFProfile.from_dict(d)

        assert restored.system_id == "my-system"
        assert restored.dimensions["breadth"].score == 45.0
        assert restored.dimensions["depth"].score == 78.0
        assert abs(restored.aggregate_score - profile.aggregate_score) < 0.1
