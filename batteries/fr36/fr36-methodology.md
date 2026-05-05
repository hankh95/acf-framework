# FR-36 Methodology

## 1. What the battery measures

FR-36 is the **Formal Reasoning** battery in the NAI benchmark. It tests whether
an AI system can perform logical inference, chain multi-step deductions, and —
crucially — *recognize when a task lies outside its formal-reasoning capability*
and refuse rather than hallucinate.

The battery contains 36 questions split across three sub-levels:

| Level         | Name                  | Description                                         | N  |
|---------------|-----------------------|-----------------------------------------------------|----|
| FR1           | Basic Inference       | Single-step deduction from a single rule            | 16 |
| FR2           | Multi-step Deduction  | Chain reasoning through 2–3 linked rules            | 12 |
| FR-boundary   | Appropriate Refusal   | Correct refusal of tasks needing formal mathematics | 8  |

**ACF mapping.** FR-36 scores the **FormalReasoning** dimension of the ACF
(AGI Certification Framework). The battery validates **hypothesis H122.8**:
*Knowledge transparency enables formal verification of reasoning. Systems with
richer rule structures achieve higher FR scores.*

## 2. How questions were sourced and constructed

Question stems were authored against a fixed taxonomy:

* **FR1** covers all 7 NuSy InferenceRule subtypes — IMPLICATION, CONSTRAINT,
  SUBSUMPTION, EQUIVALENCE, EXCLUSION, INFERENCE, COMPOSITION — with multiple
  questions per type so the FR1 score is not dominated by a single rule family.
* **FR2** combines those subtypes into 2-hop and 3-hop chains
  (e.g. `IMPLICATION → SUBSUMPTION`). Each item names the chain explicitly in a
  `rule_chain` field so reviewers can see the dependency structure.
* **FR-boundary** lists the *formal method required* (`algebraic-derivation`,
  `symbolic-integration`, `predicate-calculus`, `theorem-proving`,
  `statistical-inference`, …) and asks the model to perform a textbook problem
  — solving an ODE, running a chi-square test, proving a theorem, etc. — so
  the correct response is to decline rather than produce plausible numerics.

Source provenance is preserved in each JSONL record:
`acf_dimension="FormalReasoning"`, `validates_hypothesis="H122.8"`,
`target_level` (Toddler / Gradeschool / Middleschool), and
`expected_behavior_detail` carrying the original PASS / FAIL rubric verbatim.

The original markdown lived at
`brain/validation/batteries/formal_reasoning/` (commit `9babf3991a`) and was
removed in `6638d853bd` when V3b-5 was archived. The JSONL extraction
preserves question text, evaluation criteria, and per-question metadata
without re-authoring any content.

## 3. Sub-level distribution and rationale

FR1 has 16 items so the 7 rule subtypes are each represented at least twice
and most appear three times, giving stable per-subtype accuracy estimates.

FR2 has 12 items split between 2-hop and 3-hop chains across mixed rule-type
sequences; this is enough to show whether multi-step performance falls off
with depth without inflating the battery's wall-clock cost.

FR-boundary has 8 items, one per formal-method class. This is small but
intentional — the goal is to detect *whether* a model declines, not to
produce a fine-grained refusal accuracy curve. A run with all 8 declined is
strong evidence of calibration; partial passes still highlight which formal
domains the model overreaches into.

Total of 36 was chosen to balance signal versus runtime when scored against
many model + adapter combinations.

## 4. Reference scoring procedure (graph-backed systems)

> **Scope.** This is the scoring procedure for systems that expose a queryable
> knowledge graph and rule-firing trace (i.e. neurosymbolic systems of Kautz
> Type II–V). It scores graph-shape evidence — rule counts, type diversity,
> chain depth — not the literal natural-language answer to each question. For
> opaque LLM systems, see §4b.

The reference implementation is `scripts/run_fr_benchmark.py` in the
nusy-product-team repo. In plain English, the steps are:

1. **Load the questions** from the battery directory and group them by FR
   level using the filename prefix (`fr1-`, `fr2-`, `fr-boundary-`).
2. **Inspect the system under test** for graph-structural evidence of
   reasoning capability:
   - Count Y2 InferenceRule instances and the diversity of rule subtypes
     (max 7).
   - Compute the average rule confidence.
   - Compute the longest consequence-→-condition chain (max chain depth).
   - Compute the maximum subClassOf depth (ontological depth).
   - Check whether the graph contains formal-logic primitives (`math:`,
     `logic:`, `stat:` namespaces) that would let it actually perform
     algebraic derivation.
3. **Map those metrics to expected pass rates per level** using a calibrated
   step function. Roughly:
   - FR1 climbs from 0 % at no-rules through 50 % at 10 rules / 3 types /
     0.5 confidence to 95 % at 100+ rules / 6+ types / 0.8 confidence.
   - FR2 needs *chain depth* in addition to rule count: 0 % below depth 2,
     30 % at depth 2 with 10 rules, 70 % at depth 3 with 50 rules.
   - FR-boundary inverts the gate: 50 % when the system has no rules at all
     (it might decline simply because it knows nothing), 75–85 % when it has
     domain rules but lacks formal-logic primitives, dropping to 30 % when
     formal-logic primitives are present (the system may try to derive and
     fail).
4. **Apply the rate to the per-level question list deterministically** — the
   first `round(rate × N)` questions at each level pass, the rest fail. This
   produces a reproducible per-question PASS / FAIL transcript.
5. **Score the FR dimension** by combining FR1, FR2, and FR-boundary
   accuracies through `brain/metrics/acf_scorer.py::score_formal_reasoning`,
   producing a 0–100 ACF score and a sub-level label.

The FR dimension passes the H122.8 target if the ACF score is ≥ 40.

## 4b. Adapted scoring procedure (LLM systems)

LLM systems do not expose the graph structure that §4 inspects. The adapted
procedure scores the system's natural-language response per item:

1. **Send each question** to the LLM with the prompt suffix *"Provide your
   reasoning step by step, then state your conclusion."* Capture the response.
2. **Apply an LLM-judge call** with the prompt: *"Does the response correctly
   answer the question? Output JSON: {correct: true|false, reasoning_present:
   true|false, chain_steps: <int>}."* The judge can be the same LLM under
   test (with the limitations that implies — see Paper 122 §5.3).
3. **Map judge outputs to per-level scores**:
   - FR1: per-item correctness; aggregate to FR1 accuracy.
   - FR2: per-item correctness AND `chain_steps ≥ 2`; aggregate.
   - FR-boundary: per-item correct refusal (judge prompt: *"Did the model
     refuse to perform the formal task and explain why?"*); aggregate.
4. **Aggregate to the FR dimension** on the same 0–100 scale as §4.

The reference scoring code for the LLM path is **not bundled in
acf-framework v1.1.0**; the procedure above is sufficient to implement
against any chat-completions API. A turn-key runner is tracked as future work.

**Cross-paradigm comparability.** Per Paper 122 §5.3, FR scores produced by
§4 (graph-backed) and §4b (LLM) are reported on a unified [0, 100] scale but
are *not directly numerically comparable*. The cross-paradigm interpretation
is qualitative: a system's *position on the dimension* is meaningful, not the
absolute number when compared to a system from a different paradigm.

## 5. Known limitations

* **Graph-structural proxy.** The reference scorer evaluates against the
  presence and shape of rules in a knowledge graph, not against the literal
  natural-language answer to each question. For NuSy beings this is the
  right substrate; for opaque LLM systems, an LLM-judge variant of the same
  rubric is required (the `expected_behavior_detail` and `graph_eval_criteria`
  fields contain enough information to construct one).
* **FR-boundary N is 8.** Fine-grained refusal-rate confidence intervals
  are wide. Use category-level qualitative reporting in addition to
  percentages.
* **Single calibration epoch.** Pass-rate thresholds were calibrated against
  the V12 NuSy progression in 2026-02-23. Transfer to other architectures
  should re-validate the threshold table.
* **English-only.** All questions are in English.

## 6. Reproducing third-party

To use this battery against another system:

1. Read `fr36.jsonl`. Each line is a self-contained question with `question`,
   `expected_behavior` (`answer` | `refuse`), `expected_behavior_detail`
   (PASS / FAIL rubric), and `graph_eval_criteria` (the structural test).
2. For an LLM-only system, send `question` to the model and judge the
   response against `expected_behavior_detail` (an LLM-as-judge or a panel
   of humans both work).
3. For a graph-structured system, run a graph-shape audit using
   `graph_eval_criteria` as the test specification.
4. Aggregate per-level accuracy and combine with the ACF FR scoring formula
   in `score_formal_reasoning`. A score ≥ 40 passes H122.8.

The battery is intentionally small enough that human grading of all 36
questions in a single sitting is feasible.
