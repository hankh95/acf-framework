---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-026> a acf:Measure ;
    rdfs:label "Decision Quality" ;
    acf:id "M-026" ;
    acf:name "decision_quality_pct" ;
    acf:description "Percentage of system decisions that are correct or optimal when evaluated against ground-truth outcomes, particularly in scenarios involving uncertainty or incomplete information" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "quality" ;
    acf:collection "automated" ;
    acf:mapsTo <#GeneralizationBoundary> .

<#M-027> a acf:Measure ;
    rdfs:label "Mistake Recurrence Rate" ;
    acf:id "M-027" ;
    acf:name "mistake_recurrence_rate_pct" ;
    acf:description "Percentage of previously identified errors that recur after corrective action has been taken, measuring the system's ability to learn from mistakes" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "quality" ;
    acf:collection "automated" ;
    acf:mapsTo <#Depth>, <#Autonomy> .

<#M-028> a acf:Measure ;
    rdfs:label "Task Autonomy Level" ;
    acf:id "M-028" ;
    acf:name "task_autonomy_level_pct" ;
    acf:description "Percentage of tasks completed without human intervention, escalation, or manual correction" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "quality" ;
    acf:collection "manual" ;
    acf:mapsTo <#Autonomy> .

<#M-029> a acf:Measure ;
    rdfs:label "Error Pattern Detection" ;
    acf:id "M-029" ;
    acf:name "error_pattern_detection_pct" ;
    acf:description "Percentage of systematic error patterns that the system identifies and flags before they cause repeated failures" ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "quality" ;
    acf:collection "automated" ;
    acf:mapsTo <#GeneralizationBoundary>, <#Depth> .
---

# Quality Measures (M-026 to M-029)

Quality measures assess the caliber of an AI system's decision-making, its ability to learn from errors, and its capacity for autonomous operation. Unlike accuracy measures (which assess correctness on well-defined tasks), quality measures evaluate the system's performance in ambiguous, uncertain, or evolving situations where there is no single obvious right answer.

## M-026: Decision Quality

**What it measures:** The percentage of decisions made by the system that are judged correct or optimal when evaluated against ground-truth outcomes. This is especially meaningful for decisions made under uncertainty, where the system must weigh incomplete evidence and choose among imperfect options.

**How to collect:** Create an evaluation set of decision scenarios with known optimal outcomes (established retrospectively or by expert consensus). Run each scenario through the system's decision pipeline. Compare the system's decision to the known-optimal decision. Calculate: `(optimal_decisions / total_decisions) * 100`. For nuanced evaluation, use a graded rubric (e.g., optimal, acceptable, suboptimal, wrong) rather than binary scoring.

**Target ranges:**
- Below 50%: Decision-making is unreliable; system should not be trusted for autonomous decisions
- 50-70%: Moderate quality; acceptable for low-stakes decisions with human oversight
- 70-85%: Good quality; suitable for most operational decisions
- Above 85%: Excellent; system makes high-quality decisions consistently under uncertainty

## M-027: Mistake Recurrence Rate

**What it measures:** The percentage of previously identified and corrected errors that recur in subsequent system operation. A low recurrence rate indicates the system effectively learns from its mistakes and does not repeat them. A high recurrence rate suggests corrective actions are superficial or the system lacks the ability to generalize corrections.

**How to collect:** Maintain a log of identified errors with timestamps and corrective actions. After each corrective action, monitor for recurrence of the same error pattern over a defined follow-up period. Calculate: `(recurring_errors / total_corrected_errors) * 100`. Lower is better.

**Target ranges:**
- Above 30%: System fails to learn from mistakes; corrections are ineffective
- 15-30%: Some learning occurs, but many error patterns persist
- 5-15%: Good error learning; most corrections stick
- Below 5%: Excellent; system rarely repeats a corrected mistake

## M-028: Task Autonomy Level

**What it measures:** The percentage of tasks the system completes entirely without human intervention, escalation, or post-hoc manual correction. This measures real-world autonomous capability, not just theoretical competence.

**How to collect:** Over a measurement period, track all tasks assigned to the system. Classify each task outcome as: (a) completed autonomously, (b) required human escalation, (c) completed by system but required human correction, or (d) failed and required human takeover. Calculate: `(autonomously_completed / total_tasks) * 100`. This measure requires manual tracking because determining whether human intervention was truly needed involves judgment.

**Target ranges:**
- Below 30%: System requires heavy human supervision; limited autonomous value
- 30-60%: Partial autonomy; handles routine tasks but escalates complex ones
- 60-85%: Good autonomy; handles most tasks independently
- Above 85%: High autonomy; human intervention is rare and limited to edge cases

## M-029: Error Pattern Detection

**What it measures:** The percentage of systematic error patterns (recurring failure modes, consistent biases, degradation trends) that the system identifies and flags before they cause repeated failures. This measures proactive error awareness rather than reactive correction.

**How to collect:** Introduce known error patterns into the system's operational data or evaluation set. Monitor whether the system detects and reports these patterns. Also track organically occurring error patterns and whether the system identifies them before a human does. Calculate: `(detected_patterns / total_patterns) * 100`.

**Target ranges:**
- Below 20%: System is blind to its own systematic errors
- 20-50%: Some error awareness; detects obvious patterns but misses subtle ones
- 50-75%: Good detection; identifies most systematic failure modes
- Above 75%: Excellent; system proactively identifies and reports error trends
