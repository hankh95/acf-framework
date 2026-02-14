---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-022> a acf:Measure ;
    rdfs:label "Knowledge Graph Growth" ;
    acf:id "M-022" ;
    acf:name "knowledge_graph_growth" ;
    acf:description "Total number of triples accumulated in the system's knowledge graph over time, tracking the growth of structured knowledge" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "quantity" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .

<#M-023> a acf:Measure ;
    rdfs:label "Topic Coverage" ;
    acf:id "M-023" ;
    acf:name "topic_coverage_count" ;
    acf:description "Number of distinct topics in the system's domain that have sufficient knowledge coverage to support meaningful responses" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "quantity" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .

<#M-024> a acf:Measure ;
    rdfs:label "Learning Events" ;
    acf:id "M-024" ;
    acf:name "learning_events_per_session" ;
    acf:description "Number of new knowledge items (triples, facts, relationships) added to the knowledge base per learning session or training cycle" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "quantity" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth>, <#Depth> .

<#M-025> a acf:Measure ;
    rdfs:label "Triple Count" ;
    acf:id "M-025" ;
    acf:name "triple_count" ;
    acf:description "Total number of subject-predicate-object triples currently stored in the system's knowledge graph" ;
    acf:unit "count" ;
    acf:dataType "integer" ;
    acf:category "quantity" ;
    acf:collection "automated" ;
    acf:mapsTo <#Breadth> .
---

# Quantity Measures (M-022 to M-025)

Quantity measures track the volume and coverage of knowledge within an AI system. While accuracy and quality measures assess how correct and useful the knowledge is, quantity measures assess how much knowledge the system has accumulated and how broadly it covers its intended domain. These measures are leading indicators: a system cannot demonstrate depth or breadth of capability without first having sufficient knowledge volume.

## M-022: Knowledge Graph Growth

**What it measures:** The total number of triples (subject-predicate-object assertions) accumulated in the system's knowledge graph over time. This is a cumulative measure that tracks the growth trajectory of the system's structured knowledge.

**How to collect:** Query the knowledge graph for total triple count at regular intervals (daily, weekly, or per training cycle). Record the count with a timestamp. Plot the growth curve to identify learning rate, plateaus, and acceleration periods.

**Target ranges:** Target ranges depend heavily on the domain and system maturity:
- Below 1,000 triples: Minimal knowledge; system can answer only basic questions
- 1,000-10,000 triples: Early-stage knowledge; covers core concepts but lacks depth
- 10,000-100,000 triples: Moderate knowledge base; supports meaningful domain coverage
- Above 100,000 triples: Substantial knowledge; supports rich reasoning and cross-referencing

## M-023: Topic Coverage

**What it measures:** The number of distinct topics within the system's intended domain that have sufficient knowledge coverage to support meaningful, substantive responses. A topic is considered "covered" when it has enough associated triples, facts, and relationships to answer representative questions about it.

**How to collect:** Define the system's topic taxonomy (either manually or through automated topic extraction). For each topic, count associated knowledge items. Apply a minimum coverage threshold (e.g., at least 10 triples per topic). Count the number of topics that meet or exceed the threshold.

**Target ranges:**
- Below 20% of domain topics: Significant coverage gaps; system cannot serve most queries
- 20-50%: Partial coverage; system is useful for well-covered topics only
- 50-80%: Good coverage; most domain topics have sufficient knowledge
- Above 80%: Comprehensive; system covers the vast majority of its intended domain

## M-024: Learning Events

**What it measures:** The number of new knowledge items (triples, facts, relationships, inferences) added to the knowledge base during a single learning session or training cycle. This measures the system's learning throughput.

**How to collect:** At the start and end of each learning session, record the knowledge base size. Calculate: `end_count - start_count`. Also track the composition of new items (raw facts vs. inferred relationships vs. procedural knowledge) for richer analysis.

**Target ranges:** Rates vary by domain complexity and source material:
- Below 50 per session: Slow learning; may indicate extraction or ingestion issues
- 50-500 per session: Moderate throughput; typical for careful, quality-focused learning
- 500-5,000 per session: Good throughput; efficient knowledge extraction pipeline
- Above 5,000 per session: High throughput; verify quality is maintained at this rate

## M-025: Triple Count

**What it measures:** The total number of subject-predicate-object triples currently stored in the system's knowledge graph. While M-022 tracks growth over time, M-025 is a point-in-time snapshot of the current knowledge base size.

**How to collect:** Query the knowledge graph for the total triple count. This can be a simple SPARQL `SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }` or equivalent graph database query.

**Target ranges:** Same as M-022 — the appropriate size depends on domain scope:
- Below 1,000: Minimal; suitable only for narrow, focused domains
- 1,000-10,000: Small but functional for specific use cases
- 10,000-100,000: Medium; supports broad domain coverage
- Above 100,000: Large; supports deep reasoning and cross-domain integration
