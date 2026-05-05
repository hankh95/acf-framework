"""HuggingFace `datasets` loading script for ACF batteries.

Usage:
    from datasets import load_dataset
    fr36 = load_dataset("congruent-systems/acf-batteries", "fr36")
    zorb = load_dataset("congruent-systems/acf-batteries", "zorblaxia")
    cg100 = load_dataset("congruent-systems/acf-batteries", "cg100")

Once published to HuggingFace Hub at the above repo ID, this script
loads the JSONL files directly from the Hub.

This file is the canonical loading script. For local development:
    from acf_framework.batteries import load_local
    fr36 = load_local("fr36", "/path/to/acf-framework/batteries")
"""

import json
import os
from pathlib import Path

import datasets

_CITATION = """
@software{acf-framework-v1.1.0,
  title = {ACF Framework v1.1.0: A Neurosymbolic Capability Benchmark},
  author = {Head, Hank and {Congruent Systems LLC}},
  year = {2026},
  version = {1.1.0},
  url = {https://github.com/hankh95/acf-framework},
  license = {MIT}
}
"""

_DESCRIPTION = """
ACF (AGI Certification Framework) battery datasets — three NeSy-native
task batteries for jointly scoring Knowledge Transparency, Formal
Reasoning, Factual Grounding, and Generalization Boundary Awareness on
the same task instances.

  - fr36       (Formal Reasoning, 36 items, FR1/FR2/FR-boundary)
  - zorblaxia  (Generalization Boundary Awareness, 10 items)
  - cg100      (Compositional Generalization, 100 items, 3 sub-levels x 5 domains)
"""

_HOMEPAGE = "https://github.com/hankh95/acf-framework"
_LICENSE = "CC-BY-4.0"

_URLS = {
    "fr36":      "https://github.com/hankh95/acf-framework/raw/main/batteries/fr36/fr36.jsonl",
    "zorblaxia": "https://github.com/hankh95/acf-framework/raw/main/batteries/zorblaxia/zorblaxia.jsonl",
    "cg100":     "https://github.com/hankh95/acf-framework/raw/main/batteries/cg100/cg100.jsonl",
}


class ACFBatteriesConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super().__init__(version=datasets.Version("1.1.0"), **kwargs)


class ACFBatteries(datasets.GeneratorBasedBuilder):
    """Three battery datasets in a single repo, accessed by config name."""

    BUILDER_CONFIGS = [
        ACFBatteriesConfig(name="fr36",      description="Formal Reasoning (36 items)"),
        ACFBatteriesConfig(name="zorblaxia", description="Generalization Boundary Awareness (10 items)"),
        ACFBatteriesConfig(name="cg100",     description="Compositional Generalization (100 items)"),
    ]

    def _info(self):
        # Common fields across all three batteries; per-battery fields are nullable.
        features = datasets.Features({
            "id": datasets.Value("string"),
            "battery": datasets.Value("string"),
            "level": datasets.Value("string"),
            "subtype": datasets.Value("string"),
            "category": datasets.Value("string"),
            "domain": datasets.Value("string"),
            "question": datasets.Value("string"),
            "expected_behavior": datasets.Value("string"),
            "expected_behavior_detail": datasets.Value("string"),
            "graph_eval_criteria": datasets.Value("string"),
            "training_context": datasets.Value("string"),
            "novel_composition": datasets.Value("string"),
            "rule_chain": datasets.Value("string"),
            "target_level": datasets.Value("string"),
            "acf_dimension": datasets.Value("string"),
            "validates_hypothesis": datasets.Value("string"),
        })
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        url = _URLS[self.config.name]
        path = dl_manager.download(url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": path},
            )
        ]

    def _generate_examples(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                # Normalize: every field present (None if absent in this battery).
                normalized = {k: rec.get(k) for k in self._info().features}
                # Coerce list fields to JSON strings (HF loaders prefer flat features).
                for k, v in normalized.items():
                    if isinstance(v, (list, dict)):
                        normalized[k] = json.dumps(v, ensure_ascii=False)
                yield idx, normalized


def load_local(battery_name, root="."):
    """Bypass the Hub and load directly from a local checkout of the repo."""
    path = Path(root) / "batteries" / battery_name / f"{battery_name}.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"Battery JSONL not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
