---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ScoringMethodology> a acf:ScoringConfiguration ;
    acf:label "ACF Scoring Methodology" ;
    acf:description "Aggregate score is the weighted mean of 9 dimension scores, mapped to certification levels." .

<#Threshold-ACF-1> a acf:ScoringThreshold ;
    acf:level <#ACF-1> ;
    acf:levelId "ACF-1" ;
    acf:levelLabel "Elementary" ;
    acf:scoreMin 0.0 ;
    acf:scoreMax 20.0 ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-2> a acf:ScoringThreshold ;
    acf:level <#ACF-2> ;
    acf:levelId "ACF-2" ;
    acf:levelLabel "Middle School" ;
    acf:scoreMin 20.0 ;
    acf:scoreMax 40.0 ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-3> a acf:ScoringThreshold ;
    acf:level <#ACF-3> ;
    acf:levelId "ACF-3" ;
    acf:levelLabel "High School" ;
    acf:scoreMin 40.0 ;
    acf:scoreMax 60.0 ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-4> a acf:ScoringThreshold ;
    acf:level <#ACF-4> ;
    acf:levelId "ACF-4" ;
    acf:levelLabel "Bachelor's" ;
    acf:scoreMin 60.0 ;
    acf:scoreMax 75.0 ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-5> a acf:ScoringThreshold ;
    acf:level <#ACF-5> ;
    acf:levelId "ACF-5" ;
    acf:levelLabel "Master's" ;
    acf:scoreMin 75.0 ;
    acf:scoreMax 90.0 ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-6> a acf:ScoringThreshold ;
    acf:level <#ACF-6> ;
    acf:levelId "ACF-6" ;
    acf:levelLabel "PhD / Board Certified" ;
    acf:scoreMin 90.0 ;
    acf:scoreMax 100.0 ;
    acf:methodology <#ScoringMethodology> .
---

# Scoring Thresholds

**Configuration:** Certification level boundaries based on aggregate score

## Overview

The ACF certification level is determined by the **aggregate score**, which is the weighted mean of all 9 dimension scores. Each dimension is scored on a 0--100 scale, and the aggregate maps to one of 6 certification levels.

## Threshold Table

| Level | Label | Score Range | Human Equivalent |
|-------|-------|-------------|------------------|
| ACF-1 | Elementary | 0 -- 20 | K-5 elementary education |
| ACF-2 | Middle School | 20 -- 40 | Middle school / GED preparation |
| ACF-3 | High School | 40 -- 60 | High school / undergraduate |
| ACF-4 | Bachelor's | 60 -- 75 | Bachelor's degree / entry professional |
| ACF-5 | Master's | 75 -- 90 | Master's / licensed professional |
| ACF-6 | PhD / Board Certified | 90 -- 100 | PhD / board-certified expert |

## Scoring Methodology

### Step 1: Dimension Scoring

Each of the 9 ACF dimensions is scored independently on a 0--100 continuous scale. Dimension scores are produced by evaluators (human, automated, or hybrid) using the dimension-specific rubrics defined in `knowledge/dimensions/`.

### Step 2: Weight Application

Each dimension score is multiplied by its weight (see `default-weights.md`). By default, all weights are equal (0.111 each), but domain-specific weight profiles may be used.

### Step 3: Aggregate Computation

The aggregate score is computed as:

```
aggregate = sum(dimension_score[i] * weight[i] for i in 1..9)
```

This produces a single number on the 0--100 scale.

### Step 4: Level Assignment

The aggregate score is compared against the threshold table above. **Boundary rule:** a score exactly equal to a boundary value is assigned to the higher level. For example:

- Score 19.9 = ACF-1
- Score 20.0 = ACF-2
- Score 74.9 = ACF-4
- Score 75.0 = ACF-5

### Step 5: Certification

The assigned level, aggregate score, individual dimension scores, and weight profile are recorded in the certification record. The certification is domain-specific: a system may hold different certifications in different domains.

## Non-Uniform Level Widths

The score ranges are intentionally non-uniform:

| Level | Width (points) |
|-------|---------------|
| ACF-1 | 20 |
| ACF-2 | 20 |
| ACF-3 | 20 |
| ACF-4 | 15 |
| ACF-5 | 15 |
| ACF-6 | 10 |

The narrowing at higher levels reflects the increasing difficulty of improvement. The difference between an ACF-5 (75) and ACF-6 (90) system is profound -- it mirrors the gap between a competent professional and a field-defining expert. Fewer points separate these levels because each point of improvement at the top requires disproportionately more capability.

## Dimension Score Independence

Dimension scores are computed independently. A system can score ACF-6 on Factual Grounding but ACF-2 on Metacognitive Awareness. The aggregate smooths these differences, but the per-dimension scores are always available in the certification record for detailed analysis.

## Confidence and Reliability

A single evaluation produces a point estimate. For certification, multiple evaluations should be performed to establish:

- **Mean score** across evaluations
- **Standard deviation** as a measure of reliability
- **Minimum score** to identify worst-case performance

Certification should be based on the mean score, with the standard deviation and minimum reported alongside it. High variance (standard deviation > 5 points) suggests the system's performance is inconsistent and the certification level should be interpreted with caution.
