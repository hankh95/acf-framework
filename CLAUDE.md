# ACF Framework — Claude Code Instructions

## Project Overview

ACF (AGI Certification Framework) is a graph-based framework for measuring AI system capabilities against human professional standards. It evaluates systems across 9 dimensions and 6 certification levels (ACF-1 Elementary through ACF-6 PhD/Board).

## Architecture

**Graph-first**: All knowledge lives in RDF via [yurtle-rdflib](https://github.com/hankh95/yurtle-rdflib). The `ACFGraph` class loads `knowledge/` Yurtle files at startup into a unified graph queryable via SPARQL.

**Key files:**
- `src/acf/graph.py` — Central graph engine (`ACFGraph`)
- `src/acf/cli.py` — Click CLI (`acf` entry point)
- `src/acf/scoring/scorer.py` — 9 dimension scoring functions
- `src/acf/scoring/profile.py` — `ACFProfile`, `ACFDimensionScore`
- `knowledge/` — Yurtle knowledge files (THE specification)
- `schemas/` — JSON Schema for data validation

## Conventions

- **Yurtle format**: Markdown with TTL frontmatter for all knowledge
- **ACF namespace**: `https://acf-framework.dev/ns/`
- **Measures**: M-001 through M-066, each with `acf:mapsTo` dimension triples
- **Hypotheses**: H122.1 through H122.14
- **Data records**: experiment-run, longitudinal-series, per-query-record

## Development

```bash
pip install -e ".[dev]"  # Install with dev dependencies
pytest                    # Run tests
acf info                  # Verify installation
```

## Testing

Run `pytest` before committing. Tests cover:
- Graph loading from knowledge files
- SPARQL queries
- Scoring engine
- Data validation
- CLI commands
