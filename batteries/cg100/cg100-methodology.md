# CG-100 Methodology

## 1. What the battery measures

CG-100 is the **Compositional Generalization** battery in the NAI benchmark. It
tests whether an AI system can recombine known primitives — entities, structures,
rules — into novel compositions it has not seen during training. Compositional
generalization is widely treated as the hallmark of *systematic* (versus merely
pattern-matched) intelligence.

The battery contains 100 questions across three sub-levels and five domains:

| Level | Name        | Description                                            | N   |
|-------|-------------|--------------------------------------------------------|-----|
| CG1   | Lexical     | New entities slotted into known structural patterns    | 30  |
| CG2   | Structural  | Known entities combined in novel structural patterns   | 40  |
| CG3   | Productive  | Recursive / unbounded composition (chains, nesting)    | 30  |

**ACF mapping.** CG-100 scores the **CompositionalGeneralization** dimension
of the ACF and validates **hypothesis H122.7**: *Systems trained on structured
knowledge graphs demonstrate compositional generalization that exceeds
pattern-matching baselines, because graph-structured knowledge inherently
supports recombination.*

## 2. How questions were sourced and constructed

Each question is paired with an explicit `training_context` (what prior
knowledge the system is assumed to have) and a `novel_composition` field
(why this specific question is novel given that context). This separation is
deliberate — it lets reviewers verify that the test really is compositional
rather than memorized.

The five domains are:

| Domain     | Coverage                                              |
|------------|-------------------------------------------------------|
| `lang`     | Sentence structure, morphology, word composition      |
| `science`  | Natural world, physical processes, biology            |
| `logic`    | Deduction, induction, conditional reasoning           |
| `narrative`| Story structure, character reasoning, plot            |
| `social`   | Social rules, fairness, perspective-taking            |

Within each level, every domain receives the same number of items so domain
imbalance cannot bias level-aggregate scores. Each item draws on
SCAN/COGS-style construction patterns (for `lang` and `logic`) or
narrative/scientific scenarios that compose two known primitives into a
combination the system would not have memorized.

Source provenance is preserved per record: `acf_dimension`,
`validates_hypothesis`, `target_level`, and the original PASS / FAIL rubric
in `expected_behavior_detail`.

The original markdown lived at
`brain/validation/batteries/compositional_generalization/` (commit
`9babf3991a`) and was archived alongside V3b-5; the JSONL preserves the
question, training context, novel-composition explanation, and rubric verbatim.

## 3. Sub-level distribution and rationale

* **CG1: 30 questions, 6 per domain.** Lexical generalization is the easiest
  sub-level; 6 items per domain is enough to estimate per-domain accuracy
  with reasonable confidence.
* **CG2: 40 questions, 8 per domain.** Structural generalization is the
  *load-bearing* level — most everyday compositional tasks live here, so we
  spend the most question budget here. With 8 items per domain, per-domain
  CG2 accuracy can flag a domain-specific weakness.
* **CG3: 30 questions, 6 per domain.** Productive (recursive / unbounded)
  composition is the hardest level. Six per domain is enough to see whether
  productive performance collapses entirely or scales with depth.

The 30/40/30 split is intentionally bottom-heavy on structural items because
that is where systems most often fail in interesting ways — fully lexical
items are usually solved by string-pattern templates, and fully productive
items are often refused by everything.

## 4. Reference scoring procedure (graph-backed systems)

> **Scope.** This procedure scores graph-shape evidence — predicate diversity,
> multi-hop ratio, chain depth, Y-layer compositional predicate coverage —
> not the literal natural-language answer to each question. Appropriate for
> neurosymbolic systems that expose a queryable knowledge graph. For LLM
> systems, see §4b.

The reference implementation is `scripts/run_cg_benchmark.py` in the
nusy-product-team repo. In plain English:

1. **Load the questions** and group by CG level using the filename prefix
   (`cg1-`, `cg2-`, `cg3-`).
2. **Inspect the knowledge graph** of the system under test for structural
   compositional capacity:
   - Count distinct non-metadata predicates (`predicate_diversity`).
   - Compute the *multi-hop ratio* — the fraction of entities that appear
     as both subject and object (these are "connector" nodes that enable
     composition).
   - Estimate the longest A → B → C → … chain via BFS from sampled
     connector nodes.
   - Count Y-layer compositional predicates (`y2:condition`,
     `y2:consequence`, `y4:topic`, …) and causal predicates (`causes`,
     `leads_to`, `requires`, `enables`, …).
3. **Map metrics to per-level pass rates** with a calibrated step function:
   - **CG1** is driven by predicate diversity. Roughly 50 % at 10
     non-metadata predicates, 95 % at 30+ predicates, conditional on at
     least 100 triples in the graph.
   - **CG2** is driven by the multi-hop ratio plus compositional or causal
     predicates: 50 % at multi-hop ≥ 3 % with some Y-layer or causal preds,
     scaling to 85 % at multi-hop ≥ 8 % with both.
   - **CG3** is driven by chain depth combined with Y-layer and causal
     coverage: 30 % at depth 2, 55 % at depth 3 with richer Y-layer, 90 % at
     depth 8 with full coverage. A multi-hop bonus tops up CG3 when
     connectivity is unusually high.
4. **Apply the rate deterministically** — the first `round(rate × N)`
   questions at each level pass, in filename order. (Within a level,
   filename order corresponds to authoring order, which gives a rough
   easy-to-hard gradient.)
5. **Score the CG dimension** by combining CG1, CG2, and CG3 accuracies via
   `brain/metrics/acf_scorer.py::score_compositional_generalization`,
   producing a 0–100 ACF score, a sub-level label, and per-domain
   breakdowns.

H122.7 passes when overall CG accuracy is ≥ 80 %.

## 4b. Adapted scoring procedure (LLM systems)

LLM systems do not expose the graph structure that §4 inspects. The adapted
procedure is:

1. **Send each question** to the LLM with the prompt suffix *"Provide your
   answer and your reasoning."* Capture the response.
2. **Apply an LLM-judge call**: *"Does the response demonstrate compositional
   reasoning that addresses the question? Output JSON: {answer_addresses_question:
   true|false, composition_evidence: 'none'|'lexical'|'structural'|'productive'}."*
3. **Map judge outputs to per-level scores**:
   - **CG1** (lexical): per-item correctness aggregated.
   - **CG2** (structural): per-item correctness AND `composition_evidence ∈
     {structural, productive}` aggregated.
   - **CG3** (productive): per-item correctness AND `composition_evidence =
     productive` aggregated.
4. **Aggregate to the CG dimension** on the same 0–100 scale as §4.

Reference code for the LLM path is **not bundled in v1.1.0**; the procedure
above implements against any chat-completions API. **Cross-paradigm scores
are reported on a unified scale but are not directly numerically comparable**
— see Paper 122 §5.3.

## 5. Known limitations

* **Graph-structural proxy.** Like FR-36, the reference scorer audits a
  graph rather than judging natural-language answers. For LLM-only systems,
  an LLM-judge variant against `expected_behavior_detail` is needed; for
  graph-backed systems the proxy is appropriate.
* **Calibration is V12-anchored.** The threshold table reflects the V12 NuSy
  being progression. Other architectures should re-fit thresholds before
  using the absolute scores comparatively.
* **Per-domain depth.** Six items per (level × domain) cell gives 17 %
  granularity per cell. Aggregate level scores are robust; per-cell scores
  are indicative.
* **English-only and Western-centric.** Domains were authored in English
  with implicit Western-context defaults (especially in `social` and
  `narrative`).
* **Open-ended.** Every question is `OpenEnded` — there is no single canonical
  string answer, so judging always involves a rubric.

## 6. Reproducing third-party

To run CG-100 against another system:

1. Read `cg100.jsonl`. Each record is self-contained: `question`,
   `training_context` (what to assume the system has learned),
   `novel_composition` (why this question is novel), and
   `expected_behavior_detail` (PASS / FAIL rubric).
2. Send `question` to the model. Judge the response against
   `expected_behavior_detail` either with an LLM judge or human raters; for
   reliability, prefer two independent raters and report inter-rater
   agreement.
3. Aggregate per-level accuracy (and optionally per-domain) and combine
   through the `score_compositional_generalization` formula. Overall ≥ 80 %
   passes H122.7.

CG-100 is intentionally large enough that LLM-graded automation is the
practical path; full human grading of all 100 questions is possible but
expensive.
