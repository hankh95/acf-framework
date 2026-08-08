"""Referential integrity of the shipped knowledge graph.

These are the checks that were missing when three defects shipped together in 1.1.0:

  * 14 of 75 measures used ``acf:mapsToDimension`` -- a predicate defined nowhere in
    the ontology -- so they were invisible to every dimension-scoped query while still
    being counted in the headline "75 measures";
  * as a consequence one of the twelve dimensions (ActionCapability) had zero measures,
    i.e. the framework advertised a dimension nothing could score;
  * two measures pointed at ``<#GeneralizationBoundaryAwareness>``, which is not a
    dimension at all -- the real one is ``<#GeneralizationBoundary>``.

None of that broke a test, a lint, or the build, because every existing test asserts on
Python behaviour and nothing asserted on the DATA. A graph-based framework whose data is
its product needs its data under test.

The assertions are phrased POSITIVELY (every target resolves; every dimension is
covered) rather than as negative greps for the specific bad strings, so they keep
working when the next defect is spelled differently.
"""

from __future__ import annotations

import pytest

from acf.graph import ACFGraph


@pytest.fixture(scope="module")
def graph() -> ACFGraph:
    return ACFGraph()


def _mapped_dimension_uris(g: ACFGraph) -> set[str]:
    rows = g._select(
        "SELECT DISTINCT ?dim WHERE { ?m a acf:Measure ; acf:mapsTo ?dim }"
    )
    return {str(r.dim) for r in rows}


def _dimension_uris(g: ACFGraph) -> set[str]:
    rows = g._select("SELECT ?d WHERE { ?d a acf:Dimension }")
    return {str(r.d) for r in rows}


def test_every_measure_maps_to_a_real_dimension(graph: ACFGraph) -> None:
    """No measure points at a dimension that does not exist.

    A dangling target is silent: the measure still lists, still counts, and simply
    never appears under any dimension.
    """
    orphans = _mapped_dimension_uris(graph) - _dimension_uris(graph)
    assert not orphans, (
        f"measure(s) map to non-existent dimension(s): {sorted(orphans)}. "
        "Check the spelling against knowledge/dimensions/."
    )


def test_every_dimension_has_at_least_one_measure(graph: ACFGraph) -> None:
    """A dimension nothing maps to cannot be scored, and advertising it is a false claim."""
    uncovered = _dimension_uris(graph) - _mapped_dimension_uris(graph)
    assert not uncovered, (
        f"dimension(s) with no measures mapped to them: {sorted(uncovered)}. "
        "Either map measures to them or stop listing them as dimensions."
    )


def test_no_measure_uses_an_undefined_mapping_predicate(graph: ACFGraph) -> None:
    """Catches the specific failure that made 14 measures invisible.

    ``acf:mapsToDimension`` parses fine as RDF -- any predicate does -- so the graph
    loads clean and the measures simply never join to a dimension. The only way to
    notice is to ask whether every measure participates in the mapping at all.
    """
    total = graph._select("SELECT ?m WHERE { ?m a acf:Measure }")
    mapped = graph._select("SELECT DISTINCT ?m WHERE { ?m a acf:Measure ; acf:mapsTo ?dim }")
    unmapped = len(total) - len(mapped)
    assert unmapped == 0, (
        f"{unmapped} of {len(total)} measures participate in no acf:mapsTo edge. "
        "A measure mapped with a different predicate loads silently and joins to nothing."
    )


def test_counts_are_self_consistent(graph: ACFGraph) -> None:
    """The numbers the framework reports about itself must come from the graph.

    Guards the class of defect where a README or a post quotes a count nobody re-derives:
    if these move, every published figure needs re-checking rather than the test being
    updated to match.
    """
    dims = len(_dimension_uris(graph))
    measures = len(graph._select("SELECT ?m WHERE { ?m a acf:Measure }"))
    hypotheses = len(graph._select("SELECT ?h WHERE { ?h a acf:Hypothesis }"))

    assert dims == 12, f"dimension count moved to {dims}; update the README and any published figure"
    assert measures == 75, f"measure count moved to {measures}; update the README and any published figure"
    assert hypotheses == 16, (
        f"hypothesis count moved to {hypotheses}. Note 16 is the count of DISTINCT "
        "acf:Hypothesis subjects; a plain grep for the type string returns 17 because a "
        "SPARQL example in the same file mentions it."
    )
