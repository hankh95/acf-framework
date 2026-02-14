---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#GeneralizationBoundary> a acf:Dimension ;
    acf:id "generalization-boundary" ;
    acf:label "Generalization Boundary Awareness" ;
    acf:shortName "GBA" ;
    acf:subLevelCount 4 ;
    acf:weight 0.111 ;
    acf:description "Measures metacognition and out-of-distribution detection. Generalization Boundary Awareness captures how well an agent understands the limits of its own knowledge, from basic confidence calibration through full meta-cognitive self-assessment." .

<#GBA1> a acf:SubLevel ;
    acf:id "GBA1" ;
    acf:dimension <#GeneralizationBoundary> ;
    acf:level 1 ;
    acf:label "Confidence Calibration" ;
    acf:scoreRange "0-25" ;
    acf:description "The agent's confidence scores correlate with actual accuracy. When it says it is 80% confident, it is correct approximately 80% of the time." .

<#GBA2> a acf:SubLevel ;
    acf:id "GBA2" ;
    acf:dimension <#GeneralizationBoundary> ;
    acf:level 2 ;
    acf:label "Out-of-Domain Detection" ;
    acf:scoreRange "25-50" ;
    acf:description "The agent detects when a query falls outside its trained domains and signals this to the user rather than confabulating an answer. It knows what it does not know." .

<#GBA3> a acf:SubLevel ;
    acf:id "GBA3" ;
    acf:dimension <#GeneralizationBoundary> ;
    acf:level 3 ;
    acf:label "Domain-Adjacent Fiction Detection" ;
    acf:scoreRange "50-75" ;
    acf:description "The agent can detect domain-adjacent fiction: queries that appear to be in-domain but contain fabricated entities, false premises, or misleading framing designed to elicit plausible-sounding but incorrect responses." .

<#GBA4> a acf:SubLevel ;
    acf:id "GBA4" ;
    acf:dimension <#GeneralizationBoundary> ;
    acf:level 4 ;
    acf:label "Graceful Degradation" ;
    acf:scoreRange "75-100" ;
    acf:description "Graceful degradation with meta-cognitive self-assessment. The agent degrades performance smoothly at domain boundaries, provides useful partial answers when possible, and maintains an accurate self-model of its own capabilities and limitations." .
---

# Generalization Boundary Awareness

Generalization Boundary Awareness measures an agent's metacognitive ability to understand the limits of its own knowledge and reasoning. This is perhaps the most distinctively "intelligent" dimension in the ACF framework: it asks not what the agent knows, but whether the agent knows what it knows — and more critically, whether it knows what it does not know.

The four sub-levels (GBA1 through GBA4) progress from basic statistical calibration to sophisticated metacognitive self-modeling. At GBA1, the agent demonstrates confidence calibration: its stated confidence levels match its actual accuracy. This is a necessary foundation — an agent that is always 95% confident but only 60% accurate is dangerous, while one whose confidence faithfully tracks its accuracy is at least honest about its limitations.

GBA2 introduces out-of-domain detection, the ability to recognize when a query falls outside the agent's training or knowledge scope. Rather than generating a plausible-sounding answer about a topic it knows nothing about (a hallmark failure mode of large language models), the agent flags the query as out-of-domain and declines to answer or explicitly marks its response as speculative.

GBA3 addresses a subtler challenge: domain-adjacent fiction detection. These are queries that look like they belong to the agent's domain but contain fabricated elements — a made-up author in a literature question, a non-existent theorem in a mathematics query, or a fictional historical event presented as real. Detecting these requires the agent to have not just knowledge but a robust model of what exists within its knowledge, enabling it to recognize gaps rather than filling them with confabulation.

At GBA4, the agent achieves graceful degradation with meta-cognitive self-assessment. When operating near the boundaries of its knowledge, it degrades smoothly rather than failing catastrophically. It can provide partial answers with appropriate caveats, suggest where to find better information, and maintain an accurate internal model of its own strengths and weaknesses across different domains and question types.
