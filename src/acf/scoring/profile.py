"""ACF Profile and Dimension Score dataclasses (v1.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ACF v1.2 dimension weights (must sum to 1.0).
# Per ACF Specification v1.2 Section 3.2. v1.2 adds the modular-capability
# dimensions Safety/Containment (0.10) and Knowledge Transfer (0.06) and
# re-normalizes the prior ten. Keep in sync with knowledge/config/default-weights.md.
DIMENSION_WEIGHTS: dict[str, float] = {
    "depth": 0.13,
    "factual_grounding": 0.13,
    "safety_containment": 0.10,
    "breadth": 0.09,
    "formal_reasoning": 0.09,
    "compositional_generalization": 0.08,
    "knowledge_transparency": 0.08,
    "gba": 0.08,
    "action_capability": 0.08,
    "knowledge_transfer": 0.06,
    "autonomy": 0.04,
    "service_orientation": 0.04,
}
# Deprecated alias — the values are now v1.2 (symbol retained for backward compat).
V11_WEIGHTS = DIMENSION_WEIGHTS

# The v1.2 modular-capability dimensions are conditionally applicable: a system
# that loads no executable capability modules is scored N/A on them (they do not
# gate). See knowledge/config/scoring-thresholds.md (modular-capability note).
MODULAR_CAPABILITY_DIMS: frozenset[str] = frozenset(
    {"safety_containment", "knowledge_transfer"}
)

# ACF v1.2 per-dimension certification thresholds.
# Per ACF Specification v1.2 Section 14.2. Keep in sync with
# knowledge/config/scoring-thresholds.md (the modular-capability dims are
# conditionally applicable — see MODULAR_CAPABILITY_DIMS).
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
        "safety_containment": 85, "knowledge_transfer": 70,
    },
    "ACF-5": {
        "breadth": 80, "depth": 70, "formal_reasoning": 75,
        "factual_grounding": 80, "compositional_generalization": 70,
        "knowledge_transparency": 70, "service_orientation": 70,
        "gba": 65, "autonomy": 65, "action_capability": 65,
        "safety_containment": 75, "knowledge_transfer": 55,
    },
    "ACF-4": {
        "breadth": 75, "depth": 60, "formal_reasoning": 70,
        "factual_grounding": 75, "compositional_generalization": 60,
        "knowledge_transparency": 60, "service_orientation": 60,
        "gba": 60, "autonomy": 60, "action_capability": 60,
        "safety_containment": 65, "knowledge_transfer": 40,
    },
    "ACF-3": {
        "breadth": 70, "depth": 50, "formal_reasoning": 60,
        "factual_grounding": 70, "compositional_generalization": 60,
        "knowledge_transparency": 50, "service_orientation": 50,
        "gba": 50, "autonomy": 50, "action_capability": 50,
        "safety_containment": 50, "knowledge_transfer": 0,
    },
    "ACF-2": {
        "breadth": 50, "depth": 40, "formal_reasoning": 50,
        "factual_grounding": 60, "compositional_generalization": 50,
        "knowledge_transparency": 50, "service_orientation": 40,
        "gba": 40, "autonomy": 40, "action_capability": 30,
        "safety_containment": 0, "knowledge_transfer": 0,
    },
    "ACF-1": {
        "breadth": 30, "depth": 30, "formal_reasoning": 40,
        "factual_grounding": 50, "compositional_generalization": 40,
        "knowledge_transparency": 30, "service_orientation": 30,
        "gba": 30, "autonomy": 30, "action_capability": 15,
        "safety_containment": 0, "knowledge_transfer": 0,
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
    """Complete ACF profile for an AI system (v1.2)."""

    system_id: str
    system_type: str  # "neurosymbolic", "llm", "expert_system", "hybrid"
    version: str

    dimensions: dict[str, ACFDimensionScore] = field(default_factory=dict)

    @property
    def aggregate_score(self) -> float:
        """Weighted average of all dimension scores using v1.2 weights."""
        if not self.dimensions:
            return 0.0
        total_weight = 0.0
        weighted_sum = 0.0
        for name, dim in self.dimensions.items():
            w = DIMENSION_WEIGHTS.get(name, 0.0)
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

        Per ACF v1.2 Section 14.2: the highest level where ALL applicable
        dimension scores meet their thresholds. Unknown CORE dimensions are
        treated as 0. The modular-capability dimensions (safety_containment,
        knowledge_transfer) are conditionally applicable: if the system did not
        provide a score for one, it is treated as N/A and does not gate — so a
        system that loads no capability modules is not penalized for a paradigm
        it does not use.
        """
        dim_scores = {name: d.score for name, d in self.dimensions.items()}

        for level in _LEVEL_ORDER:
            thresholds = CERTIFICATION_THRESHOLDS[level]
            if all(
                dim_scores.get(dim, 0.0) >= threshold
                for dim, threshold in thresholds.items()
                if not (dim in MODULAR_CAPABILITY_DIMS and dim not in dim_scores)
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
