---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-036> a acf:Measure ;
    rdfs:label "Y0 Source Document Count" ;
    acf:id "M-036" ;
    acf:name "y0_document_count" ;
    acf:description "Total number of raw source documents ingested into the foundational knowledge layer. Measures the breadth of raw material available for higher-layer extraction." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .

<#M-037> a acf:Measure ;
    rdfs:label "Y1 Fact Count" ;
    acf:id "M-037" ;
    acf:name "y1_fact_count" ;
    acf:description "Total number of discrete facts extracted from source documents into the factual knowledge layer. Reflects the system's ability to decompose sources into atomic, verifiable claims." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth>, <#FactualGrounding> .

<#M-038> a acf:Measure ;
    rdfs:label "Y2 Relationship Count" ;
    acf:id "M-038" ;
    acf:name "y2_relationship_count" ;
    acf:description "Total number of explicitly encoded relationships (edges) between knowledge entities. Captures how richly the system connects concepts to form a navigable knowledge graph." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth>, <#CompositionalGeneralization> .

<#M-039> a acf:Measure ;
    rdfs:label "Y3 Experience Count" ;
    acf:id "M-039" ;
    acf:name "y3_experience_count" ;
    acf:description "Total number of experiential records at the Experience layer (conversations, actions, and learning events). Reflects accumulated operational experience that informs future decision-making. (Canon Y3 = Experience: the episodic content formerly counted at legacy Y4. 'Inference' is not a layer — it is an epistemic-status property of a fact, measured by M-048.)" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-040> a acf:Measure ;
    rdfs:label "Y4 Journal Count" ;
    acf:id "M-040" ;
    acf:name "y4_journal_count" ;
    acf:description "Total number of journal records at the Journal layer (opinions, reflections, and mental notes the system forms about its own experience). Reflects the system's self-reflective practice. (Canon Y4 = Journal: a genuinely new layer with no legacy equivalent.)" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-041> a acf:Measure ;
    rdfs:label "Y5 Procedure Count" ;
    acf:id "M-041" ;
    acf:name "y5_procedure_count" ;
    acf:description "Total number of procedural skills encoded in the system's knowledge base. Measures the breadth of executable capabilities the system can autonomously perform." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy> .

<#M-042> a acf:Measure ;
    rdfs:label "Y6 Metacognition Record Count" ;
    acf:id "M-042" ;
    acf:name "y6_metacognition_count" ;
    acf:description "Total number of metacognitive records capturing the system's self-reflective observations about its own knowledge, reasoning processes, and confidence calibration." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#GeneralizationBoundary>, <#Autonomy> .

<#M-043> a acf:Measure ;
    rdfs:label "Total Knowledge Items" ;
    acf:id "M-043" ;
    acf:name "total_knowledge_items" ;
    acf:description "Aggregate count of all knowledge items across all layers (Y0 through Y6). Provides a single summary metric for overall knowledge base size." ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "y-layer-population" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .
---

# Y-Layer Population Measures (M-036 to M-043)

Y-Layer Population measures quantify how much knowledge exists at each layer of a structured, hierarchical knowledge system. In such systems, knowledge is organized into ascending layers of abstraction: raw source documents at the foundation, progressing through extracted facts, explicit relationships, experiential records, journal reflections, procedural skills, and metacognitive self-awareness at the top.

These measures serve as the most fundamental indicators of a knowledge system's maturity. An empty or sparsely populated layer reveals a gap in the system's cognitive pipeline -- either the extraction process is not running, the system has not yet accumulated enough operational experience, or it is not reflecting on that experience.

## Layer Definitions

| Layer | Name | What It Contains |
|-------|------|-----------------|
| Y0 | Source Documents | Raw ingested materials (text, data, media references) |
| Y1 | Extracted Facts | Atomic, verifiable claims decomposed from sources |
| Y2 | Relationships | Explicit edges connecting entities in a knowledge graph |
| Y3 | Experience | Conversations, actions, and learning events (experiential records) |
| Y4 | Journal | Opinions, reflections, and mental notes the system forms about its experience |
| Y5 | Procedural Skills | Executable capabilities and learned workflows |
| Y6 | Metacognition | Self-reflective observations about the system's own knowledge and reasoning |

> **Canon note (V14 Y0–Y6).** Y0–Y2 are *definitional* (transferable "what IS true"); Y3–Y6 are *experiential* (being-specific). "Inference" is **not** a Y-layer — it is an epistemic-status property of a fact (`epistemic_status: Derived`) and is assessed by the quality measure **M-048**, decoupled from layer numbering. The Experience layer (Y3) holds the episodic content historically counted at legacy "Y4"; the Journal layer (Y4) is new.

## Collection Method

All eight measures in this category are collected automatically by querying the knowledge store. Each layer's storage backend (file system, graph database, or memory store) exposes a count API or can be enumerated directly. Collection should run at regular intervals (e.g., after each training cycle or ingestion batch) and results should be recorded with timestamps for longitudinal tracking.

The formula for M-043 is simply the sum of M-036 through M-042:

```
total_knowledge_items = y0_document_count + y1_fact_count + y2_relationship_count
                      + y3_experience_count + y4_journal_count + y5_procedure_count
                      + y6_metacognition_count
```

## Interpretation Guidelines

- **Healthy growth pattern**: Lower layers should populate first and in larger quantities. A system with many Y4 journal reflections but few Y3 experiences (or few Y1 facts) may be over-reflecting on a thin experiential or evidence base.
- **Layer ratios**: Track ratios between adjacent layers (e.g., Y1/Y0 = facts per document, Y2/Y1 = relationships per fact). These ratios reveal extraction efficiency and knowledge density.
- **Zero-population layers**: A layer with zero items after training indicates a pipeline failure or a system that has not yet reached that level of cognitive development.
- **Diminishing returns**: Very large counts in lower layers with stagnant upper layers suggest the system needs improved reasoning capabilities, not more raw data.

## ACF Dimension Mapping

The population measures map primarily to **Breadth** (coverage of the knowledge landscape) with specific layers also mapping to deeper capabilities:

- Y1 facts ground the **Factual Grounding** dimension (provenance-linked claims)
- Y2 relationships support **Compositional Generalization** (connecting concepts across domains)
- Y3 experiences inform **Service Orientation** (learning from interaction experience)
- Y4 journal reflections support **Service Orientation** (reflective self-improvement over accumulated experience)
- Y5 procedures indicate **Autonomy** (breadth of executable skills)
- Y6 metacognition connects to **Generalization Boundary Awareness** and **Autonomy** (knowing what the system knows and does not know)

*(The **Depth** and **Formal Reasoning** dimensions are no longer tied to a population layer: inference is an epistemic-status property, so synthesis quality is measured by **M-048** — see y-layer-quality.md — not by counting a "Y3 inference" layer.)*
