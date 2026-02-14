"""
ACFGraph: Central knowledge graph for the ACF framework.

Loads all knowledge files (dimensions, levels, measures, hypotheses, config)
into a unified RDF graph via yurtle-rdflib. Optionally ingests JSON data files
as triples for unified SPARQL querying.

Usage:
    from acf.graph import ACFGraph

    graph = ACFGraph()  # Loads bundled knowledge/
    graph = ACFGraph(data_dir=Path("my-evaluation/data"))  # + data
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

import yurtle_rdflib

# ACF namespace for all framework-specific predicates
ACF = Namespace("https://acf-framework.dev/ns/")

# Default knowledge directory (bundled with package)
_PACKAGE_ROOT = Path(__file__).parent.parent.parent
KNOWLEDGE_DIR = _PACKAGE_ROOT / "knowledge"


@dataclass
class Dimension:
    """An ACF dimension (e.g., Breadth, Depth)."""

    id: str
    label: str
    short_name: str
    sub_level_count: int
    weight: float
    description: str = ""


@dataclass
class SubLevel:
    """A sub-level within a dimension (e.g., L1 Remember)."""

    id: str
    dimension_id: str
    level: int
    label: str
    score_range: str = ""
    description: str = ""


@dataclass
class Measure:
    """An ACF measure definition."""

    id: str
    name: str
    unit: str
    collection: str = "automated"
    dimensions: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class CertificationLevel:
    """An ACF certification level (ACF-1 through ACF-6)."""

    id: str
    label: str
    score_min: float
    score_max: float
    human_equivalent: str = ""


@dataclass
class Hypothesis:
    """A testable hypothesis."""

    id: str
    description: str
    target: str = ""
    measures: list[str] = field(default_factory=list)
    status: str = "pending"


@dataclass
class DataPoint:
    """A data point from ingested JSON."""

    measure_id: str
    value: float
    system_id: str = ""
    system_version: str = ""
    experiment_id: str = ""
    timestamp: str = ""


class ACFGraph:
    """Central knowledge graph for the ACF framework.

    Loads all knowledge/ Yurtle files into an RDF graph via yurtle-rdflib,
    then provides typed Python accessors backed by SPARQL queries.
    """

    def __init__(
        self,
        knowledge_dir: Path | None = None,
        data_dir: Path | None = None,
    ):
        self._knowledge_dir = knowledge_dir or KNOWLEDGE_DIR

        # Load all Yurtle knowledge files into the graph
        if self._knowledge_dir.exists():
            self.graph: Graph = yurtle_rdflib.load_workspace(str(self._knowledge_dir))
        else:
            self.graph = Graph()

        # Bind ACF namespace for SPARQL queries
        self.graph.bind("acf", ACF)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)

        # Ingest JSON data files if provided
        if data_dir and data_dir.exists():
            self._ingest_data(data_dir)

    def _ingest_data(self, data_dir: Path) -> int:
        """Convert JSON data files into RDF triples and add to graph.

        Returns number of records ingested.
        """
        count = 0
        for json_file in sorted(data_dir.glob("*.json")):
            try:
                record = json.loads(json_file.read_text())
                self._ingest_record(record, json_file.stem)
                count += 1
            except (json.JSONDecodeError, KeyError):
                continue
        return count

    def _ingest_record(self, record: dict[str, Any], record_id: str) -> None:
        """Convert a single JSON record to RDF triples."""
        subject = ACF[f"data/{record_id}"]
        self.graph.add((subject, RDF.type, ACF.DataRecord))

        record_type = record.get("record_type", "unknown")
        self.graph.add((subject, ACF.recordType, Literal(record_type)))

        # Common envelope fields
        for field_name in [
            "measure_id", "system_id", "system_version",
            "experiment_id", "timestamp", "collector", "notes",
        ]:
            # Support both NuSy field names and ACF field names
            value = record.get(field_name) or record.get(
                {"system_id": "being", "experiment_id": "expedition"}.get(field_name, ""),
            )
            if value:
                self.graph.add((subject, ACF[field_name], Literal(str(value))))

        # Link to measure node
        measure_id = record.get("measure_id", "")
        if measure_id:
            self.graph.add((subject, ACF.measure, ACF[measure_id]))

        # Record-type-specific fields
        if record_type == "experiment-run":
            for field_name in ["value", "target", "n", "comparison"]:
                if field_name in record:
                    if isinstance(record[field_name], (int, float)):
                        self.graph.add((
                            subject, ACF[field_name],
                            Literal(record[field_name], datatype=XSD.double),
                        ))
                    else:
                        self.graph.add((
                            subject, ACF[field_name],
                            Literal(str(record[field_name])),
                        ))
            if "pass" in record:
                self.graph.add((
                    subject, ACF.passed,
                    Literal(record["pass"], datatype=XSD.boolean),
                ))

        elif record_type == "longitudinal-series":
            for i, dp in enumerate(record.get("data_points", [])):
                dp_node = ACF[f"data/{record_id}/dp{i}"]
                self.graph.add((subject, ACF.dataPoint, dp_node))
                self.graph.add((dp_node, RDF.type, ACF.DataPoint))
                for k, v in dp.items():
                    if isinstance(v, (int, float)):
                        self.graph.add((
                            dp_node, ACF[k],
                            Literal(v, datatype=XSD.double),
                        ))
                    else:
                        self.graph.add((dp_node, ACF[k], Literal(str(v))))

    # ── Typed Accessors (SPARQL-backed) ──────────────────────────

    def dimensions(self) -> list[Dimension]:
        """Return all ACF dimensions."""
        results = self.graph.query("""
            SELECT ?id ?label ?shortName ?subLevelCount ?weight ?desc WHERE {
                ?s a acf:Dimension .
                ?s acf:id ?id .
                OPTIONAL { ?s acf:label ?label }
                OPTIONAL { ?s acf:shortName ?shortName }
                OPTIONAL { ?s acf:subLevelCount ?subLevelCount }
                OPTIONAL { ?s acf:weight ?weight }
                OPTIONAL { ?s acf:description ?desc }
            }
            ORDER BY ?id
        """)
        return [
            Dimension(
                id=str(row.id),
                label=str(row.label or row.id),
                short_name=str(row.shortName or ""),
                sub_level_count=int(row.subLevelCount) if row.subLevelCount else 0,
                weight=float(row.weight) if row.weight else 0.0,
                description=str(row.desc or ""),
            )
            for row in results
        ]

    def dimension(self, name: str) -> Dimension | None:
        """Return a single dimension by ID."""
        for d in self.dimensions():
            if d.id == name:
                return d
        return None

    def sub_levels(self, dimension_id: str | None = None) -> list[SubLevel]:
        """Return sub-levels, optionally filtered by dimension."""
        filter_clause = ""
        if dimension_id:
            filter_clause = f'FILTER(STR(?dimId) = "{dimension_id}")'

        results = self.graph.query(f"""
            SELECT ?id ?dimId ?level ?label ?scoreRange ?desc WHERE {{
                ?s a acf:SubLevel .
                ?s acf:id ?id .
                ?s acf:dimension ?dim .
                ?dim acf:id ?dimId .
                OPTIONAL {{ ?s acf:level ?level }}
                OPTIONAL {{ ?s acf:label ?label }}
                OPTIONAL {{ ?s acf:scoreRange ?scoreRange }}
                OPTIONAL {{ ?s acf:description ?desc }}
                {filter_clause}
            }}
            ORDER BY ?dimId ?level
        """)
        return [
            SubLevel(
                id=str(row.id),
                dimension_id=str(row.dimId),
                level=int(row.level) if row.level else 0,
                label=str(row.label or ""),
                score_range=str(row.scoreRange or ""),
                description=str(row.desc or ""),
            )
            for row in results
        ]

    def measures(self, dimension: str | None = None) -> list[Measure]:
        """Return measures, optionally filtered by ACF dimension."""
        filter_clause = ""
        if dimension:
            filter_clause = f'FILTER(STR(?dimId) = "{dimension}")'

        results = self.graph.query(f"""
            SELECT ?id ?name ?unit ?collection ?desc WHERE {{
                ?s a acf:Measure .
                ?s acf:id ?id .
                OPTIONAL {{ ?s acf:name ?name }}
                OPTIONAL {{ ?s acf:unit ?unit }}
                OPTIONAL {{ ?s acf:collection ?collection }}
                OPTIONAL {{ ?s acf:description ?desc }}
                OPTIONAL {{
                    ?s acf:mapsTo ?dim .
                    ?dim acf:id ?dimId .
                }}
                {filter_clause}
            }}
            ORDER BY ?id
        """)

        # Build measures with dimension mappings
        measures_dict: dict[str, Measure] = {}
        for row in results:
            mid = str(row.id)
            if mid not in measures_dict:
                measures_dict[mid] = Measure(
                    id=mid,
                    name=str(row.name or mid),
                    unit=str(row.unit or ""),
                    collection=str(row.collection or "automated"),
                    description=str(row.desc or ""),
                )

        # Fetch dimension mappings for all measures
        dim_results = self.graph.query("""
            SELECT ?measId ?dimId WHERE {
                ?s a acf:Measure .
                ?s acf:id ?measId .
                ?s acf:mapsTo ?dim .
                ?dim acf:id ?dimId .
            }
        """)
        for row in dim_results:
            mid = str(row.measId)
            if mid in measures_dict:
                measures_dict[mid].dimensions.append(str(row.dimId))

        return list(measures_dict.values())

    def measure(self, measure_id: str) -> Measure | None:
        """Return a single measure by ID."""
        for m in self.measures():
            if m.id == measure_id:
                return m
        return None

    def levels(self) -> list[CertificationLevel]:
        """Return all certification levels."""
        results = self.graph.query("""
            SELECT ?id ?label ?scoreMin ?scoreMax ?humanEquiv WHERE {
                ?s a acf:CertificationLevel .
                ?s acf:id ?id .
                OPTIONAL { ?s acf:label ?label }
                OPTIONAL { ?s acf:scoreMin ?scoreMin }
                OPTIONAL { ?s acf:scoreMax ?scoreMax }
                OPTIONAL { ?s acf:humanEquivalent ?humanEquiv }
            }
            ORDER BY ?scoreMin
        """)
        return [
            CertificationLevel(
                id=str(row.id),
                label=str(row.label or row.id),
                score_min=float(row.scoreMin) if row.scoreMin else 0.0,
                score_max=float(row.scoreMax) if row.scoreMax else 100.0,
                human_equivalent=str(row.humanEquiv or ""),
            )
            for row in results
        ]

    def hypotheses(self) -> list[Hypothesis]:
        """Return all hypotheses."""
        results = self.graph.query("""
            SELECT ?id ?desc ?target ?status WHERE {
                ?s a acf:Hypothesis .
                ?s acf:id ?id .
                OPTIONAL { ?s acf:description ?desc }
                OPTIONAL { ?s acf:target ?target }
                OPTIONAL { ?s acf:status ?status }
            }
            ORDER BY ?id
        """)
        return [
            Hypothesis(
                id=str(row.id),
                description=str(row.desc or ""),
                target=str(row.target or ""),
                status=str(row.status or "pending"),
            )
            for row in results
        ]

    def data_series(self, measure_id: str) -> list[DataPoint]:
        """Return all data points for a given measure."""
        results = self.graph.query(f"""
            SELECT ?value ?sysId ?sysVer ?expId ?ts WHERE {{
                ?s acf:measure acf:{measure_id} .
                OPTIONAL {{ ?s acf:value ?value }}
                OPTIONAL {{ ?s acf:system_id ?sysId }}
                OPTIONAL {{ ?s acf:system_version ?sysVer }}
                OPTIONAL {{ ?s acf:experiment_id ?expId }}
                OPTIONAL {{ ?s acf:timestamp ?ts }}
            }}
            ORDER BY ?ts
        """)
        return [
            DataPoint(
                measure_id=measure_id,
                value=float(row.value) if row.value else 0.0,
                system_id=str(row.sysId or ""),
                system_version=str(row.sysVer or ""),
                experiment_id=str(row.expId or ""),
                timestamp=str(row.ts or ""),
            )
            for row in results
        ]

    def query(self, sparql: str) -> list[dict[str, Any]]:
        """Run an arbitrary SPARQL query and return results as dicts."""
        results = self.graph.query(sparql)
        return [
            {str(var): str(row[var]) for var in results.vars if row[var] is not None}
            for row in results
        ]

    def triple_count(self) -> int:
        """Return total number of triples in the graph."""
        return len(self.graph)
