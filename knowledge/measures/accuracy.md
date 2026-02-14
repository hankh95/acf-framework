---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-001> a acf:Measure ;
    rdfs:label "Routing Agreement %" ;
    acf:id "M-001" ;
    acf:name "routing_agreement_pct" ;
    acf:description "Percentage of incoming queries where the system's routing decision matches the expected correct handler or processing path" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-002> a acf:Measure ;
    rdfs:label "Routing Accuracy %" ;
    acf:id "M-002" ;
    acf:name "routing_accuracy_pct" ;
    acf:description "Percentage of queries routed to the correct processing path, measured against a ground-truth labeled evaluation set" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FormalReasoning> .

<#M-003> a acf:Measure ;
    rdfs:label "Hallucination Rate" ;
    acf:id "M-003" ;
    acf:name "hallucination_rate_pct" ;
    acf:description "Percentage of factual claims not grounded in the system's knowledge base" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FactualGrounding> .

<#M-004> a acf:Measure ;
    rdfs:label "Evidence Coverage %" ;
    acf:id "M-004" ;
    acf:name "evidence_coverage_pct" ;
    acf:description "Percentage of system responses that include a complete evidence trail linking claims to source documents" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#KnowledgeTransparency> .

<#M-005> a acf:Measure ;
    rdfs:label "Provenance Attribution" ;
    acf:id "M-005" ;
    acf:name "provenance_attribution_pct" ;
    acf:description "Percentage of factual claims attributed to a specific source document or knowledge base entry" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FactualGrounding>, <#KnowledgeTransparency> .

<#M-006> a acf:Measure ;
    rdfs:label "Semantic Search Accuracy" ;
    acf:id "M-006" ;
    acf:name "semantic_search_accuracy_pct" ;
    acf:description "Percentage of semantic search queries that return the most relevant results within the top-k results, measured by precision@k or MRR" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FactualGrounding> .

<#M-007> a acf:Measure ;
    rdfs:label "Pipeline Test Pass Rate" ;
    acf:id "M-007" ;
    acf:name "pipeline_test_pass_rate_pct" ;
    acf:description "Percentage of automated pipeline tests that pass, verifying architectural correctness across ingestion, reasoning, and response generation stages" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FormalReasoning> .

<#M-008> a acf:Measure ;
    rdfs:label "Base Coverage %" ;
    acf:id "M-008" ;
    acf:name "base_coverage_pct" ;
    acf:description "Percentage of queries answerable from the system's base knowledge without requiring external retrieval or fallback to a general-purpose language model" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .

<#M-009> a acf:Measure ;
    rdfs:label "Expected Calibration Error" ;
    acf:id "M-009" ;
    acf:name "expected_calibration_error" ;
    acf:description "Measures the gap between the system's stated confidence and its actual accuracy, averaged across confidence bins" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#FactualGrounding>, <#GeneralizationBoundary> .

<#M-010> a acf:Measure ;
    rdfs:label "Strategy Selection Optimality" ;
    acf:id "M-010" ;
    acf:name "strategy_selection_optimality_pct" ;
    acf:description "Percentage of cases where the system selects the optimal reasoning or response strategy, as judged against expert-labeled ground truth" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "accuracy" ;
    acf:collection "automated" ;
    acf:mapsTo <#GeneralizationBoundary> .
---

# Accuracy Measures (M-001 to M-010)

Accuracy measures quantify how correctly and reliably an AI system performs its core functions: routing queries, grounding claims in evidence, retrieving relevant knowledge, and selecting appropriate strategies. These measures form the foundation of system evaluation because accuracy failures propagate through all downstream capabilities.

## M-001: Routing Agreement %

**What it measures:** The percentage of incoming queries where the system's routing decision agrees with the expected correct handler or processing path.

**How to collect:** Run a labeled evaluation set of queries through the system's router. Compare each routing decision against the ground-truth label. Calculate: `(agreements / total_queries) * 100`.

**Target ranges:**
- Below 70%: Significant routing confusion; many queries reach the wrong handler
- 70-85%: Acceptable for early-stage systems with limited routing complexity
- 85-95%: Good routing performance; most queries reach the correct handler
- Above 95%: Excellent; near-human routing accuracy

## M-002: Routing Accuracy %

**What it measures:** The percentage of queries routed to the correct processing path, measured against a ground-truth labeled evaluation set. While M-001 measures agreement (can include ties or partial matches), M-002 measures strict correctness.

**How to collect:** Use a curated evaluation set with definitive correct paths. Score each routing decision as correct or incorrect with no partial credit. Calculate: `(correct / total) * 100`.

**Target ranges:**
- Below 65%: Routing logic needs fundamental redesign
- 65-80%: Adequate for prototype systems
- 80-92%: Production-ready for most use cases
- Above 92%: High-confidence routing suitable for critical applications

## M-003: Hallucination Rate

**What it measures:** The percentage of factual claims in system responses that are not grounded in the system's knowledge base. A hallucination is any assertion presented as fact that cannot be traced to a source document or verified triple in the knowledge graph.

**How to collect:** Sample system responses and extract all factual claims. For each claim, attempt to find a supporting source in the knowledge base. Calculate: `(unsupported_claims / total_claims) * 100`. This can be automated using an LLM-based claim extraction and verification pipeline.

**Target ranges:**
- Above 10%: Unacceptable for production; system cannot be trusted for factual queries
- 5-10%: Early-stage system with known grounding gaps
- 1-5%: Good performance; occasional hallucinations in edge cases
- Below 1%: Excellent; suitable for high-stakes domains

## M-004: Evidence Coverage %

**What it measures:** The percentage of system responses that include a complete evidence trail linking each factual claim to its source document or knowledge base entry.

**How to collect:** For each response, check whether every factual claim includes a citation or evidence link. Calculate: `(responses_with_full_evidence / total_responses) * 100`. Partial evidence (some claims cited, others not) counts as incomplete.

**Target ranges:**
- Below 50%: Most responses lack evidence trails
- 50-75%: Partial evidence coverage; improvement needed for transparency
- 75-90%: Good coverage; most responses are fully traceable
- Above 90%: Excellent transparency; nearly all claims are auditable

## M-005: Provenance Attribution

**What it measures:** The percentage of factual claims attributed to a specific source document or knowledge base entry. Unlike M-004 (which scores at the response level), M-005 scores at the individual claim level.

**How to collect:** Extract all factual claims from a sample of system responses. For each claim, check if it carries a provenance annotation pointing to a specific source. Calculate: `(attributed_claims / total_claims) * 100`.

**Target ranges:**
- Below 40%: Most claims are unattributed
- 40-70%: Moderate attribution; useful but not sufficient for audit
- 70-90%: Good provenance; most claims are traceable
- Above 90%: Excellent; supports full knowledge auditing

## M-006: Semantic Search Accuracy

**What it measures:** The accuracy of the system's semantic search capability, typically measured as precision@k (proportion of top-k results that are relevant) or Mean Reciprocal Rank (MRR).

**How to collect:** Prepare a labeled retrieval evaluation set with queries and known relevant documents. Run each query through the semantic search pipeline. Measure precision@k (typically k=5 or k=10) and MRR. Report the average across all evaluation queries.

**Target ranges:**
- Below 50% precision@5: Retrieval is noisy; system returns too many irrelevant results
- 50-70%: Acceptable for broad-domain systems
- 70-85%: Good retrieval quality for most applications
- Above 85%: Excellent; retrieval rarely misses relevant content

## M-007: Pipeline Test Pass Rate

**What it measures:** The percentage of automated tests covering the system's processing pipeline (ingestion, transformation, reasoning, response generation) that pass. This is a proxy for architectural correctness and regression prevention.

**How to collect:** Run the full automated test suite. Calculate: `(passing_tests / total_tests) * 100`. Track over time to detect regressions.

**Target ranges:**
- Below 80%: Active regressions; system integrity is compromised
- 80-95%: Some known failures; acceptable during active development
- 95-99%: Good health; only edge-case failures remain
- 100%: Ideal; all pipeline stages are verified

## M-008: Base Coverage %

**What it measures:** The percentage of user queries that the system can answer from its base knowledge without falling back to external retrieval, a general-purpose language model, or a "sorry, I don't know" response.

**How to collect:** Run a representative sample of expected queries. Classify each response as "answered from base knowledge" or "required fallback." Calculate: `(base_answered / total_queries) * 100`.

**Target ranges:**
- Below 30%: System has significant knowledge gaps for its intended domain
- 30-60%: Partial coverage; adequate for learning-phase systems
- 60-85%: Good domain coverage
- Above 85%: Comprehensive; system handles the vast majority of in-domain queries

## M-009: Expected Calibration Error

**What it measures:** The gap between stated confidence and actual accuracy. A well-calibrated system that says it is 80% confident should be correct about 80% of the time. ECE is the weighted average of `|accuracy - confidence|` across confidence bins.

**How to collect:** Collect a large sample of system predictions with confidence scores. Bin predictions by confidence level (e.g., 0-10%, 10-20%, ..., 90-100%). For each bin, compute the absolute difference between average confidence and actual accuracy. Weight by bin size and sum. Lower is better.

**Target ranges:**
- Above 15%: Poorly calibrated; confidence scores are unreliable
- 10-15%: Moderate calibration; confidence is directionally useful but imprecise
- 5-10%: Good calibration; confidence scores are meaningfully informative
- Below 5%: Excellent calibration; stated confidence closely matches actual accuracy

## M-010: Strategy Selection Optimality

**What it measures:** The percentage of cases where the system selects the optimal reasoning or response strategy from its available options. For example, choosing to retrieve from the knowledge graph vs. performing multi-step reasoning vs. asking a clarifying question.

**How to collect:** Create an evaluation set with ground-truth optimal strategy labels (determined by domain experts). Run each case through the system's strategy selector. Calculate: `(optimal_selections / total_cases) * 100`.

**Target ranges:**
- Below 50%: Strategy selection is near-random; system needs better decision logic
- 50-70%: Some strategic awareness; often picks a reasonable but suboptimal path
- 70-85%: Good strategic selection for most query types
- Above 85%: Excellent; system consistently identifies the best approach
