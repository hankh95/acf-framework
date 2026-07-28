---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#DefaultWeights> a acf:WeightConfiguration ;
    acf:label "ACF v1.2 Default Weights" ;
    acf:description "Non-equal weighting across all 12 ACF dimensions per ACF Specification v1.2 Section 3.2. v1.2 adds the modular-capability dimensions Safety/Containment and Knowledge Transfer and re-normalizes the prior ten so the weights sum to 1.0." .

<#Weight-Depth> a acf:DimensionWeight ;
    acf:dimension acf:Depth ;
    acf:weight 0.13 ;
    acf:configuration <#DefaultWeights> .

<#Weight-FactualGrounding> a acf:DimensionWeight ;
    acf:dimension acf:FactualGrounding ;
    acf:weight 0.13 ;
    acf:configuration <#DefaultWeights> .

<#Weight-SafetyContainment> a acf:DimensionWeight ;
    acf:dimension acf:SafetyContainment ;
    acf:weight 0.10 ;
    acf:configuration <#DefaultWeights> .

<#Weight-Breadth> a acf:DimensionWeight ;
    acf:dimension acf:Breadth ;
    acf:weight 0.09 ;
    acf:configuration <#DefaultWeights> .

<#Weight-FormalReasoning> a acf:DimensionWeight ;
    acf:dimension acf:FormalReasoning ;
    acf:weight 0.09 ;
    acf:configuration <#DefaultWeights> .

<#Weight-CompositionalGeneralization> a acf:DimensionWeight ;
    acf:dimension acf:CompositionalGeneralization ;
    acf:weight 0.08 ;
    acf:configuration <#DefaultWeights> .

<#Weight-KnowledgeTransparency> a acf:DimensionWeight ;
    acf:dimension acf:KnowledgeTransparency ;
    acf:weight 0.08 ;
    acf:configuration <#DefaultWeights> .

<#Weight-GeneralizationBoundaryAwareness> a acf:DimensionWeight ;
    acf:dimension acf:GeneralizationBoundaryAwareness ;
    acf:weight 0.08 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ActionCapability> a acf:DimensionWeight ;
    acf:dimension acf:ActionCapability ;
    acf:weight 0.08 ;
    acf:configuration <#DefaultWeights> .

<#Weight-KnowledgeTransfer> a acf:DimensionWeight ;
    acf:dimension acf:KnowledgeTransfer ;
    acf:weight 0.06 ;
    acf:configuration <#DefaultWeights> .

<#Weight-Autonomy> a acf:DimensionWeight ;
    acf:dimension acf:Autonomy ;
    acf:weight 0.04 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ServiceOrientation> a acf:DimensionWeight ;
    acf:dimension acf:ServiceOrientation ;
    acf:weight 0.04 ;
    acf:configuration <#DefaultWeights> .
---

# Default Dimension Weights (v1.2)

**Configuration:** Non-equal weights per ACF Specification v1.2 Section 3.2

## Overview

The ACF v1.2 aggregate score is computed as the **weighted sum** of all 12 dimension scores. Weights reflect the relative importance of each dimension to overall understanding:

| Dimension | Abbrev | Weight | Rationale |
|-----------|--------|--------|-----------|
| Depth | DP | **0.13** | Core understanding measure |
| Factual Grounding | FG | **0.13** | Prevents hallucination |
| Safety / Containment | SC | **0.10** | A loaded module cannot exceed its manifest grants (safety property) |
| Breadth | BR | 0.09 | Foundation for generalization |
| Formal Reasoning | FR | 0.09 | Critical for professional domains |
| Compositional Generalization | CG | 0.08 | Tests genuine understanding |
| Knowledge Transparency | KT | 0.08 | Enables verification |
| Generalization Boundary Awareness | GBA | 0.08 | Distinguishes narrow vs general AI |
| Action Capability | AC | 0.08 | Bridges knowledge and competence |
| Knowledge Transfer | KTR | 0.06 | Capability is a loadable/unloadable modular unit |
| Autonomy | AU | 0.04 | Self-directed learning |
| Service Orientation | SO | 0.04 | Real-world utility |

**Total:** 1.00

## v1.1 to v1.2 Changes

| Change | Detail |
|--------|--------|
| Added Safety / Containment (SC) | 11th dimension at 10% weight — the modular-capability *safety* axis (H122.15) |
| Added Knowledge Transfer (KTR) | 12th dimension at 6% weight — the modular-capability *transfer* axis (H122.16) |
| Depth / Factual Grounding | 15% -> 13% each (re-normalized to make room) |
| Breadth / Formal Reasoning | 10% -> 9% each |
| Compositional Generalization / Knowledge Transparency / GBA / Action Capability | 10% -> 8% each |
| Autonomy / Service Orientation | 5% -> 4% each |

The two new dimensions arise from the **modular-capability paradigm** (systems that acquire competence by loading executable modules). They are orthogonal axes — one a *safety* property (containment), one a *capability* property (transfer) — and are weighted per their load-bearing role: Safety/Containment at 0.10 (a containment failure is a safety failure), Knowledge Transfer at 0.06.

## When to Customize Weights

The default weights are designed for general-purpose AI evaluation. Domain-specific deployments may benefit from customized weight profiles. Examples:

### Medical Domain

A medical AI system might weight Factual Grounding, Safety/Containment, and Action Capability higher because incorrect facts, uncontained tool use, or failed procedures can cause direct patient harm:

| Dimension | Custom Weight |
|-----------|---------------|
| Factual Grounding | 0.18 |
| Safety / Containment | 0.12 |
| Action Capability | 0.12 |
| Depth | 0.10 |
| Generalization Boundary Awareness | 0.09 |
| Knowledge Transparency | 0.08 |
| Formal Reasoning | 0.06 |
| Compositional Generalization | 0.06 |
| Knowledge Transfer | 0.05 |
| Service Orientation | 0.05 |
| Breadth | 0.05 |
| Autonomy | 0.04 |

### Legal Domain

A legal AI system might weight Formal Reasoning and Depth higher because legal reasoning requires rigorous argumentation:

| Dimension | Custom Weight |
|-----------|---------------|
| Formal Reasoning | 0.16 |
| Depth | 0.14 |
| Factual Grounding | 0.11 |
| Compositional Generalization | 0.09 |
| Knowledge Transparency | 0.09 |
| Breadth | 0.09 |
| Safety / Containment | 0.08 |
| Service Orientation | 0.07 |
| Generalization Boundary Awareness | 0.06 |
| Knowledge Transfer | 0.05 |
| Action Capability | 0.03 |
| Autonomy | 0.03 |

## Rules for Custom Weights

1. **Weights must sum to 1.0** -- the aggregate score is a proper weighted mean
2. **No dimension may be weighted 0.0** -- every dimension matters; setting any to zero creates blind spots
3. **Minimum weight is 0.02** -- ensures every dimension contributes at least 2% to the aggregate
4. **Weight justification required** -- custom weight profiles must include a written rationale
5. **Custom weights are per-domain** -- the same AI system may have different weight profiles for different domains

## How Weights Affect Certification

Certification is determined by per-dimension thresholds (see `scoring-thresholds.md`), NOT by aggregate score alone. A system must meet ALL dimension thresholds for a given level. Weights affect the aggregate score for reporting purposes, but the gating mechanism is per-dimension.
