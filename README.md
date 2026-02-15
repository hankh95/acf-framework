# ACF Framework

A graph-based framework for measuring Artificial General Intelligence.

The AGI Certification Framework (ACF) provides a rigorous, multi-dimensional scoring system for evaluating AI system capabilities against human professional standards. All knowledge — dimensions, measures, hypotheses, collected data — lives in an RDF graph, queryable via SPARQL.

## Quick Start

```bash
pip install acf-framework

# Explore the framework
acf dimensions              # List all 9 ACF dimensions
acf measures                # List all 66 measures
acf levels                  # Show certification levels (ACF-1 through ACF-6)

# Evaluate your system
acf validate path/to/data/  # Validate data files against schemas
acf score path/to/data/     # Generate ACF profile with certification level

# Query the knowledge graph directly
acf query "SELECT ?id ?name WHERE { ?m acf:mapsTo <#Depth> ; acf:id ?id ; rdfs:label ?name . }"
```

## The Nine Dimensions

The ACF evaluates AI systems across 9 independent dimensions:

| Dimension | What it measures | Sub-levels |
|-----------|-----------------|------------|
| **Breadth** (B1-B4) | Range of domains where the system has knowledge | 4 |
| **Depth** (L1-L6) | Bloom's taxonomy cognitive levels achieved | 6 |
| **Formal Reasoning** (FR1-FR4) | Logical and mathematical reasoning capability | 4 |
| **Factual Grounding** (FG1-FG4) | Accuracy and evidence-based claims | 4 |
| **Compositional Generalization** (CG1-CG3) | Novel combination of known concepts | 3 |
| **Knowledge Transparency** (KT1-KT3) | Explainability and provenance of knowledge | 3 |
| **Service Orientation** (SO1-SO4) | Practical task completion capability | 4 |
| **Generalization Boundary Awareness** (GBA1-GBA4) | Knowing what you don't know | 4 |
| **Autonomy** (AU1-AU4) | Self-directed learning and operation | 4 |

## Certification Levels

| Level | Label | Human Equivalent | Score Range |
|-------|-------|-----------------|-------------|
| ACF-1 | Elementary | Elementary School | 0-16 |
| ACF-2 | Middle School | Middle School | 17-33 |
| ACF-3 | High School | High School Diploma | 34-50 |
| ACF-4 | Bachelor's | Bachelor's Degree | 51-67 |
| ACF-5 | Master's | Master's Degree | 68-84 |
| ACF-6 | PhD / Board | PhD or Board Certification | 85-100 |

## Graph-First Architecture

ACF uses [yurtle-rdflib](https://github.com/hankh95/yurtle-rdflib) to load all knowledge files into a live RDF graph at startup. This means:

- **All 66 measures** have `acf:mapsTo` triples linking them to ACF dimensions
- **All 14 hypotheses** are queryable with their targets and validation methodology
- **Collected data** (JSON files) is ingested as RDF triples for unified querying
- **Ad-hoc analysis** via SPARQL — no custom code needed for common queries

```sparql
# Which dimensions have fewer than 4 measures? (coverage gaps)
SELECT ?dim ?name (COUNT(?m) AS ?count) WHERE {
  ?dim a acf:Dimension ; rdfs:label ?name .
  OPTIONAL { ?m acf:mapsTo ?dim . }
} GROUP BY ?dim ?name HAVING (COUNT(?m) < 4)
```

## Data Collection

ACF defines three record types for collecting evaluation data:

| Record Type | Use Case | Schema |
|------------|----------|--------|
| **experiment-run** | Single measurement event | `schemas/experiment-run.schema.json` |
| **longitudinal-series** | Track a measure across versions | `schemas/longitudinal-series.schema.json` |
| **per-query-record** | Signal-level detail per query | `schemas/per-query-record.schema.json` |

```bash
# Print a blank template
acf template experiment-run

# Validate your data
acf validate my-data/experiment-results.json
```

## CLI Reference

```
acf dimensions [name]                  # List/show dimension details
acf measures [--dimension X]           # List measures, filter by dimension
acf levels                             # Show certification levels
acf validate <data-file|data-dir>      # Validate data against schemas
acf score <data-dir>                   # Score system → ACF profile
acf compare <profile1> <profile2>      # Compare two ACF profiles
acf template <record-type>             # Print blank data template
acf query "<sparql>"                   # Run SPARQL over knowledge + data
acf info                               # Show framework version and stats
```

## 66 Measures

The framework includes 66 measures across 11 categories:

- **Accuracy** (M-001–M-010): Routing, hallucination, provenance, calibration
- **Latency** (M-011–M-018): Processing paths, queries, end-to-end response
- **Efficiency** (M-019–M-021): Compute acceleration, call reduction
- **Quantity** (M-022–M-025): Knowledge graph growth, topic coverage
- **Quality** (M-026–M-029): Decision quality, task autonomy, error patterns
- **Metacognitive** (M-030–M-035): Self-assessment, automated decisions, reflection
- **Y-Layer Population** (M-036–M-043): Knowledge items per layer (Y0-Y6)
- **Y-Layer Growth** (M-044–M-046): Enrichment rate, confidence, diversity
- **Y-Layer Quality** (M-047–M-052): Fact correctness, inference coherence
- **Y-Layer Structural** (M-053–M-055): Provenance, connectivity
- **Proposed** (M-056–M-066): Domain count, Bloom profile, task completion

## 14 Hypotheses

The framework includes 14 testable hypotheses about AGI measurement:

- **H122.1**: Breadth-Depth Independence (r < 0.3)
- **H122.2**: Human Certification Equivalence (ACF-3+)
- **H122.3**: Service Orientation Correlation (r > 0.7)
- **H122.4**: Provenance Requirement (>=95% accuracy)
- **H122.5**: LLM Depth Ceiling (<60% on L5-L6)
- **H122.6**: Understanding Efficiency (UER >=10x)
- **H122.7**: Compositional Generalization Gap
- **H122.8**: Knowledge Transparency Enables Verification
- **H122.9**: GBA Distinguishes Expert Systems
- **H122.10**: Paradigm Selection Capability
- **H122.11**: Symbolic-to-Motor Transfer
- **H122.12**: Autonomous Gap Detection (70%+)
- **H122.13**: Crystallization Efficiency (99%+)
- **H122.14**: Self-Directed Learning

## Installation

### From source (development)

```bash
git clone https://github.com/hankh95/acf-framework.git
cd acf-framework
pip install -e ".[dev]"
```

### Dependencies

- **Core**: `yurtle-rdflib`, `click`, `rich`
- **Development**: `pytest`, `ruff`, `mypy`
- **Optional** `[search]`: `nusy-nano` (semantic search via txtai)

## License

MIT — see [LICENSE](LICENSE).

## Citation

If you use the ACF framework in your research, please cite:

```bibtex
@software{acf-framework,
  title = {ACF Framework: A Graph-Based Framework for Measuring AGI},
  author = {Conguent Systems PBC},
  year = {2026},
  url = {https://github.com/hankh95/acf-framework},
  license = {MIT}
}
```
