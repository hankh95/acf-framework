---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#DefaultWeights> a acf:WeightConfiguration ;
    acf:label "ACF v1.1 Default Weights" ;
    acf:description "Non-equal weighting across all 10 ACF dimensions per ACF Specification v1.1 Section 3.2." .

<#Weight-Depth> a acf:DimensionWeight ;
    acf:dimension acf:Depth ;
    acf:weight 0.15 ;
    acf:configuration <#DefaultWeights> .

<#Weight-FactualGrounding> a acf:DimensionWeight ;
    acf:dimension acf:FactualGrounding ;
    acf:weight 0.15 ;
    acf:configuration <#DefaultWeights> .

<#Weight-Breadth> a acf:DimensionWeight ;
    acf:dimension acf:Breadth ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-FormalReasoning> a acf:DimensionWeight ;
    acf:dimension acf:FormalReasoning ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-CompositionalGeneralization> a acf:DimensionWeight ;
    acf:dimension acf:CompositionalGeneralization ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-KnowledgeTransparency> a acf:DimensionWeight ;
    acf:dimension acf:KnowledgeTransparency ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-GeneralizationBoundaryAwareness> a acf:DimensionWeight ;
    acf:dimension acf:GeneralizationBoundaryAwareness ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ActionCapability> a acf:DimensionWeight ;
    acf:dimension acf:ActionCapability ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-Autonomy> a acf:DimensionWeight ;
    acf:dimension acf:Autonomy ;
    acf:weight 0.05 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ServiceOrientation> a acf:DimensionWeight ;
    acf:dimension acf:ServiceOrientation ;
    acf:weight 0.05 ;
    acf:configuration <#DefaultWeights> .
---

# Default Dimension Weights (v1.1)

**Configuration:** Non-equal weights per ACF Specification v1.1 Section 3.2

## Overview

The ACF v1.1 aggregate score is computed as the **weighted sum** of all 10 dimension scores. Weights reflect the relative importance of each dimension to overall understanding:

| Dimension | Abbrev | Weight | Rationale |
|-----------|--------|--------|-----------|
| Depth | DP | **0.15** | Core understanding measure |
| Factual Grounding | FG | **0.15** | Prevents hallucination |
| Breadth | BR | 0.10 | Foundation for generalization |
| Formal Reasoning | FR | 0.10 | Critical for professional domains |
| Compositional Generalization | CG | 0.10 | Tests genuine understanding |
| Knowledge Transparency | KT | 0.10 | Enables verification |
| Generalization Boundary Awareness | GBA | 0.10 | Distinguishes narrow vs general AI |
| Action Capability | AC | **0.10** | Bridges knowledge and competence |
| Autonomy | AU | 0.05 | Self-directed learning |
| Service Orientation | SO | 0.05 | Real-world utility |

**Total:** 1.00

## v1.0 to v1.1 Changes

| Change | Detail |
|--------|--------|
| Added Action Capability (AC) | 10th dimension at 10% weight |
| Autonomy reduced | 10% -> 5% |
| Service Orientation reduced | 10% -> 5% |
| Depth increased | 11.1% -> 15% |
| Factual Grounding increased | 11.1% -> 15% |
| All other dimensions adjusted | 11.1% -> 10% |

## When to Customize Weights

The default weights are designed for general-purpose AI evaluation. Domain-specific deployments may benefit from customized weight profiles. Examples:

### Medical Domain

A medical AI system might weight Factual Grounding and Action Capability higher because incorrect facts or failed procedures can cause direct patient harm:

| Dimension | Custom Weight |
|-----------|---------------|
| Factual Grounding | 0.20 |
| Action Capability | 0.15 |
| Depth | 0.12 |
| Generalization Boundary Awareness | 0.10 |
| Knowledge Transparency | 0.10 |
| Formal Reasoning | 0.08 |
| Compositional Generalization | 0.08 |
| Service Orientation | 0.07 |
| Breadth | 0.05 |
| Autonomy | 0.05 |

### Legal Domain

A legal AI system might weight Formal Reasoning and Depth higher because legal reasoning requires rigorous argumentation:

| Dimension | Custom Weight |
|-----------|---------------|
| Formal Reasoning | 0.18 |
| Depth | 0.15 |
| Factual Grounding | 0.12 |
| Compositional Generalization | 0.10 |
| Knowledge Transparency | 0.10 |
| Breadth | 0.10 |
| Service Orientation | 0.08 |
| Generalization Boundary Awareness | 0.07 |
| Action Capability | 0.05 |
| Autonomy | 0.05 |

## Rules for Custom Weights

1. **Weights must sum to 1.0** -- the aggregate score is a proper weighted mean
2. **No dimension may be weighted 0.0** -- every dimension matters; setting any to zero creates blind spots
3. **Minimum weight is 0.02** -- ensures every dimension contributes at least 2% to the aggregate
4. **Weight justification required** -- custom weight profiles must include a written rationale
5. **Custom weights are per-domain** -- the same AI system may have different weight profiles for different domains

## How Weights Affect Certification

Certification is determined by per-dimension thresholds (see `scoring-thresholds.md`), NOT by aggregate score alone. A system must meet ALL dimension thresholds for a given level. Weights affect the aggregate score for reporting purposes, but the gating mechanism is per-dimension.
