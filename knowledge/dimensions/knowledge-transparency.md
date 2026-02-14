---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#KnowledgeTransparency> a acf:Dimension ;
    acf:id "knowledge-transparency" ;
    acf:label "Knowledge Transparency" ;
    acf:shortName "KT" ;
    acf:subLevelCount 3 ;
    acf:weight 0.111 ;
    acf:description "Measures how inspectable, queryable, and traceable an agent's knowledge is. Knowledge Transparency captures the degree to which an agent's internal knowledge representation is accessible to external inspection, structured querying, and full provenance tracing." .

<#KT1> a acf:SubLevel ;
    acf:id "KT1" ;
    acf:dimension <#KnowledgeTransparency> ;
    acf:level 1 ;
    acf:label "Inspectable Knowledge" ;
    acf:scoreRange "0-33" ;
    acf:description "Knowledge is stored in a human-readable format. An observer can examine what the agent knows by reading its knowledge files directly." .

<#KT2> a acf:SubLevel ;
    acf:id "KT2" ;
    acf:dimension <#KnowledgeTransparency> ;
    acf:level 2 ;
    acf:label "Queryable Knowledge" ;
    acf:scoreRange "33-66" ;
    acf:description "Knowledge is structured for programmatic queries. Beyond human readability, the knowledge can be searched, filtered, and aggregated through structured query mechanisms." .

<#KT3> a acf:SubLevel ;
    acf:id "KT3" ;
    acf:dimension <#KnowledgeTransparency> ;
    acf:level 3 ;
    acf:label "Fully Traceable Reasoning" ;
    acf:scoreRange "66-100" ;
    acf:description "Complete reasoning chain traceability with provenance. Every conclusion can be traced back through its full reasoning chain to the original source documents that supported it." .
---

# Knowledge Transparency

Knowledge Transparency measures the degree to which an agent's knowledge is open to external scrutiny. In contrast to opaque neural models where knowledge is encoded in inscrutable weight matrices, a transparent knowledge system allows humans and other agents to inspect, query, and trace the agent's knowledge and reasoning. This dimension is central to building trustworthy AI systems that can be audited, debugged, and improved.

The three sub-levels (KT1 through KT3) build from basic readability to full reasoning traceability. At KT1, the agent's knowledge is stored in human-readable formats — markdown files, structured documents, or annotated graphs that a person can open and read. This is the minimum bar for transparency: you can look at what the agent knows, even if finding specific information requires manual search.

KT2 adds programmatic queryability. The knowledge is not just human-readable but machine-readable in a structured way. This means SPARQL-like queries over RDF graphs, keyword search with semantic filtering, or structured API access to the knowledge base. An engineer or another agent can ask "what does this agent know about topic X?" and get a precise, comprehensive answer without reading every file.

At KT3, the agent achieves full reasoning traceability. Every conclusion the agent reaches can be traced back through a complete chain of reasoning steps to the original source documents. If the agent says "X is true because Y and Z", you can verify that Y and Z are grounded in specific sources, that the inference from Y and Z to X follows valid reasoning rules, and that no steps are missing or fabricated. This level of transparency enables formal auditing of agent decisions.

Evaluation of Knowledge Transparency combines structural analysis (is the knowledge format inspectable?), query benchmarks (can structured queries return correct results?), and trace audits (can reasoning chains be followed end-to-end from conclusion to source?).
