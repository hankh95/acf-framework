---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#Breadth> a acf:Dimension ;
    acf:id "breadth" ;
    acf:label "Breadth" ;
    acf:shortName "B" ;
    acf:subLevelCount 4 ;
    acf:weight 0.111 ;
    acf:description "Measures topic coverage and cross-domain integration capability. Breadth captures how widely an agent's knowledge spans across the domains it is expected to operate in, from basic topic existence through full cross-domain integration." .

<#B1> a acf:SubLevel ;
    acf:id "B1" ;
    acf:dimension <#Breadth> ;
    acf:level 1 ;
    acf:label "Topic Existence" ;
    acf:scoreRange "0-30" ;
    acf:description "Any coverage greater than zero. The agent has at least some knowledge of the topic, however shallow or incomplete." .

<#B2> a acf:SubLevel ;
    acf:id "B2" ;
    acf:dimension <#Breadth> ;
    acf:level 2 ;
    acf:label "Majority Coverage" ;
    acf:scoreRange "30-60" ;
    acf:description "Topic coverage exceeds 50%. The agent covers the majority of expected subtopics within each domain." .

<#B3> a acf:SubLevel ;
    acf:id "B3" ;
    acf:dimension <#Breadth> ;
    acf:level 3 ;
    acf:label "Cross-Domain Capability" ;
    acf:scoreRange "60-90" ;
    acf:description "Coverage exceeds 80% with demonstrated cross-domain capability. The agent can draw on knowledge from one domain to inform another." .

<#B4> a acf:SubLevel ;
    acf:id "B4" ;
    acf:dimension <#Breadth> ;
    acf:level 4 ;
    acf:label "Full Cross-Domain Integration" ;
    acf:scoreRange "90-100" ;
    acf:description "Full coverage with cross-domain integration. The agent seamlessly synthesizes knowledge across all trained domains." .
---

# Breadth

Breadth measures the extent to which an agent's knowledge spans the domains and topics it is expected to operate in. It answers the question: "How much of the required knowledge landscape does this agent actually cover?" A high breadth score indicates that there are few blind spots in the agent's training data or learned knowledge base.

The dimension is divided into four sub-levels (B1 through B4) that progress from minimal topic awareness to fully integrated cross-domain knowledge. At the lowest level (B1), we simply check whether the agent has any coverage at all for a given topic. At B2, coverage must exceed 50% of expected subtopics. B3 raises the bar to 80% coverage and additionally requires the agent to demonstrate cross-domain capability — the ability to connect ideas between different knowledge areas.

At the highest level (B4), the agent achieves full coverage across all expected domains and demonstrates seamless cross-domain integration. This means the agent can not only answer questions in each domain independently but can synthesize knowledge across domains to produce richer, more connected responses.

Breadth is measured through curriculum coverage analysis: given a defined curriculum of topics and subtopics, what percentage does the agent cover, and can it demonstrate connections between them? This makes breadth both objectively measurable and directly tied to the agent's training curriculum.

The default weight for Breadth in the overall ACF score is 0.111 (1/9), reflecting equal weighting across all nine dimensions. This weight can be adjusted based on use-case priorities — for example, a general-purpose assistant might weight Breadth higher than a specialist agent.
