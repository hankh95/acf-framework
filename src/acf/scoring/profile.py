"""ACF Profile and Dimension Score dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    """Complete ACF profile for an AI system."""

    system_id: str
    system_type: str  # "neurosymbolic", "llm", "expert_system", "hybrid"
    version: str

    dimensions: dict[str, ACFDimensionScore] = field(default_factory=dict)

    @property
    def aggregate_score(self) -> float:
        """Weighted average of all dimension scores."""
        if not self.dimensions:
            return 0.0
        return sum(d.score for d in self.dimensions.values()) / len(self.dimensions)

    @property
    def certification_level(self) -> str:
        """Determine ACF certification level from aggregate score."""
        score = self.aggregate_score
        if score >= 90:
            return "ACF-6"
        elif score >= 75:
            return "ACF-5"
        elif score >= 60:
            return "ACF-4"
        elif score >= 40:
            return "ACF-3"
        elif score >= 20:
            return "ACF-2"
        else:
            return "ACF-1"

    @property
    def certification_label(self) -> str:
        """Human-readable certification level."""
        labels = {
            "ACF-1": "Elementary",
            "ACF-2": "Middle School",
            "ACF-3": "High School",
            "ACF-4": "Bachelor's",
            "ACF-5": "Master's / Professional",
            "ACF-6": "PhD / Board Certified",
        }
        return labels.get(self.certification_level, "Unknown")

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
