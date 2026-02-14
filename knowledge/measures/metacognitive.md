---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-030> a acf:Measure ;
    rdfs:label "Self-Assessment Accuracy" ;
    acf:id "M-030" ;
    acf:name "self_assessment_accuracy_pct" ;
    acf:description "Percentage of cases where the system's self-evaluation of its own performance matches an external ground-truth assessment" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "automated" ;
    acf:mapsTo <#GeneralizationBoundary>, <#Autonomy> .

<#M-031> a acf:Measure ;
    rdfs:label "Automated Decisions Ratio" ;
    acf:id "M-031" ;
    acf:name "automated_decisions_ratio_pct" ;
    acf:description "Percentage of decisions made through learned or adaptive logic rather than hardcoded rules or static lookup tables" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy> .

<#M-032> a acf:Measure ;
    rdfs:label "Self-Review Capability" ;
    acf:id "M-032" ;
    acf:name "self_review_capability_pct" ;
    acf:description "Percentage of system outputs that the system can meaningfully evaluate for correctness, completeness, and quality without external feedback" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy>, <#Depth> .

<#M-033> a acf:Measure ;
    rdfs:label "Configuration Adaptability" ;
    acf:id "M-033" ;
    acf:name "configuration_adaptability_pct" ;
    acf:description "Percentage of system configuration parameters that can be dynamically adjusted per context, user, or domain without code changes" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy> .

<#M-034> a acf:Measure ;
    rdfs:label "Metacognitive Awareness Score" ;
    acf:id "M-034" ;
    acf:name "metacognitive_awareness_score_pct" ;
    acf:description "Composite score measuring how accurately the system understands its own capabilities, limitations, knowledge boundaries, and failure modes" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#GeneralizationBoundary> .

<#M-035> a acf:Measure ;
    rdfs:label "Reflection Quality" ;
    acf:id "M-035" ;
    acf:name "reflection_quality_score_pct" ;
    acf:description "Quality of the system's self-reflective analysis, measuring depth of insight, actionability of identified improvements, and accuracy of self-diagnosis" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "metacognitive" ;
    acf:collection "llm-graded" ;
    acf:mapsTo <#Depth>, <#GeneralizationBoundary> .
---

# Metacognitive Measures (M-030 to M-035)

Metacognitive measures assess an AI system's ability to reason about its own reasoning, evaluate its own outputs, understand its own limitations, and adapt its behavior based on self-knowledge. These are the most advanced measures in the ACF framework, capturing capabilities that distinguish truly intelligent systems from sophisticated pattern matchers. Metacognition is the bridge between competent performance and genuine understanding.

## M-030: Self-Assessment Accuracy

**What it measures:** The percentage of cases where the system's self-evaluation of its own performance matches an external ground-truth assessment. A system with high self-assessment accuracy knows when it has performed well and when it has not.

**How to collect:** After the system generates responses, ask it to evaluate its own output on a defined rubric (e.g., correctness, completeness, confidence). Independently evaluate the same outputs using human experts or a validated automated evaluator. Compare the system's self-ratings to the external ratings. Calculate: `(matching_assessments / total_assessments) * 100`, where "matching" is defined as within an acceptable tolerance band (e.g., +/- 1 rubric level).

**Target ranges:**
- Below 40%: System has poor self-awareness; its self-evaluations are unreliable
- 40-60%: Moderate self-awareness; directionally useful but often miscalibrated
- 60-80%: Good self-assessment; the system accurately judges most of its own outputs
- Above 80%: Excellent; system has reliable self-knowledge and can be trusted to flag its own errors

## M-031: Automated Decisions Ratio

**What it measures:** The percentage of decisions the system makes through learned, adaptive, or model-driven logic rather than hardcoded rules, static lookup tables, or fixed conditional logic. This measures how much of the system's behavior emerges from learning versus engineering.

**How to collect:** Audit the system's decision points. Classify each as: (a) hardcoded/static (e.g., if-else rules, lookup tables), (b) parameter-driven (e.g., configurable thresholds), or (c) learned/adaptive (e.g., model predictions, reinforcement-learned policies, dynamically adjusted weights). Calculate: `(learned_decisions / total_decisions) * 100`.

**Target ranges:**
- Below 20%: System is primarily rule-based; limited adaptability
- 20-50%: Mixed system; some decisions are learned, most are engineered
- 50-75%: Primarily learned; system adapts to novel situations
- Above 75%: Highly adaptive; system behavior emerges largely from learning

## M-032: Self-Review Capability

**What it measures:** The percentage of system outputs that the system can meaningfully evaluate for correctness, completeness, and quality on its own, without requiring external feedback or human review. This measures the system's capacity for quality assurance on its own work.

**How to collect:** Present the system with a set of its own outputs (some correct, some containing errors). Ask it to identify errors, rate quality, and suggest improvements. Compare its self-review judgments against expert ground truth. Calculate: `(accurate_self_reviews / total_self_reviews) * 100`.

**Target ranges:**
- Below 30%: System cannot reliably evaluate its own outputs; external review is essential
- 30-55%: Partial self-review capability; catches obvious errors but misses subtleties
- 55-75%: Good self-review; identifies most quality issues in its own outputs
- Above 75%: Strong self-review; can serve as a meaningful quality gate for its own work

## M-033: Configuration Adaptability

**What it measures:** The percentage of the system's configuration parameters (thresholds, weights, strategies, behavioral settings) that can be dynamically adjusted per context, user, or domain without requiring code changes or redeployment.

**How to collect:** Enumerate all configuration parameters that affect system behavior. Classify each as: (a) hardcoded in source code, (b) configurable at deployment time only, (c) dynamically adjustable per context at runtime. Calculate: `(dynamically_adjustable / total_parameters) * 100`.

**Target ranges:**
- Below 20%: System is rigid; behavioral changes require code changes
- 20-50%: Moderate adaptability; some parameters are configurable
- 50-75%: Good adaptability; most behavioral parameters are runtime-adjustable
- Above 75%: Highly adaptable; system behavior can be tuned per-context without engineering effort

## M-034: Metacognitive Awareness Score

**What it measures:** A composite score measuring how accurately the system understands its own capabilities, limitations, knowledge boundaries, and failure modes. This goes beyond confidence calibration (M-009) to assess whether the system has a coherent model of itself.

**How to collect:** Administer a metacognitive evaluation battery consisting of:
1. **Capability boundary questions:** "Can you do X?" where X spans known capabilities, known limitations, and edge cases
2. **Knowledge boundary questions:** "Do you know about Y?" for topics inside and outside its training domain
3. **Failure mode questions:** "In what situations would you fail at Z?" compared against known failure modes

Score each answer for accuracy against ground truth. Calculate the composite score as the weighted average across all three categories. This measure is typically LLM-graded, using an evaluator model to score the system's metacognitive responses against expert-defined ground truth.

**Target ranges:**
- Below 30%: System has minimal self-awareness; overestimates or underestimates its own abilities
- 30-50%: Basic metacognition; system knows some of its limitations but has blind spots
- 50-70%: Good metacognition; system has a reasonably accurate self-model
- Above 70%: Excellent; system demonstrates sophisticated understanding of its own boundaries

## M-035: Reflection Quality

**What it measures:** The quality of the system's self-reflective analysis, including the depth of insight into its own performance, the actionability of its self-identified improvement opportunities, and the accuracy of its self-diagnosis when errors occur.

**How to collect:** After the system completes a set of tasks (including some that it handled poorly), prompt it to reflect on its performance. Evaluate the reflection output on three dimensions:
1. **Insight depth:** Does the reflection identify root causes rather than surface symptoms?
2. **Actionability:** Does the reflection suggest specific, implementable improvements?
3. **Self-diagnosis accuracy:** When the system identifies an error in its own performance, is the diagnosis correct?

Score each dimension on a rubric (e.g., 0-100) and compute the average. This measure is typically LLM-graded, with an evaluator model assessing the reflection output against expert-level analysis.

**Target ranges:**
- Below 25%: Reflections are superficial or inaccurate; no meaningful self-improvement signal
- 25-50%: Some useful insights; reflections identify obvious issues but lack depth
- 50-70%: Good reflections; system demonstrates genuine analytical capability about its own performance
- Above 70%: Excellent; reflections rival expert-level performance analysis and suggest actionable improvements
