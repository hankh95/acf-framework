---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-044> a acf:Measure ;
    rdfs:label "Knowledge Enrichment Rate" ;
    acf:id "M-044" ;
    acf:name "enrichment_rate" ;
    acf:description "Rate at which new knowledge items are added across all layers, measured in items per hour. Captures the velocity of knowledge acquisition and synthesis during active learning cycles." ;
    acf:unit "items_per_hour" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-growth" ;
    acf:collection "automated" ;
    acf:mapsTo <#Depth>, <#Autonomy> .

<#M-045> a acf:Measure ;
    rdfs:label "Knowledge Confidence Score" ;
    acf:id "M-045" ;
    acf:name "confidence_score" ;
    acf:description "Average confidence score across all knowledge items in the system, normalized to a 0-1 scale. Reflects the overall epistemic reliability of the knowledge base as assessed by the system's own confidence estimation mechanisms." ;
    acf:unit "score_0_1" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-growth" ;
    acf:collection "automated" ;
    acf:mapsTo <#FactualGrounding>, <#GeneralizationBoundary> .

<#M-046> a acf:Measure ;
    rdfs:label "Knowledge Diversity Index" ;
    acf:id "M-046" ;
    acf:name "diversity_index" ;
    acf:description "Shannon diversity index computed over the distribution of knowledge items across categories, domains, or topics. Higher values indicate more evenly distributed knowledge rather than concentration in a few areas." ;
    acf:unit "score" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-growth" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth>, <#CompositionalGeneralization> .
---

# Y-Layer Growth Measures (M-044 to M-046)

Y-Layer Growth measures capture the dynamics of knowledge evolution over time. While population measures (M-036 to M-043) provide a snapshot of how much knowledge exists, growth measures reveal how quickly and how well that knowledge base is developing. These are rate and quality metrics that turn static counts into actionable intelligence about the learning process.

## Measures

### M-044: Knowledge Enrichment Rate

The enrichment rate measures how many new knowledge items the system produces per hour during active learning. This includes items added at any layer -- new facts extracted, relationships discovered, inferences drawn, episodes recorded, procedures learned, or metacognitive observations made.

**Collection**: Compute as the delta in total knowledge items (M-043) divided by elapsed wall-clock hours between two measurement points. For meaningful results, measure over complete learning cycles rather than arbitrary time windows.

**Interpretation**:
- A declining enrichment rate during training may indicate the system is approaching saturation for its current source material, or that extraction/reasoning pipelines are bottlenecked.
- Sudden spikes may follow the ingestion of new source documents or the activation of a new reasoning capability.
- Compare enrichment rates across training runs to evaluate the impact of architectural or algorithmic changes.

### M-045: Knowledge Confidence Score

The confidence score is the mean confidence value across all knowledge items that carry a confidence annotation. Many knowledge systems assign confidence or certainty scores to extracted facts, inferred relationships, and derived conclusions. This measure aggregates those into a single indicator of overall epistemic quality.

**Collection**: Query all knowledge items that have an associated confidence value, compute the arithmetic mean, and normalize to a 0-1 scale. Items without confidence annotations are excluded from the calculation.

**Interpretation**:
- A high confidence score (above 0.8) suggests the system is operating within well-understood domains with strong source material.
- A low confidence score (below 0.5) may indicate noisy sources, aggressive inference, or insufficient validation.
- Track confidence over time: a system that adds knowledge while maintaining or increasing confidence is learning effectively. A system where confidence drops as volume increases may be over-extending.

### M-046: Knowledge Diversity Index

The diversity index applies Shannon entropy to the distribution of knowledge items across categories, domains, or topic clusters. It answers the question: "Is the system's knowledge evenly spread, or concentrated in a few areas?"

**Collection**: Categorize all knowledge items by domain or topic. Compute Shannon entropy:

```
H = -sum(p_i * log2(p_i))
```

where `p_i` is the proportion of knowledge items in category `i`. Higher entropy indicates more diverse, evenly distributed knowledge.

**Interpretation**:
- Maximum entropy occurs when knowledge is perfectly evenly distributed across all categories. This is desirable for general-purpose systems.
- Low entropy indicates domain concentration, which may be appropriate for specialist systems but problematic for generalists.
- Compare the diversity index to the target curriculum distribution to assess whether the system is learning proportionally across all expected domains.

## ACF Dimension Mapping

- **Enrichment Rate** maps to **Depth** (the system is synthesizing, not just ingesting) and **Autonomy** (higher rates suggest the system is actively driving its own learning).
- **Confidence Score** maps to **Factual Grounding** (epistemic reliability of claims) and **Generalization Boundary Awareness** (the system knows how certain it is).
- **Diversity Index** maps to **Breadth** (coverage across domains) and **Compositional Generalization** (diverse knowledge enables cross-domain connections).
