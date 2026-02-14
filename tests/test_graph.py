"""Tests for ACFGraph — the central knowledge graph engine."""

from pathlib import Path

import pytest

from acf.graph import ACFGraph, KNOWLEDGE_DIR


@pytest.fixture
def graph():
    """Create an ACFGraph from the bundled knowledge files."""
    return ACFGraph()


@pytest.fixture
def graph_with_data(tmp_path):
    """Create an ACFGraph with example data loaded."""
    import json
    import shutil

    # Copy example data to tmp
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    examples_dir = Path(__file__).parent.parent / "examples" / "data"
    for f in examples_dir.glob("*.json"):
        shutil.copy(f, data_dir / f.name)

    return ACFGraph(data_dir=data_dir)


class TestGraphLoading:
    """Test knowledge graph loading."""

    def test_knowledge_dir_exists(self):
        assert KNOWLEDGE_DIR.exists()
        assert (KNOWLEDGE_DIR / "dimensions").exists()
        assert (KNOWLEDGE_DIR / "levels").exists()
        assert (KNOWLEDGE_DIR / "measures").exists()

    def test_graph_loads(self, graph):
        assert graph.triple_count() > 0

    def test_graph_has_significant_triples(self, graph):
        # 9 dimensions + 6 levels + 66 measures + 14 hypotheses + sub-levels
        assert graph.triple_count() > 500


class TestDimensions:
    """Test dimension loading and querying."""

    def test_nine_dimensions(self, graph):
        dims = graph.dimensions()
        assert len(dims) == 9

    def test_dimension_ids(self, graph):
        dims = graph.dimensions()
        ids = {d.id for d in dims}
        expected = {
            "breadth", "depth", "formal-reasoning", "factual-grounding",
            "compositional-generalization", "knowledge-transparency",
            "service-orientation", "generalization-boundary", "autonomy",
        }
        assert ids == expected

    def test_dimension_has_weight(self, graph):
        dims = graph.dimensions()
        for d in dims:
            assert d.weight > 0, f"Dimension {d.id} has no weight"

    def test_dimension_has_sub_levels(self, graph):
        dims = graph.dimensions()
        for d in dims:
            assert d.sub_level_count > 0, f"Dimension {d.id} has no sub-levels"

    def test_get_single_dimension(self, graph):
        d = graph.dimension("depth")
        assert d is not None
        assert d.label == "Depth"

    def test_get_missing_dimension(self, graph):
        assert graph.dimension("nonexistent") is None


class TestMeasures:
    """Test measure loading and querying."""

    def test_sixty_six_measures(self, graph):
        ms = graph.measures()
        assert len(ms) == 66

    def test_measures_have_ids(self, graph):
        ms = graph.measures()
        ids = {m.id for m in ms}
        # Check a sample from each category
        assert "M-001" in ids
        assert "M-003" in ids  # Hallucination Rate
        assert "M-036" in ids  # Y-layer population
        assert "M-058" in ids  # Bloom Level Profile (proposed)
        assert "M-066" in ids  # Self-Correction Rate (last)

    def test_measures_have_dimension_mappings(self, graph):
        ms = graph.measures()
        with_dims = [m for m in ms if m.dimensions]
        # Most measures should have dimension mappings
        assert len(with_dims) > 50

    def test_filter_by_dimension(self, graph):
        depth_measures = graph.measures(dimension="depth")
        assert len(depth_measures) > 0
        # M-058 (Bloom Level Profile) should map to depth
        ids = {m.id for m in depth_measures}
        assert "M-058" in ids or "M-048" in ids  # At least one depth measure

    def test_get_single_measure(self, graph):
        m = graph.measure("M-003")
        assert m is not None
        assert "hallucination" in m.name.lower() or "hallucination" in m.description.lower()


class TestLevels:
    """Test certification level loading."""

    def test_six_levels(self, graph):
        lvls = graph.levels()
        assert len(lvls) == 6

    def test_level_ordering(self, graph):
        lvls = graph.levels()
        for i in range(len(lvls) - 1):
            assert lvls[i].score_min <= lvls[i + 1].score_min

    def test_level_labels(self, graph):
        lvls = graph.levels()
        labels = {l.label for l in lvls}
        assert "Elementary" in labels
        assert "PhD / Board Certified" in labels


class TestHypotheses:
    """Test hypothesis loading."""

    def test_fourteen_hypotheses(self, graph):
        hyps = graph.hypotheses()
        assert len(hyps) == 14

    def test_hypothesis_ids(self, graph):
        hyps = graph.hypotheses()
        ids = {h.id for h in hyps}
        assert "H122.1" in ids
        assert "H122.14" in ids

    def test_hypothesis_has_description(self, graph):
        hyps = graph.hypotheses()
        for h in hyps:
            assert h.description, f"Hypothesis {h.id} has no description"


class TestSPARQL:
    """Test SPARQL query capabilities."""

    def test_ad_hoc_query(self, graph):
        results = graph.query("""
            SELECT ?id WHERE {
                ?s a acf:Dimension ; acf:id ?id .
            }
        """)
        assert len(results) == 9

    def test_query_with_filter(self, graph):
        results = graph.query("""
            SELECT ?id ?name WHERE {
                ?m a acf:Measure ; acf:id ?id ; rdfs:label ?name .
                FILTER(STRSTARTS(?id, "M-05"))
            }
        """)
        assert len(results) > 0

    def test_empty_query(self, graph):
        results = graph.query("""
            SELECT ?x WHERE {
                ?x a <http://example.org/NonExistent> .
            }
        """)
        assert len(results) == 0


class TestDataIngestion:
    """Test JSON data ingestion."""

    def test_data_loaded(self, graph_with_data):
        assert graph_with_data.triple_count() > 0

    def test_empty_data_dir(self, tmp_path):
        data_dir = tmp_path / "empty"
        data_dir.mkdir()
        g = ACFGraph(data_dir=data_dir)
        # Should still have knowledge triples
        assert g.triple_count() > 0
