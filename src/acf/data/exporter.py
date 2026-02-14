"""Export ACF profiles and data to various formats."""

from __future__ import annotations

import json
from typing import Any

from acf.scoring.profile import ACFProfile


def to_json(profile: ACFProfile, indent: int = 2) -> str:
    """Export profile as JSON."""
    return json.dumps(profile.to_dict(), indent=indent)


def to_markdown(profile: ACFProfile) -> str:
    """Export profile as markdown table."""
    lines = [
        f"# ACF Profile: {profile.system_id}",
        "",
        f"**System Type:** {profile.system_type}",
        f"**Version:** {profile.version}",
        f"**Aggregate Score:** {profile.aggregate_score:.1f}",
        f"**Certification Level:** {profile.certification_level} ({profile.certification_label})",
        "",
        "## Dimension Scores",
        "",
        "| Dimension | Score | Level | Confidence |",
        "|-----------|------:|-------|------------|",
    ]

    for name, dim in sorted(profile.dimensions.items()):
        lines.append(
            f"| {name} | {dim.score:.1f} | {dim.sub_level} | {dim.confidence} |"
        )

    return "\n".join(lines)


def to_csv(profile: ACFProfile) -> str:
    """Export profile as CSV."""
    lines = ["dimension,score,sub_level,confidence,evidence"]
    for name, dim in sorted(profile.dimensions.items()):
        evidence = dim.evidence.replace('"', '""')
        lines.append(
            f'{name},{dim.score:.1f},{dim.sub_level},{dim.confidence},"{evidence}"'
        )
    return "\n".join(lines)


def to_latex(profile: ACFProfile) -> str:
    """Export profile as LaTeX table."""
    lines = [
        r"\begin{table}[h]",
        r"\centering",
        f"\\caption{{ACF Profile: {profile.system_id} "
        f"({profile.certification_level})}}",
        r"\begin{tabular}{lrll}",
        r"\toprule",
        r"Dimension & Score & Level & Confidence \\",
        r"\midrule",
    ]

    for name, dim in sorted(profile.dimensions.items()):
        dim_label = name.replace("_", " ").title()
        lines.append(
            f"  {dim_label} & {dim.score:.1f} & {dim.sub_level} "
            f"& {dim.confidence} \\\\"
        )

    lines.extend([
        r"\midrule",
        f"  \\textbf{{Aggregate}} & \\textbf{{{profile.aggregate_score:.1f}}} "
        f"& \\textbf{{{profile.certification_level}}} & \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])

    return "\n".join(lines)


def comparison_markdown(p1: ACFProfile, p2: ACFProfile) -> str:
    """Generate markdown comparison of two profiles."""
    lines = [
        f"# ACF Comparison: {p1.system_id} vs {p2.system_id}",
        "",
        f"| Dimension | {p1.system_id} | {p2.system_id} | Delta |",
        "|-----------|------:|------:|------:|",
    ]

    all_dims = sorted(set(list(p1.dimensions.keys()) + list(p2.dimensions.keys())))
    for dim in all_dims:
        s1 = p1.dimensions.get(dim)
        s2 = p2.dimensions.get(dim)
        v1 = f"{s1.score:.1f}" if s1 else "-"
        v2 = f"{s2.score:.1f}" if s2 else "-"
        delta = f"{s2.score - s1.score:+.1f}" if s1 and s2 else "-"
        lines.append(f"| {dim} | {v1} | {v2} | {delta} |")

    lines.append(f"| **Aggregate** | **{p1.aggregate_score:.1f}** "
                 f"| **{p2.aggregate_score:.1f}** "
                 f"| **{p2.aggregate_score - p1.aggregate_score:+.1f}** |")

    return "\n".join(lines)
