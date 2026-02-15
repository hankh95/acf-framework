"""
ACF CLI: Command-line interface for the AGI Certification Framework.

Usage:
    acf dimensions          List all 9 ACF dimensions
    acf measures             List all measures with dimension mappings
    acf levels               Show certification levels
    acf score <data-dir>     Score a system from collected data
    acf validate <path>      Validate data files against schemas
    acf query "<sparql>"     Run SPARQL over the knowledge graph
    acf compare <p1> <p2>    Compare two ACF profiles
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from acf.graph import ACFGraph, KNOWLEDGE_DIR

console = Console()


def _get_graph(data_dir: str | None = None) -> ACFGraph:
    """Create an ACFGraph, optionally with data."""
    d = Path(data_dir) if data_dir else None
    return ACFGraph(knowledge_dir=KNOWLEDGE_DIR, data_dir=d)


@click.group()
@click.version_option(package_name="acf-framework")
def main():
    """ACF: Graph-based AGI Certification Framework."""
    pass


@main.command()
@click.argument("name", required=False)
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def dimensions(name: str | None, as_json: bool):
    """List ACF dimensions or show detail for one."""
    graph = _get_graph()
    dims = graph.dimensions()

    if not dims:
        console.print("[yellow]No dimensions found in knowledge graph.[/yellow]")
        console.print(f"Knowledge dir: {KNOWLEDGE_DIR}")
        return

    if name:
        dim = next((d for d in dims if d.id == name), None)
        if not dim:
            console.print(f"[red]Dimension '{name}' not found.[/red]")
            console.print(f"Available: {', '.join(d.id for d in dims)}")
            return
        if as_json:
            click.echo(json.dumps(dim.__dict__, indent=2))
        else:
            console.print(f"[bold]{dim.label}[/bold] ({dim.short_name})")
            console.print(f"  Weight: {dim.weight:.3f}")
            console.print(f"  Sub-levels: {dim.sub_level_count}")
            if dim.description:
                console.print(f"  {dim.description}")
            # Show sub-levels
            subs = graph.sub_levels(dim.id)
            if subs:
                table = Table(title="Sub-Levels")
                table.add_column("ID", style="cyan")
                table.add_column("Label")
                table.add_column("Score Range")
                for s in subs:
                    table.add_row(s.id, s.label, s.score_range)
                console.print(table)
        return

    if as_json:
        click.echo(json.dumps([d.__dict__ for d in dims], indent=2))
        return

    table = Table(title="ACF Dimensions")
    table.add_column("#", style="dim")
    table.add_column("ID", style="cyan")
    table.add_column("Label", style="bold")
    table.add_column("Short", style="dim")
    table.add_column("Sub-levels", justify="right")
    table.add_column("Weight", justify="right")

    for i, d in enumerate(dims, 1):
        table.add_row(
            str(i), d.id, d.label, d.short_name,
            str(d.sub_level_count), f"{d.weight:.3f}",
        )
    console.print(table)


@main.command()
@click.option("--dimension", "-d", help="Filter by ACF dimension ID")
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def measures(dimension: str | None, as_json: bool):
    """List all measures with ACF dimension mappings."""
    graph = _get_graph()
    ms = graph.measures(dimension=dimension)

    if not ms:
        msg = f"for dimension '{dimension}'" if dimension else "in knowledge graph"
        console.print(f"[yellow]No measures found {msg}.[/yellow]")
        return

    if as_json:
        click.echo(json.dumps([m.__dict__ for m in ms], indent=2))
        return

    title = f"ACF Measures — {dimension}" if dimension else "ACF Measures"
    table = Table(title=title)
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Unit", style="dim")
    table.add_column("Collection", style="dim")
    table.add_column("Dimensions", style="green")

    for m in ms:
        table.add_row(
            m.id, m.name, m.unit, m.collection,
            ", ".join(m.dimensions) if m.dimensions else "-",
        )
    console.print(table)
    console.print(f"\n[dim]{len(ms)} measures total[/dim]")


@main.command()
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def levels(as_json: bool):
    """Show ACF certification levels."""
    graph = _get_graph()
    lvls = graph.levels()

    if not lvls:
        console.print("[yellow]No certification levels found.[/yellow]")
        return

    if as_json:
        click.echo(json.dumps([l.__dict__ for l in lvls], indent=2))
        return

    table = Table(title="ACF Certification Levels")
    table.add_column("Level", style="cyan bold")
    table.add_column("Label")
    table.add_column("Score Range", justify="right")
    table.add_column("Human Equivalent")

    for l in lvls:
        table.add_row(
            l.id, l.label,
            f"{l.score_min:.0f}–{l.score_max:.0f}",
            l.human_equivalent,
        )
    console.print(table)


@main.command("query")
@click.argument("sparql")
@click.option("--data", "-d", "data_dir", help="Data directory to include")
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def run_query(sparql: str, data_dir: str | None, as_json: bool):
    """Run a SPARQL query over the ACF knowledge graph."""
    graph = _get_graph(data_dir)

    try:
        results = graph.query(sparql)
    except Exception as e:
        console.print(f"[red]SPARQL error: {e}[/red]")
        sys.exit(1)

    if as_json:
        click.echo(json.dumps(results, indent=2))
        return

    if not results:
        console.print("[yellow]No results.[/yellow]")
        return

    # Auto-detect columns from first result
    columns = list(results[0].keys())
    table = Table(title="Query Results")
    for col in columns:
        table.add_column(col, style="cyan" if col == columns[0] else "")

    for row in results:
        table.add_row(*[row.get(c, "") for c in columns])

    console.print(table)
    console.print(f"\n[dim]{len(results)} results[/dim]")


@main.command()
@click.argument("path", type=click.Path(exists=True))
def validate(path: str):
    """Validate data files against ACF schemas."""
    p = Path(path)
    files = list(p.glob("*.json")) if p.is_dir() else [p]

    if not files:
        console.print("[yellow]No JSON files found.[/yellow]")
        return

    valid = 0
    invalid = 0
    for f in files:
        try:
            data = json.loads(f.read_text())
            # Basic envelope validation (per-query-record doesn't require measure_id)
            required = ["record_type"]
            if data.get("record_type") != "per-query-record":
                required.append("measure_id")
            missing = [k for k in required if k not in data]
            if missing:
                console.print(f"  [red]FAIL[/red] {f.name}: missing {missing}")
                invalid += 1
            else:
                console.print(f"  [green]OK[/green]   {f.name} ({data['record_type']})")
                valid += 1
        except json.JSONDecodeError as e:
            console.print(f"  [red]FAIL[/red] {f.name}: invalid JSON — {e}")
            invalid += 1

    console.print(f"\n{valid} valid, {invalid} invalid")
    if invalid > 0:
        sys.exit(1)


@main.command()
@click.argument("profile1", type=click.Path(exists=True))
@click.argument("profile2", type=click.Path(exists=True))
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def compare(profile1: str, profile2: str, as_json: bool):
    """Compare two ACF profiles side by side."""
    from acf.scoring.profile import ACFProfile

    p1 = ACFProfile.from_dict(json.loads(Path(profile1).read_text()))
    p2 = ACFProfile.from_dict(json.loads(Path(profile2).read_text()))

    if as_json:
        click.echo(json.dumps({
            "profile1": p1.to_dict(),
            "profile2": p2.to_dict(),
        }, indent=2))
        return

    table = Table(title="ACF Profile Comparison")
    table.add_column("Dimension", style="bold")
    table.add_column(p1.system_id, justify="right", style="cyan")
    table.add_column(p2.system_id, justify="right", style="green")
    table.add_column("Delta", justify="right")

    all_dims = sorted(set(list(p1.dimensions.keys()) + list(p2.dimensions.keys())))
    for dim in all_dims:
        s1 = p1.dimensions.get(dim)
        s2 = p2.dimensions.get(dim)
        v1 = f"{s1.score:.1f} ({s1.sub_level})" if s1 else "-"
        v2 = f"{s2.score:.1f} ({s2.sub_level})" if s2 else "-"
        delta = ""
        if s1 and s2:
            d = s2.score - s1.score
            color = "green" if d > 0 else "red" if d < 0 else "dim"
            delta = f"[{color}]{d:+.1f}[/{color}]"
        table.add_row(dim, v1, v2, delta)

    # Aggregate row
    table.add_section()
    d = p2.aggregate_score - p1.aggregate_score
    color = "green" if d > 0 else "red" if d < 0 else "dim"
    table.add_row(
        "[bold]Aggregate[/bold]",
        f"{p1.aggregate_score:.1f} ({p1.certification_level})",
        f"{p2.aggregate_score:.1f} ({p2.certification_level})",
        f"[{color}]{d:+.1f}[/{color}]",
    )
    console.print(table)


@main.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.option("--system", "-s", "system_id", help="Filter by system ID")
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
@click.option("--save", type=click.Path(), help="Save profile to JSON file")
def score(data_path: str, system_id: str | None, as_json: bool, save: str | None):
    """Score a system from collected data, producing an ACF profile."""
    from acf.scoring.profile import ACFDimensionScore, ACFProfile

    data_dir = Path(data_path)
    files = list(data_dir.glob("*.json")) if data_dir.is_dir() else [data_dir]

    if not files:
        console.print("[yellow]No JSON files found.[/yellow]")
        return

    graph = _get_graph()

    # Build measure -> dimensions lookup from the graph
    all_measures = graph.measures()
    measure_dims: dict[str, list[str]] = {}
    for m in all_measures:
        measure_dims[m.id] = m.dimensions

    # Collect experiment-run values: {measure_id: {system_id: {value, target, pass}}}
    records: list[dict] = []
    for f in files:
        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("record_type") != "experiment-run":
            continue
        sid = data.get("system_id") or data.get("being", "unknown")
        if system_id and sid != system_id:
            continue
        records.append({
            "system_id": sid,
            "measure_id": data.get("measure_id", ""),
            "value": data.get("value", 0.0),
            "target": data.get("target"),
            "passed": data.get("pass", False),
            "system_version": data.get("system_version", ""),
        })

    if not records:
        console.print("[yellow]No experiment-run records found.[/yellow]")
        if system_id:
            console.print(f"  Filtered by system: {system_id}")
        return

    # Auto-detect system_id from most common
    detected_systems = {}
    for r in records:
        detected_systems[r["system_id"]] = detected_systems.get(r["system_id"], 0) + 1

    if not system_id:
        # If multiple systems, show them and pick the one with most records
        if len(detected_systems) > 1:
            console.print("[dim]Multiple systems found in data:[/dim]")
            for sid, cnt in sorted(detected_systems.items(), key=lambda x: -x[1]):
                console.print(f"  {sid}: {cnt} records")
            system_id = max(detected_systems, key=detected_systems.get)
            console.print(f"[dim]Using: {system_id} (use --system to override)[/dim]\n")
            records = [r for r in records if r["system_id"] == system_id]
        else:
            system_id = next(iter(detected_systems))

    # Deduplicate: keep latest record per measure_id
    latest: dict[str, dict] = {}
    for r in records:
        mid = r["measure_id"]
        if mid not in latest:
            latest[mid] = r

    # Group measures by dimension
    dim_measures: dict[str, list[dict]] = {}
    unmapped: list[str] = []
    for mid, rec in latest.items():
        dims = measure_dims.get(mid, [])
        if not dims:
            unmapped.append(mid)
            continue
        for dim in dims:
            dim_measures.setdefault(dim, []).append(rec)

    # Score each dimension
    dim_scores: dict[str, ACFDimensionScore] = {}
    for dim_id, measure_recs in sorted(dim_measures.items()):
        total = len(measure_recs)
        passed = sum(1 for r in measure_recs if r["passed"])

        # Compute score from measure values
        # For percent-type measures, average the values directly
        values = [r["value"] for r in measure_recs if r["value"] is not None]
        if values:
            # Normalize: values > 1 assumed to be 0-100 scale; values <= 1 assumed 0-1 scale
            normalized = []
            for v in values:
                if v <= 1.0 and v >= 0.0:
                    normalized.append(v * 100)
                else:
                    normalized.append(min(v, 100.0))
            avg_value = sum(normalized) / len(normalized)
        else:
            avg_value = 0.0

        # Pass rate contributes to confidence, average value IS the score
        pass_rate = passed / total if total > 0 else 0.0
        dimension_score = avg_value

        # Determine sub-level from graph
        sub_levels = graph.sub_levels(dim_id)
        sub_level = "?"
        for sl in reversed(sub_levels):
            if sl.score_range:
                parts = sl.score_range.replace("–", "-").split("-")
                try:
                    low = float(parts[0].strip())
                    if dimension_score >= low:
                        sub_level = sl.id
                        break
                except (ValueError, IndexError):
                    continue
        if sub_level == "?" and sub_levels:
            sub_level = sub_levels[0].id

        confidence = "measured" if total >= 3 else "estimated"
        dim_scores[dim_id] = ACFDimensionScore(
            dimension=dim_id,
            score=round(dimension_score, 1),
            sub_level=sub_level,
            evidence=f"{passed}/{total} measures passed, avg={avg_value:.1f}",
            confidence=confidence,
        )

    # Build profile
    version = records[0].get("system_version", "") if records else ""
    profile = ACFProfile(
        system_id=system_id,
        system_type="unknown",
        version=version,
        dimensions=dim_scores,
    )

    if as_json or save:
        profile_json = json.dumps(profile.to_dict(), indent=2)
        if save:
            Path(save).write_text(profile_json + "\n")
            console.print(f"Profile saved to [bold]{save}[/bold]")
        if as_json:
            click.echo(profile_json)
            return

    # Rich table output
    console.print(f"\n[bold]ACF Profile: {system_id}[/bold] (v{version})")
    console.print()

    table = Table(title="Dimension Scores")
    table.add_column("Dimension", style="bold")
    table.add_column("Score", justify="right", style="cyan")
    table.add_column("Sub-Level", style="green")
    table.add_column("Evidence", style="dim")
    table.add_column("Conf.", style="dim")

    for dim_id in sorted(dim_scores):
        ds = dim_scores[dim_id]
        table.add_row(
            dim_id, f"{ds.score:.1f}", ds.sub_level,
            ds.evidence, ds.confidence,
        )

    console.print(table)

    # Aggregate
    console.print()
    console.print(f"  Aggregate Score: [bold cyan]{profile.aggregate_score:.1f}[/bold cyan]")
    console.print(f"  Certification:   [bold green]{profile.certification_level} — {profile.certification_label}[/bold green]")
    console.print(f"  Dimensions scored: {len(dim_scores)}/9")
    if unmapped:
        console.print(f"  [yellow]Unmapped measures: {', '.join(unmapped)}[/yellow]")
    console.print()


@main.command()
@click.argument("record_type", type=click.Choice([
    "experiment-run", "longitudinal-series", "per-query-record",
]))
def template(record_type: str):
    """Print a blank data template for a record type."""
    templates = {
        "experiment-run": {
            "schema_version": "1.0.0",
            "record_type": "experiment-run",
            "system_version": "",
            "experiment_id": "",
            "timestamp": "",
            "system_id": "",
            "measure_id": "M-XXX",
            "collector": "manual",
            "condition_a": {"label": "", "system_version": ""},
            "condition_b": {"label": "", "system_version": ""},
            "n": 0,
            "value": 0.0,
            "target": 0.0,
            "comparison": "GE",
            "pass": False,
            "notes": "",
        },
        "longitudinal-series": {
            "schema_version": "1.0.0",
            "record_type": "longitudinal-series",
            "system_version": "",
            "experiment_id": "",
            "timestamp": "",
            "system_id": "",
            "measure_id": "M-XXX",
            "collector": "automated",
            "data_points": [
                {"system_version": "", "value": 0.0, "timestamp": ""}
            ],
            "trend": {"direction": "stable", "slope": 0.0},
            "notes": "",
        },
        "per-query-record": {
            "schema_version": "1.0.0",
            "record_type": "per-query-record",
            "system_version": "",
            "experiment_id": "",
            "timestamp": "",
            "system_id": "",
            "measure_id": "M-XXX",
            "collector": "automated",
            "query": "",
            "response": "",
            "signals": {},
            "notes": "",
        },
    }
    click.echo(json.dumps(templates[record_type], indent=2))


@main.command()
@click.option("--json-output", "as_json", is_flag=True, help="Output as JSON")
def info(as_json: bool):
    """Show ACF framework information and graph statistics."""
    graph = _get_graph()

    stats = {
        "knowledge_dir": str(KNOWLEDGE_DIR),
        "total_triples": graph.triple_count(),
        "dimensions": len(graph.dimensions()),
        "measures": len(graph.measures()),
        "levels": len(graph.levels()),
        "hypotheses": len(graph.hypotheses()),
    }

    if as_json:
        click.echo(json.dumps(stats, indent=2))
        return

    console.print("[bold]ACF Framework[/bold]")
    console.print(f"  Knowledge: {stats['knowledge_dir']}")
    console.print(f"  Triples:   {stats['total_triples']}")
    console.print(f"  Dimensions: {stats['dimensions']}")
    console.print(f"  Measures:  {stats['measures']}")
    console.print(f"  Levels:    {stats['levels']}")
    console.print(f"  Hypotheses: {stats['hypotheses']}")


if __name__ == "__main__":
    main()
