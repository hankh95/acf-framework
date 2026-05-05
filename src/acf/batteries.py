"""
ACF battery loaders and the BatteryRunner protocol.

This module provides:

  - `load_battery(name)` — load a battery's JSONL items as Python dicts
  - `list_batteries()` — discover available batteries in the package
  - `BatteryRunner` — a Protocol for systems-under-test to implement

It does NOT include the system-under-test scoring procedure. The reference
scoring procedures are battery-specific and platform-specific:

  - **Graph-backed systems** (NeSy with rule-firing trace) use the
    graph-structural scorers documented in each battery's methodology
    document under `batteries/<name>/<name>-methodology.md`. Reference
    Python implementations live in the upstream nusy-product-team
    monorepo at `scripts/run_fr_benchmark.py` and
    `scripts/run_cg_benchmark.py`; the canonical Zorblaxia classifier
    lives in `crates/nusy-safety/src/zorblaxia.rs`.

  - **LLM systems** require an adapted scoring path (final-answer
    correctness via an LLM judge, plus heuristic Zorblaxia
    classification). A reference adapter is documented in Paper 122 §5.

The `acf-framework` v1.1.0 package ships the schemas, items, and this
loader. It does not ship a bundled LLM-judge runner; the methodology
documents specify the procedure so third parties can implement against
their own LLM provider, evaluation harness, or compute environment.
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Iterable, Protocol, TypedDict, runtime_checkable

# These are the canonical battery names. The actual JSONL files live at
# repo-root/batteries/<name>/<name>.jsonl in the source tree, and at the
# package's `batteries/` subtree once installed.
BATTERY_NAMES: tuple[str, ...] = ("fr36", "zorblaxia", "cg100")


class BatteryItem(TypedDict, total=False):
    """A single battery item. All batteries share these keys; per-battery
    extras (level, subtype, category, domain, graph_eval_criteria, etc.)
    are present where applicable."""

    id: str
    battery: str
    question: str
    expected_behavior: str  # "answer" | "refuse" | other
    acf_dimension: str
    validates_hypothesis: str


def _battery_root() -> Path:
    """Locate the on-disk batteries directory.

    Returns the first match of:
      1. `<repo-root>/batteries/` (development install)
      2. The packaged `batteries/` subtree (if shipped via wheel)
    """
    here = Path(__file__).resolve()
    # Walk up until we find a sibling `batteries/` dir
    for parent in [here.parent, here.parent.parent, here.parent.parent.parent]:
        candidate = parent / "batteries"
        if candidate.is_dir() and (candidate / "fr36").is_dir():
            return candidate
    # Fall back to the package's installed location, if any
    try:
        with resources.as_file(resources.files("acf").joinpath("../batteries")) as path:
            if path.is_dir():
                return path
    except (FileNotFoundError, ModuleNotFoundError):
        pass
    raise FileNotFoundError(
        "Could not locate the `batteries/` directory. Are you running from "
        "the acf-framework repo root? The expected layout is "
        "`<repo>/batteries/{fr36,zorblaxia,cg100}/<name>.jsonl`."
    )


def list_batteries() -> list[str]:
    """Return the names of the batteries shipped in this distribution."""
    root = _battery_root()
    found = []
    for name in BATTERY_NAMES:
        if (root / name / f"{name}.jsonl").is_file():
            found.append(name)
    return found


def load_battery(name: str) -> list[BatteryItem]:
    """Load all items in the named battery as a list of dicts.

    Args:
        name: One of `fr36`, `zorblaxia`, `cg100`.

    Returns:
        List of battery items. The order matches the JSONL file order,
        which matches the published item id ordering — important because
        the reference graph-structural scorers pass the top-N items in
        this order.

    Raises:
        ValueError: if `name` is not a known battery.
        FileNotFoundError: if the JSONL is missing on disk.
    """
    if name not in BATTERY_NAMES:
        raise ValueError(
            f"Unknown battery {name!r}. Available: {', '.join(BATTERY_NAMES)}."
        )
    path = _battery_root() / name / f"{name}.jsonl"
    if not path.is_file():
        raise FileNotFoundError(f"Battery JSONL not found: {path}")
    items: list[BatteryItem] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def battery_methodology_path(name: str) -> Path:
    """Return the on-disk path to a battery's methodology document."""
    if name not in BATTERY_NAMES:
        raise ValueError(f"Unknown battery {name!r}.")
    return _battery_root() / name / f"{name}-methodology.md"


@runtime_checkable
class BatteryRunner(Protocol):
    """Protocol that systems-under-test implement to be scored on a battery.

    A `BatteryRunner` takes a single battery item and returns the
    system's response, including any provenance / trace information the
    battery's scorer needs.

    The minimal contract:

        def run_item(self, item: BatteryItem) -> dict:
            '''Return at least {"id": item["id"], "response_text": str}.

            Optional fields (used by the graph-structural scorers when
            present):
              - "rule_trace": list of inference-rule firings
              - "predicate_trace": list of predicates invoked
              - "chain_depth": int
              - "confidence": float in [0, 1]
              - "provenance": list of source pointers
            '''
    """

    def run_item(self, item: BatteryItem) -> dict: ...


def iter_battery(name: str) -> Iterable[BatteryItem]:
    """Generator-style alternative to `load_battery` for streaming."""
    yield from load_battery(name)
