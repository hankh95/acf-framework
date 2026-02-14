"""SPARQL-backed measure registry."""

from __future__ import annotations

from acf.graph import ACFGraph, Measure


class MeasureRegistry:
    """Access ACF measures via the knowledge graph."""

    def __init__(self, graph: ACFGraph):
        self.graph = graph

    def all(self) -> list[Measure]:
        """Return all measures."""
        return self.graph.measures()

    def for_dimension(self, dimension: str) -> list[Measure]:
        """Return measures mapped to a specific ACF dimension."""
        return self.graph.measures(dimension=dimension)

    def get(self, measure_id: str) -> Measure | None:
        """Get a single measure by ID."""
        return self.graph.measure(measure_id)

    def coverage_matrix(self) -> dict[str, list[str]]:
        """Return dimension -> [measure_ids] mapping."""
        matrix: dict[str, list[str]] = {}
        for m in self.all():
            for dim in m.dimensions:
                matrix.setdefault(dim, []).append(m.id)
        return matrix
