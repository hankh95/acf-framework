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

## Development Practices

### Branch + PR Pattern (Required)

All implementation work goes through feature branches and pull requests:

1. Create a feature branch: `git checkout -b feat-short-description`
2. Do all implementation work on the branch — **never push directly to main**
3. Run tests: `pytest`
4. Push and create PR: `gh pr create`
5. Get review from another developer/agent before merging

After merge, clean up:
```bash
git branch -d feat-short-description
git push origin --delete feat-short-description
```

### Testing

Run `pytest` before committing. Tests must pass before creating a PR. Tests cover:
- Graph loading from knowledge files
- SPARQL queries
- Scoring engine
- Data validation
- CLI commands

### Code Quality

- Always use type hints
- Prefer editing existing files over creating new ones
- Don't create files unless necessary
- Knowledge belongs in Yurtle files (`knowledge/`), not Python code

## Multi-Agent Coordination

| Agent | GitHub | Platform |
|-------|--------|----------|
| **M5** | hankh95 | MacBook Pro M5 |
| **DGX** | hankh959 | DGX Spark |
| **Mini** | hankh1844 | Mac Mini M4 |

## Related Projects

- **nusy-product-team** — Uses ACF for being certification
- **yurtle-rdflib** — RDF parsing library
- **research** — Paper 122 (AGI Certification Framework)
