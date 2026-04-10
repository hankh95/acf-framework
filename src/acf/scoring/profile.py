"""ACF Profile and Dimension Score dataclasses (v1.1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ACF v1.1 dimension weights (must sum to 1.0).
# Per ACF Specification v1.1 Section 3.2.
V11_WEIGHTS: dict[str, float] = {
    "depth": 0.15,
    "factual_grounding": 0.15,
    "breadth": 0.10,
    "formal_reasoning": 0.10,
    "compositional_generalization": 0.10,
    "knowledge_transparency": 0.10,
    "gba": 0.10,
    "action_capability": 0.10,
    "autonomy": 0.05,
    "service_orientation": 0.05,
}

# ACF v1.1 per-dimension certification thresholds.
# Per ACF Specification v1.1 Section 14.2.
# Format: level -> {dimension: min_score}
# Order: [breadth, depth, formal_reasoning, factual_grounding,
#         compositional_generalization, knowledge_transparency,
#         service_orientation, gba, autonomy, action_capability]
CERTIFICATION_THRESHOLDS: dict[str, dict[str, float]] = {
    "ACF-6": {
        "breadth": 90, "depth": 80, "formal_reasoning": 80,
        "factual_grounding": 85, "compositional_generalization": 75,
        "knowledge_transparency": 80, "service_orientation": 80,
        "gba": 75, "autonomy": 70, "action_capability": 75,
    },
    "ACF-5": {
        "breadth": 80, "depth": 70, "formal_reasoning": 75,
        "factual_grounding": 80, "compositional_generalization": 70,
        "knowledge_transparency": 70, "service_orientation": 70,
        "gba": 65, "autonomy": 65, "action_capability": 65,
    },
    "ACF-4": {
        "breadth": 75, "depth": 60, "formal_reasoning": 70,
        "factual_grounding": 75, "compositional_generalization": 60,
        "knowledge_transparency": 60, "service_orientation": 60,
        "gba": 60, "autonomy": 60, "action_capability": 60,
    },
    "ACF-3": {
        "breadth": 70, "depth": 50, "formal_reasoning": 60,
        "factual_grounding": 70, "compositional_generalization": 60,
        "knowledge_transparency": 50, "service_orientation": 50,
        "gba": 50, "autonomy": 50, "action_capability": 50,
    },
    "ACF-2": {
        "breadth": 50, "depth": 40, "formal_reasoning": 50,
        "factual_grounding": 60, "compositional_generalization": 50,
        "knowledge_transparency": 50, "service_orientation": 40,
        "gba": 40, "autonomy": 40, "action_capability": 30,
    },
    "ACF-1": {
        "breadth": 30, "depth": 30, "formal_reasoning": 40,
        "factual_grounding": 50, "compositional_generalization": 40,
        "knowledge_transparency": 30, "service_orientation": 30,
        "gba": 30, "autonomy": 30, "action_capability": 15,
    },
}

CERTIFICATION_LABELS: dict[str, str] = {
    "ACF-0": "Below Elementary",
    "ACF-1": "Elementary",
    "ACF-2": "Secondary",
    "ACF-3": "Undergraduate",
    "ACF-4": "Graduate",
    "ACF-5": "Professional",
    "ACF-6": "Expert",
}

# Level order from highest to lowest for gating
_LEVEL_ORDER = ["ACF-6", "ACF-5", "ACF-4", "ACF-3", "ACF-2", "ACF-1"]


@dataclass
class ACFDimensionScore:
    """Score for a single ACF dimension."""

    dimension: str
    score: float           # 0-100
    sub_level: str         # e.g., "B2", "L4", "GBA2"
    evidence: str = ""     # How this was determined
    confidence: str = "measured"  # "measured", "estimated", "projected"

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "score": round(self.score, 1),
            "sub_level": self.sub_level,
            "evidence": self.evidence,
            "confidence": self.confidence,
        }


@dataclass
class ACFProfile:
    """Complete ACF profile for an AI system (v1.1)."""

    system_id: str
    system_type: str  # "neurosymbolic", "llm", "expert_system", "hybrid"
    version: str

    dimensions: dict[str, ACFDimensionScore] = field(default_factory=dict)

    @property
    def aggregate_score(self) -> float:
        """Weighted average of all dimension scores using v1.1 weights."""
        if not self.dimensions:
            return 0.0
        total_weight = 0.0
        weighted_sum = 0.0
        for name, dim in self.dimensions.items():
            w = V11_WEIGHTS.get(name, 0.0)
            if w > 0:
                weighted_sum += dim.score * w
                total_weight += w
        if total_weight == 0:
            # Fallback to simple average if no known dimensions
            return sum(d.score for d in self.dimensions.values()) / len(self.dimensions)
        return weighted_sum

    @property
    def certification_level(self) -> str:
        """Determine ACF certification level using per-dimension gating.

        Per ACF v1.1 Section 14.2: the highest level where ALL dimension
        scores meet their thresholds. Unknown dimensions are treated as 0.
        """
        dim_scores = {name: d.score for name, d in self.dimensions.items()}

        for level in _LEVEL_ORDER:
            thresholds = CERTIFICATION_THRESHOLDS[level]
            if all(
                dim_scores.get(dim, 0.0) >= threshold
                for dim, threshold in thresholds.items()
            ):
                return level
        return "ACF-0"

    @property
    def certification_label(self) -> str:
        """Human-readable certification level."""
        return CERTIFICATION_LABELS.get(self.certification_level, "Unknown")

    def dimension_scores_dict(self) -> dict[str, float]:
        """Return dimension name -> score mapping."""
        return {name: d.score for name, d in self.dimensions.items()}

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON export."""
        return {
            "system_id": self.system_id,
            "system_type": self.system_type,
            "version": self.version,
            "aggregate_score": round(self.aggregate_score, 1),
            "certification_level": self.certification_level,
            "certification_label": self.certification_label,
            "dimensions": {
                name: d.to_dict()
                for name, d in self.dimensions.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ACFProfile:
        """Deserialize from dict."""
        profile = cls(
            system_id=data["system_id"],
            system_type=data.get("system_type", "unknown"),
            version=data.get("version", ""),
        )
        for name, dim_data in data.get("dimensions", {}).items():
            profile.dimensions[name] = ACFDimensionScore(
                dimension=dim_data.get("dimension", name),
                score=dim_data["score"],
                sub_level=dim_data.get("sub_level", ""),
                evidence=dim_data.get("evidence", ""),
                confidence=dim_data.get("confidence", "measured"),
            )
        return profile
