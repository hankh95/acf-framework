---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#DefaultWeights> a acf:WeightConfiguration ;
    acf:label "Default Equal Weights" ;
    acf:description "Equal weighting across all 9 ACF dimensions (1/9 each)." .

<#Weight-FactualGrounding> a acf:DimensionWeight ;
    acf:dimension acf:FactualGrounding ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ReasoningDepth> a acf:DimensionWeight ;
    acf:dimension acf:ReasoningDepth ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ContextualAdaptation> a acf:DimensionWeight ;
    acf:dimension acf:ContextualAdaptation ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-SafetyEthicalAlignment> a acf:DimensionWeight ;
    acf:dimension acf:SafetyEthicalAlignment ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-CommunicationClarity> a acf:DimensionWeight ;
    acf:dimension acf:CommunicationClarity ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-UncertaintyCalibration> a acf:DimensionWeight ;
    acf:dimension acf:UncertaintyCalibration ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-ToolResourceUtilization> a acf:DimensionWeight ;
    acf:dimension acf:ToolResourceUtilization ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-LearningAdaptability> a acf:DimensionWeight ;
    acf:dimension acf:LearningAdaptability ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .

<#Weight-MetacognitiveAwareness> a acf:DimensionWeight ;
    acf:dimension acf:MetacognitiveAwareness ;
    acf:weight 0.111 ;
    acf:configuration <#DefaultWeights> .
---

# Default Dimension Weights

**Configuration:** Equal weights (1/9 = 0.111 per dimension)

## Overview

The ACF aggregate score is computed as the **weighted mean** of all 9 dimension scores. By default, each dimension contributes equally:

| Dimension | Weight |
|-----------|--------|
| Factual Grounding | 0.111 |
| Reasoning Depth | 0.111 |
| Contextual Adaptation | 0.111 |
| Safety & Ethical Alignment | 0.111 |
| Communication Clarity | 0.111 |
| Uncertainty Calibration | 0.111 |
| Tool & Resource Utilization | 0.111 |
| Learning & Adaptability | 0.111 |
| Metacognitive Awareness | 0.111 |

**Total:** 1.0 (0.111 x 9 = 0.999, with rounding)

## When to Customize Weights

Equal weighting is the default because it makes no assumptions about which dimensions are more important. However, domain-specific deployments often benefit from customized weight profiles. Examples:

### Medical Domain

A medical AI system might weight **Factual Grounding** and **Safety & Ethical Alignment** higher because incorrect facts or unsafe recommendations can cause direct patient harm:

| Dimension | Custom Weight |
|-----------|---------------|
| Factual Grounding | 0.20 |
| Safety & Ethical Alignment | 0.20 |
| Uncertainty Calibration | 0.15 |
| Reasoning Depth | 0.12 |
| Communication Clarity | 0.10 |
| Contextual Adaptation | 0.08 |
| Tool & Resource Utilization | 0.05 |
| Learning & Adaptability | 0.05 |
| Metacognitive Awareness | 0.05 |

### Legal Domain

A legal AI system might weight **Reasoning Depth** and **Communication Clarity** higher because legal reasoning requires rigorous argumentation and precise language:

| Dimension | Custom Weight |
|-----------|---------------|
| Reasoning Depth | 0.18 |
| Communication Clarity | 0.18 |
| Factual Grounding | 0.15 |
| Contextual Adaptation | 0.12 |
| Safety & Ethical Alignment | 0.12 |
| Uncertainty Calibration | 0.10 |
| Metacognitive Awareness | 0.05 |
| Tool & Resource Utilization | 0.05 |
| Learning & Adaptability | 0.05 |

### Creative Domain

A creative writing AI system might weight **Contextual Adaptation** and **Communication Clarity** higher:

| Dimension | Custom Weight |
|-----------|---------------|
| Contextual Adaptation | 0.20 |
| Communication Clarity | 0.20 |
| Learning & Adaptability | 0.15 |
| Metacognitive Awareness | 0.10 |
| Reasoning Depth | 0.10 |
| Factual Grounding | 0.08 |
| Uncertainty Calibration | 0.07 |
| Safety & Ethical Alignment | 0.05 |
| Tool & Resource Utilization | 0.05 |

## Rules for Custom Weights

1. **Weights must sum to 1.0** -- the aggregate score is a proper weighted mean
2. **No dimension may be weighted 0.0** -- every dimension matters; setting any to zero creates blind spots
3. **Minimum weight is 0.02** -- ensures every dimension contributes at least 2% to the aggregate
4. **Weight justification required** -- custom weight profiles must include a written rationale explaining why each dimension is weighted as it is
5. **Custom weights are per-domain** -- the same AI system may have different weight profiles for different certification domains

## How Weights Affect Certification

The aggregate score determines the certification level (see `scoring-thresholds.md`). Because weights change the aggregate, the same system can achieve different certification levels under different weight profiles. This is by design: a system that is ACF-5 in general medicine might only be ACF-3 in radiology if the radiology weight profile emphasizes dimensions where it is weaker.
