---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#Depth> a acf:Dimension ;
    acf:id "depth" ;
    acf:label "Depth" ;
    acf:shortName "L" ;
    acf:subLevelCount 6 ;
    acf:weight 0.111 ;
    acf:description "Measures cognitive depth using Bloom's Taxonomy levels. Depth captures how deeply an agent can reason about the topics it knows, from simple recall through original synthesis and creation." .

<#L1> a acf:SubLevel ;
    acf:id "L1" ;
    acf:dimension <#Depth> ;
    acf:level 1 ;
    acf:label "Remember" ;
    acf:scoreRange "0-17" ;
    acf:description "Recall facts and basic concepts. The agent can retrieve stored information and reproduce definitions, lists, and terminology." .

<#L2> a acf:SubLevel ;
    acf:id "L2" ;
    acf:dimension <#Depth> ;
    acf:level 2 ;
    acf:label "Understand" ;
    acf:scoreRange "17-33" ;
    acf:description "Explain ideas and concepts. The agent can paraphrase, summarize, and interpret meaning beyond rote recall." .

<#L3> a acf:SubLevel ;
    acf:id "L3" ;
    acf:dimension <#Depth> ;
    acf:level 3 ;
    acf:label "Apply" ;
    acf:scoreRange "33-50" ;
    acf:description "Use information in new situations. The agent can take learned concepts and apply them to solve novel problems or scenarios." .

<#L4> a acf:SubLevel ;
    acf:id "L4" ;
    acf:dimension <#Depth> ;
    acf:level 4 ;
    acf:label "Analyze" ;
    acf:scoreRange "50-67" ;
    acf:description "Draw connections, organize, and compare. The agent can decompose complex information, identify relationships, and distinguish relevant from irrelevant elements." .

<#L5> a acf:SubLevel ;
    acf:id "L5" ;
    acf:dimension <#Depth> ;
    acf:level 5 ;
    acf:label "Evaluate" ;
    acf:scoreRange "67-83" ;
    acf:description "Justify, critique, and defend positions. The agent can assess the quality of arguments, make judgments based on criteria, and provide reasoned evaluations." .

<#L6> a acf:SubLevel ;
    acf:id "L6" ;
    acf:dimension <#Depth> ;
    acf:level 6 ;
    acf:label "Create" ;
    acf:scoreRange "83-100" ;
    acf:description "Produce original work and synthesize new ideas. The agent can generate novel hypotheses, design solutions, and compose coherent original artifacts." .
---

# Depth

Depth measures the cognitive sophistication of an agent's reasoning, grounded in Bloom's Taxonomy — the well-established educational framework for classifying learning objectives by complexity. While Breadth asks "how much does the agent know?", Depth asks "how deeply can it think about what it knows?"

The six sub-levels (L1 through L6) follow Bloom's progression faithfully. At L1 (Remember), the agent can recall facts — names, dates, definitions, formulas. At L2 (Understand), it moves beyond parroting to genuine comprehension: it can explain concepts in its own words, summarize passages, and translate between representations. L3 (Apply) tests whether the agent can use knowledge in unfamiliar contexts, solving problems it has not seen before by transferring learned principles.

The upper levels represent increasingly sophisticated cognition. L4 (Analyze) requires the agent to decompose complex information, identify patterns, and organize components into coherent structures. L5 (Evaluate) demands critical judgment — the ability to assess arguments, weigh evidence, and justify positions using sound reasoning. At the pinnacle, L6 (Create) measures whether the agent can produce genuinely original work: generating hypotheses, designing experiments, composing creative artifacts, or synthesizing new frameworks from existing knowledge.

Depth is measured through structured exam batteries that target specific Bloom's levels. Each question is tagged with its cognitive level, and the agent's performance is assessed not just on correctness but on the sophistication of its reasoning. An agent that answers correctly through surface-level pattern matching scores lower than one that demonstrates deep analytical reasoning.

This dimension is particularly important for distinguishing between agents that merely retrieve information (chatbot-level) and those that can genuinely reason (cognitive-level). The L1-L6 progression provides a clear developmental trajectory for agent training.
