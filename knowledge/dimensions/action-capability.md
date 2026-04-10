---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ActionCapability> a acf:Dimension ;
    acf:id "action_capability" ;
    acf:label "Action Capability" ;
    acf:shortName "AC" ;
    acf:subLevelCount 4 ;
    acf:weight 0.10 ;
    acf:description "Measures a system's ability to execute known procedures on novel inputs, not merely describe or recall them. Closes the knowledge-action gap between procedural knowledge coverage and actual execution success." .

<#AC1> a acf:SubLevel ;
    acf:id "AC1" ;
    acf:dimension <#ActionCapability> ;
    acf:level 1 ;
    acf:label "Identify" ;
    acf:scoreRange "15-29" ;
    acf:description "Recognizes when action is needed; selects appropriate procedure from knowledge." .

<#AC2> a acf:SubLevel ;
    acf:id "AC2" ;
    acf:dimension <#ActionCapability> ;
    acf:level 2 ;
    acf:label "Apply" ;
    acf:scoreRange "30-59" ;
    acf:description "Executes known procedures on novel inputs; produces correct, verifiable outputs." .

<#AC3> a acf:SubLevel ;
    acf:id "AC3" ;
    acf:dimension <#ActionCapability> ;
    acf:level 3 ;
    acf:label "Adapt" ;
    acf:scoreRange "60-74" ;
    acf:description "Modifies procedures for new contexts; handles edge cases and partial information." .

<#AC4> a acf:SubLevel ;
    acf:id "AC4" ;
    acf:dimension <#ActionCapability> ;
    acf:level 4 ;
    acf:label "Optimize" ;
    acf:scoreRange "75-100" ;
    acf:description "Creates new procedures; improves existing ones based on execution feedback." .
---

# Action Capability

Action Capability measures a system's ability to **execute known procedures** on novel inputs, not merely describe or recall them. This dimension closes the *knowledge-action gap* — the empirical disconnect between procedural knowledge coverage and actual execution success.

## Motivation: The Knowledge-Action Gap

Research shows a measurable gap between knowing and doing:

| System | Knowledge | Execution | Gap |
|--------|-----------|-----------|-----|
| Expert System (FHIR-CPG) | 95% | 92-96% | 0-3% |
| LLM (GPT-4) | 82-87% | 41-48% | 38-43% |
| Neurosymbolic (before action framework) | 91-93% | 12-18% | 74-80% |
| Neurosymbolic (with action framework) | 91-93% | 63-71% | 22-28% |

Existing ACF dimensions don't capture this gap:
- **Depth (L3: Apply)** measures whether a system *can reason* about application — not whether it can *execute*
- **Service Orientation (SO1: Task Completion)** measures end-to-end helpfulness — AC measures the specific ability to ground a procedure template against novel context
- **Autonomy (AU3: Self-Learning)** measures knowledge acquisition — AC measures knowledge *application*

## Sub-Levels

### AC1: Identify (15-29)
Recognizes when action is needed; selects appropriate procedure from knowledge.

Human equivalent: Student identifies which formula to use.

### AC2: Apply (30-59)
Executes known procedures on novel inputs; produces correct, verifiable outputs.

Human equivalent: Practitioner applies knowledge to cases.

### AC3: Adapt (60-74)
Modifies procedures for new contexts; handles edge cases and partial information.

Human equivalent: Expert adapts standard procedures.

### AC4: Optimize (75-100)
Creates new procedures; improves existing ones based on execution feedback.

Human equivalent: Master innovates new approaches.

## Composite Score

The AC composite score is calculated as:

```
AC_composite = PER x SCR x ACR x 100

Where:
  PER = Procedure Execution Rate (procedures attempted / procedures in knowledge)
  SCR = Step Completion Rate (steps correct / steps attempted)
  ACR = Answer Correctness Rate (correct outputs / procedures completed)

Example: PER=0.80, SCR=0.90, ACR=0.85 -> AC_composite = 61.2
```

This multiplicative formula captures that all three components are necessary: a system that attempts many procedures but completes few steps correctly scores low, and a system that completes steps correctly but produces wrong final outputs also scores low.

## Test Protocol

### Phase 1: Procedure Identification (AC1)
1. Present 20 scenarios requiring procedural knowledge
2. System must identify the correct procedure from its knowledge graph
3. Score: percentage of scenarios where correct procedure is identified

### Phase 2: Novel Execution (AC2)
1. Present 15 problems requiring execution of known procedures on new inputs
2. System must produce verifiable outputs (not just descriptions)
3. Audit each step for correctness
4. Score: PER x SCR x ACR composite

### Phase 3: Adaptive Execution (AC3)
1. Present 10 problems that require procedure modification
2. Missing parameters, edge cases, partial knowledge
3. Score: Success rate on adapted executions

### Phase 4: Procedure Creation (AC4)
1. Present 5 novel problems where no existing procedure applies
2. System must compose a new procedure from component knowledge
3. Score: Expert rating on created procedures

## Certification Flags

| Flag | Criteria | Meaning |
|------|----------|---------|
| Knowledge-Only | Depth >= L4 AND AC < AC2 | High knowledge but cannot execute |
| Procedural | AC >= AC2 AND Depth < L3 | Can execute but lacks understanding |
| Professional | AC >= AC2 AND FG >= FG3 | Executes with provenance |
| Adaptive | AC >= AC3 AND GBA >= GBA3 | Adapts while respecting boundaries |

## Relationship to Other Dimensions

| Dimension | Relationship to AC |
|-----------|-------------------|
| Depth (L3: Apply) | L3 measures reasoning about application; AC measures actual execution |
| Service Orientation | SO measures end-to-end helpfulness; AC is the mechanism |
| Autonomy | AU3 (self-learning) feeds AC: newly learned procedures become executable |
| Formal Reasoning | FR provides the logical framework; AC applies it to produce outputs |
| Factual Grounding | FG ensures action outputs are evidence-based |
| GBA | GBA2 (boundary detection) informs AC: system should refuse beyond its competence |

New in ACF v1.1. Source: Paper 128 — "From Knowledge to Action: Closing the Execution Gap in Neurosymbolic Cognitive Agents."
