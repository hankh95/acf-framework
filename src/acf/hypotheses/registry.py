"""SPARQL-backed hypothesis registry."""

from __future__ import annotations

from acf.graph import ACFGraph, Hypothesis


class HypothesisRegistry:
    """Access ACF hypotheses via the knowledge graph."""

    def __init__(self, graph: ACFGraph):
        self.graph = graph

    def all(self) -> list[Hypothesis]:
        """Return all hypotheses."""
        return self.graph.hypotheses()

    def get(self, hypothesis_id: str) -> Hypothesis | None:
        """Get a single hypothesis by ID."""
        for h in self.all():
            if h.id == hypothesis_id:
                return h
        return None
