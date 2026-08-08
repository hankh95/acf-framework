"""The knowledge data and the README must agree — derived, not asserted.

This suite exists because they drifted twice without anything going red:
the README said "74 measures" while the data carried 75 measure declarations,
and the 75th was a duplicate id — two different measures both declared
``<#M-073>`` (Load/Unload Differential in knowledge-transfer-measures.md,
which the README endorses, and Regression Rollback Rate in
safety-containment-measures.md, added eight days later; issue #30).

A count stated in prose that nothing derives is a count that rots. Every
assertion here recomputes the number from ``knowledge/`` and compares it to
the README's own sentences, so adding a measure without touching the README
(or re-using a taken id) fails the suite instead of shipping.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "knowledge"
README = (REPO_ROOT / "README.md").read_text()

MEASURE_DECL = re.compile(r"<#(M-\d+)> a acf:Measure\b")
DIMENSION_DECL = re.compile(r"<#(\w+)> a acf:Dimension\b")
HYPOTHESIS_DECL = re.compile(r"<#(H122\.\d+)> a acf:Hypothesis\b")


def _declarations(pattern: re.Pattern, subdir: str) -> list[str]:
    ids: list[str] = []
    for path in sorted((KNOWLEDGE / subdir).glob("*.md")):
        ids.extend(pattern.findall(path.read_text()))
    return ids


def test_measure_ids_are_unique():
    """Two measures sharing an id poison every downstream reference to it."""
    ids = _declarations(MEASURE_DECL, "measures")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    assert not dupes, f"duplicate measure id(s) declared: {dupes}"


def test_measure_ids_are_dense_from_m001():
    """The id space is M-001..M-NNN with no gaps, so ranges in prose stay honest."""
    ids = sorted(_declarations(MEASURE_DECL, "measures"))
    expected = [f"M-{n:03d}" for n in range(1, len(ids) + 1)]
    assert ids == expected, (
        f"measure ids are not dense M-001..M-{len(ids):03d}: "
        f"missing {sorted(set(expected) - set(ids))}, "
        f"unexpected {sorted(set(ids) - set(expected))}"
    )


def test_readme_measure_count_matches_data():
    """Every README sentence that states the measure count states the real one."""
    count = len(set(_declarations(MEASURE_DECL, "measures")))
    claims = {
        "quick-start": re.search(r"List all (\d+) measures", README),
        "conformance bullet": re.search(r"All (\d+) measures", README),
        "section heading": re.search(r"## (\d+) Measures", README),
        "section lead": re.search(r"includes (\d+) measures across", README),
    }
    for where, match in claims.items():
        assert match, f"README no longer states a measure count at the {where}"
        assert int(match.group(1)) == count, (
            f"README {where} says {match.group(1)} measures; knowledge/ declares {count}"
        )


def test_every_measure_maps_to_a_dimension():
    """Canonical measures use acf:mapsTo, the proposed tranche acf:mapsToDimension —
    every declaration must carry one of the two."""
    total = 0
    unmapped: list[str] = []
    for path in sorted((KNOWLEDGE / "measures").glob("*.md")):
        text = path.read_text()
        declared = MEASURE_DECL.findall(text)
        total += len(declared)
        mapped = len(re.findall(r"acf:mapsTo\b", text)) + len(
            re.findall(r"acf:mapsToDimension\b", text)
        )
        if mapped < len(declared):
            unmapped.append(f"{path.name}: {len(declared)} declared, {mapped} mapped")
    assert not unmapped, f"measures without a dimension mapping: {unmapped}"
    assert total > 0


def test_readme_dimension_count_matches_data():
    count = len(set(_declarations(DIMENSION_DECL, "dimensions")))
    match = re.search(r"across (\d+) dimensions", README)
    assert match, "README no longer states the dimension count"
    assert int(match.group(1)) == count, (
        f"README says {match.group(1)} dimensions; knowledge/ declares {count}"
    )


def test_readme_hypothesis_count_matches_data():
    count = len(set(_declarations(HYPOTHESIS_DECL, "hypotheses")))
    match = re.search(r"## (\d+) Hypotheses", README)
    assert match, "README no longer states the hypothesis count"
    assert int(match.group(1)) == count, (
        f"README says {match.group(1)} hypotheses; knowledge/ declares {count}"
    )
