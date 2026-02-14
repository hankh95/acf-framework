"""
Understanding Efficiency Ratio (UER) Calculator.

    UER = Understanding / Compute

Where Understanding = Breadth x Depth x Domain_count:
- Breadth: topic coverage (0.0-1.0)
- Depth: weighted average Bloom level performance
- Domain_count: number of knowledge domains

UER enables cross-paradigm comparison (neurosymbolic vs LLM vs expert system).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Bloom level weights — higher levels contribute more to depth score
BLOOM_WEIGHTS: dict[str, float] = {
    "L1": 1.0,   # Remember
    "L2": 2.0,   # Understand
    "L3": 3.0,   # Apply
    "L4": 4.0,   # Analyze
    "L5": 5.0,   # Evaluate
    "L6": 6.0,   # Create
}

MAX_UER = 1_000_000.0
MIN_COMPUTE = 0.001  # 3.6 seconds


@dataclass
class TrainingSnapshot:
    """Point-in-time metrics from a system's training."""

    system_id: str
    version: str

    # Training volume
    documents_processed: int = 0
    knowledge_units_extracted: int = 0  # triples, weights, rules, etc.

    # Curriculum coverage (breadth)
    topics_total: int = 0
    topics_covered: int = 0

    # Bloom level scores (depth) — L1 through L6, each 0.0-1.0
    bloom_scores: dict[str, float] = field(default_factory=dict)

    # Domain coverage
    domains: list[str] = field(default_factory=list)

    # Compute cost
    gpu_hours: float = 0.0
    wall_clock_hours: float = 0.0


@dataclass
class UnderstandingScore:
    """Decomposed understanding score."""

    breadth: float       # 0.0-1.0
    depth: float         # 0.0-1.0
    domain_count: int
    composite: float     # breadth x depth x domain_count


@dataclass
class UERResult:
    """Complete UER computation result."""

    system_id: str
    version: str
    understanding: UnderstandingScore
    gpu_hours: float
    wall_clock_hours: float
    total_compute: float
    uer: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "system_id": self.system_id,
            "version": self.version,
            "understanding": {
                "breadth": round(self.understanding.breadth, 4),
                "depth": round(self.understanding.depth, 4),
                "domain_count": self.understanding.domain_count,
                "composite": round(self.understanding.composite, 4),
            },
            "gpu_hours": round(self.gpu_hours, 4),
            "wall_clock_hours": round(self.wall_clock_hours, 4),
            "total_compute": round(self.total_compute, 4),
            "uer": round(self.uer, 4),
        }


@dataclass
class UERComparison:
    """Cross-version or cross-system UER comparison."""

    from_id: str
    to_id: str
    from_uer: float
    to_uer: float
    uer_delta: float
    uer_ratio: float      # >1 = improvement
    breadth_delta: float
    depth_delta: float
    compute_ratio: float  # >1 = more efficient


def calculate_understanding(snapshot: TrainingSnapshot) -> UnderstandingScore:
    """Compute understanding score from a training snapshot."""
    breadth = (
        snapshot.topics_covered / snapshot.topics_total
        if snapshot.topics_total > 0 else 0.0
    )

    if not snapshot.bloom_scores:
        depth = 0.0
    else:
        weighted_sum = 0.0
        weight_total = 0.0
        for level, score in snapshot.bloom_scores.items():
            weight = BLOOM_WEIGHTS.get(level, 1.0)
            weighted_sum += score * weight
            weight_total += weight
        depth = weighted_sum / weight_total if weight_total > 0 else 0.0

    domain_count = len(snapshot.domains)
    composite = breadth * depth * max(domain_count, 1)

    return UnderstandingScore(
        breadth=breadth,
        depth=depth,
        domain_count=domain_count,
        composite=composite,
    )


def calculate_uer(snapshot: TrainingSnapshot) -> UERResult:
    """Compute UER for a single system snapshot."""
    understanding = calculate_understanding(snapshot)

    total_compute = snapshot.gpu_hours + snapshot.wall_clock_hours
    if total_compute < MIN_COMPUTE:
        total_compute = MIN_COMPUTE

    uer = min(understanding.composite / total_compute, MAX_UER)

    return UERResult(
        system_id=snapshot.system_id,
        version=snapshot.version,
        understanding=understanding,
        gpu_hours=snapshot.gpu_hours,
        wall_clock_hours=snapshot.wall_clock_hours,
        total_compute=total_compute,
        uer=uer,
    )


def compare_uer(
    from_snapshot: TrainingSnapshot,
    to_snapshot: TrainingSnapshot,
) -> UERComparison:
    """Compare UER between two snapshots."""
    from_result = calculate_uer(from_snapshot)
    to_result = calculate_uer(to_snapshot)

    uer_delta = to_result.uer - from_result.uer
    uer_ratio = to_result.uer / from_result.uer if from_result.uer > 0 else float("inf")
    breadth_delta = to_result.understanding.breadth - from_result.understanding.breadth
    depth_delta = to_result.understanding.depth - from_result.understanding.depth
    compute_ratio = (
        from_result.total_compute / to_result.total_compute
        if to_result.total_compute > 0 else float("inf")
    )

    return UERComparison(
        from_id=f"{from_snapshot.system_id}@{from_snapshot.version}",
        to_id=f"{to_snapshot.system_id}@{to_snapshot.version}",
        from_uer=from_result.uer,
        to_uer=to_result.uer,
        uer_delta=uer_delta,
        uer_ratio=uer_ratio,
        breadth_delta=breadth_delta,
        depth_delta=depth_delta,
        compute_ratio=compute_ratio,
    )
