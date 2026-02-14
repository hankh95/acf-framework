---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-047> a acf:Measure ;
    rdfs:label "Fact Correctness Rate" ;
    acf:id "M-047" ;
    acf:name "fact_correctness_rate" ;
    acf:description "Percentage of extracted facts verified as factually correct through automated or LLM-graded evaluation against source documents and external references." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#FactualGrounding> .

<#M-048> a acf:Measure ;
    rdfs:label "Inference Coherence" ;
    acf:id "M-048" ;
    acf:name "inference_coherence" ;
    acf:description "Percentage of inferred knowledge items that are logically consistent with their supporting facts and relationships. Evaluates whether the reasoning layer produces valid conclusions from its premises." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#FormalReasoning>, <#Depth> .

<#M-049> a acf:Measure ;
    rdfs:label "Procedure Validity" ;
    acf:id "M-049" ;
    acf:name "procedure_validity" ;
    acf:description "Percentage of procedural skills that execute correctly when invoked, producing expected outcomes without errors or unintended side effects." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#Autonomy> .

<#M-050> a acf:Measure ;
    rdfs:label "Metacognition Accuracy" ;
    acf:id "M-050" ;
    acf:name "metacognition_accuracy" ;
    acf:description "Accuracy of the system's self-knowledge claims, measured as the percentage of metacognitive assertions that align with independently verified ground truth about the system's actual capabilities and knowledge state." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#GeneralizationBoundary> .

<#M-051> a acf:Measure ;
    rdfs:label "Knowledge Freshness" ;
    acf:id "M-051" ;
    acf:name "knowledge_freshness" ;
    acf:description "Percentage of knowledge items that have been updated or revalidated within a defined target time window. Measures whether the knowledge base is actively maintained or becoming stale." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .

<#M-052> a acf:Measure ;
    rdfs:label "Cross-Reference Integrity" ;
    acf:id "M-052" ;
    acf:name "cross_reference_integrity" ;
    acf:description "Percentage of cross-references between knowledge items that resolve correctly to valid targets. Detects broken links, orphaned references, and referential inconsistencies in the knowledge graph." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-quality" ;
    acf:collection "automated" ;
    acf:mapsTo <#KnowledgeTransparency> .
---

# Y-Layer Quality Measures (M-047 to M-052)

Y-Layer Quality measures evaluate the correctness, consistency, and integrity of knowledge stored across all layers. While population measures tell you how much knowledge exists and growth measures tell you how fast it is accumulating, quality measures answer the harder question: "Is this knowledge actually good?"

Quality assessment is essential because a large, fast-growing knowledge base that is full of errors, incoherent inferences, or broken references provides a false sense of capability. These six measures cover quality at each cognitive level -- from the accuracy of extracted facts through the validity of learned procedures and the honesty of self-assessment.

## Measures

### M-047: Fact Correctness Rate

Evaluates the factual accuracy of Y1 extracted facts by comparing them against source documents and, where possible, external references. A random sample of facts is presented to an LLM grader along with the original source material, and the grader determines whether each fact is correctly extracted, distorted, or fabricated.

**Collection**: Sample facts from Y1, pair each with its source document, submit to an LLM evaluator with a structured rubric (correct / partially correct / incorrect / fabricated). Compute the percentage rated as correct.

**Target**: Greater than 95% for production systems. Below 85% indicates extraction pipeline issues requiring investigation.

### M-048: Inference Coherence

Assesses whether Y3 inferred knowledge follows logically from its supporting Y1 facts and Y2 relationships. An LLM grader examines each inference alongside its premises and determines whether the conclusion is logically valid, plausible but unsupported, or contradicted by the evidence.

**Collection**: Sample inferences from Y3, retrieve their provenance chains (the facts and relationships they were derived from), submit to an LLM evaluator. Compute the percentage of inferences rated as logically coherent.

**Target**: Greater than 90%. Incoherent inferences propagate errors upward and undermine trust in the reasoning layer.

### M-049: Procedure Validity

Tests whether Y5 procedural skills actually work when executed. Each procedure is invoked in a controlled environment and its output is evaluated against expected outcomes. This is the most direct test of operational capability.

**Collection**: Execute a sample of procedures from Y5 in a sandboxed environment. An LLM grader or automated test harness evaluates whether each procedure produced the correct output, handled edge cases appropriately, and completed without errors.

**Target**: Greater than 90% for core procedures. Procedures that fail validation should be flagged for retraining or removal.

### M-050: Metacognition Accuracy

Measures how well the system knows itself. Y6 metacognitive records contain claims like "I am confident about topic X" or "I lack knowledge in area Y." This measure checks those claims against independently verified ground truth.

**Collection**: Sample metacognitive assertions from Y6. For capability claims, test the system on relevant tasks. For confidence claims, compare stated confidence against actual accuracy. Compute the percentage of metacognitive claims that match reality.

**Target**: Greater than 80%. Systems with low metacognition accuracy are unreliable self-reporters -- they may claim competence where they lack it or express false uncertainty about strong capabilities.

### M-051: Knowledge Freshness

Measures the recency of the knowledge base by computing what percentage of items have been updated, revalidated, or confirmed within a target time window (e.g., the last 30 days or the last training cycle).

**Collection**: For each knowledge item, check its last-modified or last-validated timestamp against the target window boundary. Compute the percentage of items that fall within the window.

**Target**: Depends on domain volatility. For rapidly changing domains, freshness targets may be 90%+ within 7 days. For stable domains, 80%+ within 90 days may suffice.

### M-052: Cross-Reference Integrity

Checks the structural health of the knowledge graph by verifying that all cross-references between items resolve to valid targets. Broken references indicate knowledge items that have been deleted, moved, or corrupted without updating their dependents.

**Collection**: Traverse all cross-references (edges, provenance links, citations) in the knowledge graph. For each reference, verify that the target item exists and is accessible. Compute the percentage of references that resolve successfully.

**Target**: Greater than 99%. Even small percentages of broken references can cascade into reasoning failures when the system attempts to follow provenance chains.

## ACF Dimension Mapping

Quality measures connect to the ACF dimensions that care most about correctness and trustworthiness:

- **Fact Correctness Rate** directly measures **Factual Grounding** -- are claims tied to verifiable truth?
- **Inference Coherence** reflects **Formal Reasoning** (logical validity) and **Depth** (quality of synthesis).
- **Procedure Validity** maps to **Autonomy** -- can the system reliably execute its learned skills?
- **Metacognition Accuracy** is the core indicator for **Generalization Boundary Awareness** -- does the system accurately know what it knows and does not know?
- **Knowledge Freshness** supports **Breadth** -- stale knowledge effectively reduces coverage.
- **Cross-Reference Integrity** maps to **Knowledge Transparency** -- a system cannot be transparent about its reasoning if its internal references are broken.
