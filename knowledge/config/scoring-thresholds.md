---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ScoringMethodology> a acf:ScoringConfiguration ;
    acf:label "ACF v1.1 Scoring Methodology" ;
    acf:description "Certification level is determined by per-dimension gating: ALL dimensions must meet their thresholds for a given level. Aggregate score is the weighted sum per v1.1 weights." .

<#Threshold-ACF-1> a acf:ScoringThreshold ;
    acf:level <#ACF-1> ;
    acf:levelId "ACF-1" ;
    acf:levelLabel "Elementary" ;
    acf:humanEquivalent "K-5 Education" ;
    acf:dimensionThresholds "breadth>=30, depth>=30, formal_reasoning>=40, factual_grounding>=50, compositional_generalization>=40, knowledge_transparency>=30, service_orientation>=30, gba>=30, autonomy>=30, action_capability>=15" ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-2> a acf:ScoringThreshold ;
    acf:level <#ACF-2> ;
    acf:levelId "ACF-2" ;
    acf:levelLabel "Secondary" ;
    acf:humanEquivalent "High School / GED" ;
    acf:dimensionThresholds "breadth>=50, depth>=40, formal_reasoning>=50, factual_grounding>=60, compositional_generalization>=50, knowledge_transparency>=50, service_orientation>=40, gba>=40, autonomy>=40, action_capability>=30" ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-3> a acf:ScoringThreshold ;
    acf:level <#ACF-3> ;
    acf:levelId "ACF-3" ;
    acf:levelLabel "Undergraduate" ;
    acf:humanEquivalent "Bachelor's Degree" ;
    acf:dimensionThresholds "breadth>=70, depth>=50, formal_reasoning>=60, factual_grounding>=70, compositional_generalization>=60, knowledge_transparency>=50, service_orientation>=50, gba>=50, autonomy>=50, action_capability>=50" ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-4> a acf:ScoringThreshold ;
    acf:level <#ACF-4> ;
    acf:levelId "ACF-4" ;
    acf:levelLabel "Graduate" ;
    acf:humanEquivalent "Master's Degree" ;
    acf:dimensionThresholds "breadth>=75, depth>=60, formal_reasoning>=70, factual_grounding>=75, compositional_generalization>=60, knowledge_transparency>=60, service_orientation>=60, gba>=60, autonomy>=60, action_capability>=60" ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-5> a acf:ScoringThreshold ;
    acf:level <#ACF-5> ;
    acf:levelId "ACF-5" ;
    acf:levelLabel "Professional" ;
    acf:humanEquivalent "Bar/USMLE/PE/CFA" ;
    acf:dimensionThresholds "breadth>=80, depth>=70, formal_reasoning>=75, factual_grounding>=80, compositional_generalization>=70, knowledge_transparency>=70, service_orientation>=70, gba>=65, autonomy>=65, action_capability>=65" ;
    acf:methodology <#ScoringMethodology> .

<#Threshold-ACF-6> a acf:ScoringThreshold ;
    acf:level <#ACF-6> ;
    acf:levelId "ACF-6" ;
    acf:levelLabel "Expert" ;
    acf:humanEquivalent "PhD / Board Certified" ;
    acf:dimensionThresholds "breadth>=90, depth>=80, formal_reasoning>=80, factual_grounding>=85, compositional_generalization>=75, knowledge_transparency>=80, service_orientation>=80, gba>=75, autonomy>=70, action_capability>=75" ;
    acf:methodology <#ScoringMethodology> .
---

# Scoring Thresholds (v1.1)

**Configuration:** Per-dimension gating per ACF Specification v1.1 Section 14.2

## Overview

ACF v1.1 certification is determined by **per-dimension gating**: a system must meet ALL dimension thresholds for a given level. The lowest qualifying dimension determines the certification level. The aggregate score (weighted sum) is reported for informational purposes but does not gate certification.

## Dimension Requirements by Level

| Level | Label | BR | DP | FR | FG | CG | KT | SO | GBA | AU | AC |
|-------|-------|-----|-----|-----|-----|-----|-----|-----|------|-----|-----|
| **ACF-1** | Elementary | 30 | 30 | 40 | 50 | 40 | 30 | 30 | 30 | 30 | 15 |
| **ACF-2** | Secondary | 50 | 40 | 50 | 60 | 50 | 50 | 40 | 40 | 40 | 30 |
| **ACF-3** | Undergraduate | 70 | 50 | 60 | 70 | 60 | 50 | 50 | 50 | 50 | 50 |
| **ACF-4** | Graduate | 75 | 60 | 70 | 75 | 60 | 60 | 60 | 60 | 60 | 60 |
| **ACF-5** | Professional | 80 | 70 | 75 | 80 | 70 | 70 | 70 | 65 | 65 | 65 |
| **ACF-6** | Expert | 90 | 80 | 80 | 85 | 75 | 80 | 80 | 75 | 70 | 75 |

**Critical (v1.1):** ACF-3+ requires AC >= 50 (AC2 level). A system that cannot execute known procedures on novel inputs cannot receive undergraduate-level certification. ACF-5+ requires AC >= 65 (AC3 level) — professionals must adapt procedures.

## Scoring Methodology

### Step 1: Dimension Scoring

Each of the 10 ACF dimensions is scored independently on a 0-100 continuous scale. Dimension scores are produced by evaluators (human, automated, or hybrid) using the dimension-specific rubrics defined in `knowledge/dimensions/`.

### Step 2: Weighted Aggregate

Each dimension score is multiplied by its v1.1 weight (see `default-weights.md`):

```
aggregate = sum(dimension_score[i] * weight[i] for i in 1..10)
```

This produces a single number on the 0-100 scale.

### Step 3: Per-Dimension Certification Gating

The certification level is the highest level where ALL dimension scores meet or exceed their thresholds:

```python
for level in [ACF-6, ACF-5, ACF-4, ACF-3, ACF-2, ACF-1]:
    if all(score[dim] >= threshold[level][dim] for dim in 10 dimensions):
        return level
return ACF-0  # Below ACF-1
```

### Step 4: Certification

The assigned level, aggregate score, individual dimension scores, and weight profile are recorded in the certification record.

## v1.0 to v1.1 Changes

| Change | Detail |
|--------|--------|
| Per-dimension gating | Certification no longer uses aggregate score thresholds |
| AC column added | All 6 levels have Action Capability requirements |
| ACF-1 AC threshold | 15 (AC1 minimum) |
| ACF-3 AC threshold | 50 (AC2 required for undergraduate) |
| ACF-5 AC threshold | 65 (AC3 required for professional) |
| ACF-5+ requires GBA3+ | Prevents narrow expert systems |
| ACF-5+ requires AU3+ | Prevents purely reactive systems |

## Why Per-Dimension Gating

The v1.0 approach used aggregate score thresholds (>= 90 = ACF-6). This allowed systems with extreme dimension imbalance to achieve high certification — a system with 100 on every dimension except GBA (20) could still reach ACF-4 or higher. Per-dimension gating ensures balanced capability across all dimensions, matching how human professional certification works: you must pass every section, not just achieve a high average.

## Confidence and Reliability

A single evaluation produces a point estimate. For certification, multiple evaluations should be performed to establish:

- **Mean score** across evaluations
- **Standard deviation** as a measure of reliability
- **Minimum score** to identify worst-case performance

Certification should be based on the mean score, with the standard deviation and minimum reported alongside it. High variance (standard deviation > 5 points) suggests the system's performance is inconsistent.
