"""
ACF Scorer: Score AI systems across the 9 ACF dimensions.

Each dimension has a scoring function that takes raw metrics and returns
an ACFDimensionScore. The ACFScorer aggregates dimension scores into
a complete ACFProfile with certification level.
"""

from __future__ import annotations

from typing import Optional

from acf.scoring.profile import ACFDimensionScore, ACFProfile


# Bloom level to depth score mapping
BLOOM_DEPTH_MAP = {
    "L1": 17,   # Remember
    "L2": 33,   # Understand
    "L3": 50,   # Apply
    "L4": 67,   # Analyze
    "L5": 83,   # Evaluate
    "L6": 100,  # Create
}


def score_breadth(
    topics_covered: int,
    topics_total: int,
    domain_count: int,
    cross_domain_passed: int = 0,
    cross_domain_total: int = 0,
) -> ACFDimensionScore:
    """Score Breadth dimension (B1-B4).

    B1: Topic existence (coverage > 0)
    B2: Topic coverage > 50%
    B3: Coverage > 80% + cross-domain
    B4: Full coverage + cross-domain integration
    """
    if topics_total == 0:
        return ACFDimensionScore("breadth", 0.0, "B0", "No curriculum defined")

    coverage = topics_covered / topics_total
    cross_domain = (
        cross_domain_passed / cross_domain_total
        if cross_domain_total > 0 else 0.0
    )

    if coverage >= 0.95 and domain_count >= 3 and cross_domain >= 0.8:
        score = 90 + (coverage - 0.95) * 200
        sub_level = "B4"
    elif coverage >= 0.80 and domain_count >= 2:
        score = 60 + (coverage - 0.80) * 150
        sub_level = "B3"
    elif coverage >= 0.50:
        score = 30 + (coverage - 0.50) * 100
        sub_level = "B2"
    elif coverage > 0:
        score = coverage * 60
        sub_level = "B1"
    else:
        score = 0.0
        sub_level = "B0"

    return ACFDimensionScore(
        "breadth", min(score, 100.0), sub_level,
        f"coverage={coverage:.0%}, domains={domain_count}",
    )


def score_depth(
    bloom_scores: dict[str, float],
    highest_bloom_demonstrated: str = "",
) -> ACFDimensionScore:
    """Score Depth dimension (L1-L6) using Bloom's Taxonomy.

    bloom_scores: dict mapping level (L1-L6) to accuracy (0.0-1.0)
    """
    if not bloom_scores:
        return ACFDimensionScore("depth", 0.0, "L0", "No Bloom scores")

    # Find highest level with score > 0.5 (demonstrated competence)
    highest = "L0"
    for level in ["L6", "L5", "L4", "L3", "L2", "L1"]:
        if bloom_scores.get(level, 0.0) >= 0.5:
            highest = level
            break

    if highest_bloom_demonstrated:
        highest = highest_bloom_demonstrated

    base_score = BLOOM_DEPTH_MAP.get(highest, 0)
    highest_performance = bloom_scores.get(highest, 0.0)
    quality_bonus = highest_performance * 10

    score = min(base_score + quality_bonus, 100.0)

    return ACFDimensionScore(
        "depth", score, highest,
        f"highest={highest}, bloom_scores={bloom_scores}",
    )


def score_formal_reasoning(
    single_step_accuracy: float = 0.0,
    multi_step_accuracy: float = 0.0,
    proof_construction: float = 0.0,
) -> ACFDimensionScore:
    """Score Formal Reasoning (FR1-FR4).

    All inputs are 0.0-1.0 accuracy rates.
    """
    score = (single_step_accuracy * 30 + multi_step_accuracy * 40 +
             proof_construction * 30)

    if proof_construction >= 0.5:
        sub_level = "FR4"
    elif multi_step_accuracy >= 0.5:
        sub_level = "FR3"
    elif single_step_accuracy >= 0.5:
        sub_level = "FR2"
    elif single_step_accuracy > 0:
        sub_level = "FR1"
    else:
        sub_level = "FR0"

    return ACFDimensionScore(
        "formal_reasoning", min(score, 100.0), sub_level,
        f"single={single_step_accuracy:.0%}, multi={multi_step_accuracy:.0%}",
    )


def score_factual_grounding(
    provenance_rate: float,
    hallucination_rate: float,
) -> ACFDimensionScore:
    """Score Factual Grounding (FG1-FG4).

    provenance_rate: fraction of responses with source attribution (0-1)
    hallucination_rate: fraction of responses containing fabricated facts (0-1)
    """
    correctness = 1.0 - hallucination_rate
    score = (provenance_rate * 0.6 + correctness * 0.4) * 100

    if provenance_rate >= 0.99 and hallucination_rate == 0:
        sub_level = "FG4"
    elif provenance_rate >= 0.90 and hallucination_rate < 0.02:
        sub_level = "FG3"
    elif provenance_rate >= 0.50 and hallucination_rate < 0.10:
        sub_level = "FG2"
    elif provenance_rate > 0:
        sub_level = "FG1"
    else:
        sub_level = "FG0"

    return ACFDimensionScore(
        "factual_grounding", min(score, 100.0), sub_level,
        f"provenance={provenance_rate:.0%}, hallucination={hallucination_rate:.0%}",
    )


def score_compositional_generalization(
    known_composition_accuracy: float = 0.0,
    novel_combination_accuracy: float = 0.0,
    scan_cogs_accuracy: float = 0.0,
) -> ACFDimensionScore:
    """Score Compositional Generalization (CG1-CG3).

    All inputs are 0.0-1.0 accuracy rates.
    """
    score = (known_composition_accuracy * 30 + novel_combination_accuracy * 35 +
             scan_cogs_accuracy * 35)

    if scan_cogs_accuracy >= 0.5:
        sub_level = "CG3"
    elif novel_combination_accuracy >= 0.5:
        sub_level = "CG2"
    elif known_composition_accuracy > 0:
        sub_level = "CG1"
    else:
        sub_level = "CG0"

    return ACFDimensionScore(
        "compositional_generalization", min(score, 100.0), sub_level,
        f"known={known_composition_accuracy:.0%}, novel={novel_combination_accuracy:.0%}",
    )


def score_knowledge_transparency(
    inspectable: bool = False,
    queryable: bool = False,
    traceable_provenance_rate: float = 0.0,
) -> ACFDimensionScore:
    """Score Knowledge Transparency (KT1-KT3).

    inspectable: knowledge stored in human-readable format
    queryable: structured queries possible over knowledge
    traceable_provenance_rate: fraction of reasoning with full provenance chain (0-1)
    """
    score = 0.0
    if inspectable:
        score += 33
    if queryable:
        score += 33
    score += traceable_provenance_rate * 34

    if queryable and traceable_provenance_rate >= 0.8:
        sub_level = "KT3"
    elif queryable:
        sub_level = "KT2"
    elif inspectable:
        sub_level = "KT1"
    else:
        sub_level = "KT0"

    return ACFDimensionScore(
        "knowledge_transparency", min(score, 100.0), sub_level,
        f"inspect={inspectable}, query={queryable}, trace={traceable_provenance_rate:.0%}",
    )


def score_service_orientation(
    task_completion_rate: float = 0.0,
    explanation_quality: float = 0.0,
    user_trust_score: float = 0.0,
) -> ACFDimensionScore:
    """Score Service Orientation (SO1-SO4).

    All inputs are 0.0-1.0 rates/scores.
    """
    score = (task_completion_rate * 40 + explanation_quality * 30 +
             user_trust_score * 30)

    if task_completion_rate >= 0.9 and user_trust_score >= 0.8:
        sub_level = "SO4"
    elif task_completion_rate >= 0.7:
        sub_level = "SO3"
    elif task_completion_rate >= 0.4:
        sub_level = "SO2"
    elif task_completion_rate > 0:
        sub_level = "SO1"
    else:
        sub_level = "SO0"

    return ACFDimensionScore(
        "service_orientation", min(score, 100.0), sub_level,
        f"completion={task_completion_rate:.0%}, trust={user_trust_score:.0%}",
    )


def score_gba(
    gba1_calibration: float,
    gba2_ood_detection: float,
    gba3_graceful: float = 0.0,
    gba4_meta: float = 0.0,
) -> ACFDimensionScore:
    """Score Generalization Boundary Awareness (GBA1-GBA4).

    GBA1: Confidence calibration accuracy (0-1)
    GBA2: Out-of-domain detection rate (0-1)
    GBA3: Graceful degradation on boundary queries (0-1)
    GBA4: Meta-cognitive self-assessment accuracy (0-1)
    """
    weighted = (gba1_calibration * 0.3 + gba2_ood_detection * 0.4 +
                gba3_graceful * 0.2 + gba4_meta * 0.1)
    score = weighted * 100

    if weighted >= 0.90:
        sub_level = "GBA4"
    elif weighted >= 0.75:
        sub_level = "GBA3"
    elif weighted >= 0.50:
        sub_level = "GBA2"
    elif weighted > 0:
        sub_level = "GBA1"
    else:
        sub_level = "GBA0"

    return ACFDimensionScore(
        "gba", min(score, 100.0), sub_level,
        f"GBA1={gba1_calibration:.0%}, GBA2={gba2_ood_detection:.0%}",
    )


def score_autonomy(
    autonomy_rate: float,
    gap_detection_rate: float = 0.0,
    self_directed_learning: bool = False,
) -> ACFDimensionScore:
    """Score Autonomy dimension (AU1-AU4).

    autonomy_rate: fraction of tasks completed without human intervention (0-1)
    gap_detection_rate: fraction of knowledge gaps correctly identified (0-1)
    self_directed_learning: whether system initiates its own learning
    """
    score = autonomy_rate * 50 + gap_detection_rate * 30
    if self_directed_learning:
        score += 20

    if score >= 80:
        sub_level = "AU4"
    elif score >= 50 and gap_detection_rate > 0.5:
        sub_level = "AU3"
    elif gap_detection_rate > 0.3:
        sub_level = "AU2"
    elif autonomy_rate > 0:
        sub_level = "AU1"
    else:
        sub_level = "AU0"

    return ACFDimensionScore(
        "autonomy", min(score, 100.0), sub_level,
        f"autonomy={autonomy_rate:.0%}, gaps={gap_detection_rate:.0%}",
    )


class ACFScorer:
    """Aggregate scorer that builds ACFProfiles from dimension scores."""

    @staticmethod
    def create_profile(
        system_id: str,
        system_type: str,
        version: str,
        **dimension_scores: ACFDimensionScore,
    ) -> ACFProfile:
        """Create an ACF profile from individual dimension scores."""
        profile = ACFProfile(
            system_id=system_id,
            system_type=system_type,
            version=version,
        )
        for name, score in dimension_scores.items():
            profile.dimensions[name] = score
        return profile
