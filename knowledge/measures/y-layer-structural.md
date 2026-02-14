---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-053> a acf:Measure ;
    rdfs:label "Cross-Layer Provenance" ;
    acf:id "M-053" ;
    acf:name "cross_layer_provenance" ;
    acf:description "Percentage of knowledge items in higher layers (Y1 and above) that have a complete, traceable provenance chain back to their originating source documents in Y0. Measures the auditability of the knowledge derivation pipeline." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-structural" ;
    acf:collection "automated" ;
    acf:mapsTo <#KnowledgeTransparency> .

<#M-054> a acf:Measure ;
    rdfs:label "Layer Utilization Distribution" ;
    acf:id "M-054" ;
    acf:name "layer_utilization" ;
    acf:description "Shannon entropy of the distribution of knowledge items across all layers (Y0 through Y6). Higher entropy indicates more balanced utilization of the full knowledge hierarchy rather than over-concentration in a single layer." ;
    acf:unit "score" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-structural" ;
    acf:collection "automated" ;
    acf:mapsTo <#Depth>, <#Breadth> .

<#M-055> a acf:Measure ;
    rdfs:label "Knowledge Graph Connectivity" ;
    acf:id "M-055" ;
    acf:name "graph_connectivity" ;
    acf:description "Average degree (number of edges per node) in the knowledge graph. Higher connectivity indicates a more richly interlinked knowledge structure where concepts are connected through multiple relationship pathways." ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "y-layer-structural" ;
    acf:collection "automated" ;
    acf:mapsTo <#CompositionalGeneralization> .
---

# Y-Layer Structural Measures (M-053 to M-055)

Y-Layer Structural measures evaluate the architectural health of the knowledge system as a whole. Rather than examining individual layers in isolation (as population and quality measures do), structural measures look at how layers relate to each other, how knowledge flows between them, and how well-connected the overall graph is.

These measures address a fundamental concern: a knowledge system can have healthy individual layers while still being poorly structured overall. Layers might be disconnected from each other (no provenance chains), unevenly utilized (everything concentrated in one layer), or sparsely connected (many isolated nodes with few relationships). Structural measures detect these systemic issues.

## Measures

### M-053: Cross-Layer Provenance

Provenance is the chain of evidence from a knowledge item back to its original source. In a well-structured system, a Y3 inference should trace back through the Y2 relationships and Y1 facts it was derived from, all the way down to the Y0 source documents. Cross-layer provenance measures what percentage of higher-layer items have this complete chain.

**Collection**: For each knowledge item in Y1 through Y6, walk its provenance chain downward toward Y0. An item has complete provenance if every link in the chain resolves to a valid item in the layer below, terminating at a Y0 source document. Compute the percentage of items with complete provenance.

**Interpretation**:
- 100% provenance means every piece of derived knowledge can be audited back to its source. This is the gold standard for transparent, trustworthy AI systems.
- Below 90% indicates systematic gaps in the derivation pipeline -- some extraction or reasoning steps are not recording their sources.
- Provenance gaps at specific layer transitions (e.g., Y2-to-Y1 links are intact but Y3-to-Y2 links are missing) point to specific pipeline components that need instrumentation.

### M-054: Layer Utilization Distribution

Layer utilization measures whether the system is making balanced use of its full knowledge hierarchy, or whether knowledge is concentrated in just one or two layers. It applies Shannon entropy to the distribution of items across layers.

**Collection**: Count items at each layer (using M-036 through M-042). Compute the proportion of total items at each layer, then calculate Shannon entropy:

```
H = -sum(p_i * log2(p_i))
```

where `p_i` is the proportion of items at layer `i`. Maximum entropy for 7 layers is `log2(7) = 2.807`.

**Interpretation**:
- High entropy (above 2.0) indicates balanced utilization across layers. The system is extracting facts, building relationships, making inferences, accumulating experience, learning procedures, and reflecting on itself.
- Low entropy (below 1.0) indicates heavy concentration. A system with 90% of its knowledge in Y0 (raw documents) has not yet developed higher-order cognitive capabilities. A system concentrated in Y3 (inferences) without proportional Y1 (facts) may be making unsupported leaps.
- The "ideal" distribution depends on the system's maturity and purpose. Early-stage systems naturally concentrate in lower layers. Mature systems should show population across all layers.

### M-055: Knowledge Graph Connectivity

Graph connectivity measures how densely interconnected the knowledge graph is by computing the average degree (number of edges per node). A highly connected graph allows the system to traverse from any concept to related concepts through multiple paths, supporting richer reasoning and more robust generalization.

**Collection**: Count the total number of edges and the total number of nodes in the knowledge graph. Compute: `average_degree = total_edges / total_nodes`. Alternatively, for directed graphs, compute in-degree and out-degree separately.

**Interpretation**:
- An average degree below 1.0 means the graph has more isolated nodes than connected ones -- many concepts exist in isolation without relationships to other concepts.
- An average degree between 2.0 and 5.0 is typical for moderately connected knowledge graphs.
- Very high average degree (above 10.0) may indicate overly aggressive relationship extraction that creates noise.
- Track connectivity over time: it should increase as the system discovers more relationships between existing concepts, not just as new concepts are added.

## ACF Dimension Mapping

Structural measures connect to the ACF dimensions that concern system-level coherence:

- **Cross-Layer Provenance** is the primary measure for **Knowledge Transparency** -- a system cannot explain its reasoning if it cannot trace the chain of evidence.
- **Layer Utilization Distribution** maps to both **Depth** (the system is using all cognitive levels, not just surface extraction) and **Breadth** (balanced utilization implies comprehensive knowledge processing).
- **Knowledge Graph Connectivity** directly supports **Compositional Generalization** -- rich interconnections between concepts enable the system to combine knowledge in novel ways to address new problems.
