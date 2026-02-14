---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#Autonomy> a acf:Dimension ;
    acf:id "autonomy" ;
    acf:label "Autonomy" ;
    acf:shortName "AU" ;
    acf:subLevelCount 4 ;
    acf:weight 0.111 ;
    acf:description "Measures self-directed learning and autonomous operation capability. Autonomy captures the degree to which an agent can operate independently, from executing prompted tasks through full autonomous operation with self-improvement." .

<#AU1> a acf:SubLevel ;
    acf:id "AU1" ;
    acf:dimension <#Autonomy> ;
    acf:level 1 ;
    acf:label "Prompted Task Execution" ;
    acf:scoreRange "0-25" ;
    acf:description "The agent can execute explicitly prompted tasks. It follows instructions reliably but requires human direction for what to do next." .

<#AU2> a acf:SubLevel ;
    acf:id "AU2" ;
    acf:dimension <#Autonomy> ;
    acf:level 2 ;
    acf:label "Knowledge Gap Detection" ;
    acf:scoreRange "25-50" ;
    acf:description "The agent detects gaps in its own knowledge and signals them. It can identify what it needs to learn but relies on external systems to provide the learning material." .

<#AU3> a acf:SubLevel ;
    acf:id "AU3" ;
    acf:dimension <#Autonomy> ;
    acf:level 3 ;
    acf:label "Self-Directed Learning" ;
    acf:scoreRange "50-75" ;
    acf:description "The agent engages in self-directed learning. It identifies knowledge gaps, seeks out relevant material, processes it, and integrates new knowledge into its existing knowledge graph without human intervention." .

<#AU4> a acf:SubLevel ;
    acf:id "AU4" ;
    acf:dimension <#Autonomy> ;
    acf:level 4 ;
    acf:label "Full Autonomous Operation" ;
    acf:scoreRange "75-100" ;
    acf:description "Full autonomous operation with self-improvement. The agent sets its own learning goals, optimizes its own processes, identifies and corrects its own errors, and continuously improves its capabilities over time." .
---

# Autonomy

Autonomy measures the degree to which an agent can operate independently and direct its own learning and improvement. This dimension captures the progression from a purely reactive tool that requires constant human direction to a fully autonomous agent that sets its own goals, learns from its environment, and improves itself over time. Autonomy is the dimension most closely tied to the long-term vision of artificial general intelligence.

The four sub-levels (AU1 through AU4) define a clear developmental trajectory. At AU1, the agent is a capable executor: given explicit instructions, it carries them out reliably and correctly. However, it has no initiative of its own — when the current task is complete, it waits for the next instruction. Most current AI assistants operate at this level, functioning as sophisticated tools that require human direction at every step.

AU2 introduces the first spark of self-awareness: knowledge gap detection. The agent can examine its own knowledge state and identify what is missing. When asked a question it cannot fully answer, it does not just say "I don't know" — it can articulate specifically what knowledge it would need to provide a complete answer. This meta-cognitive capability is a prerequisite for self-directed learning.

At AU3, the agent takes the leap into self-directed learning. Building on its ability to detect gaps, it now actively seeks out and processes new information to fill them. It can identify relevant source material, ingest and comprehend it, extract knowledge, and integrate that knowledge into its existing knowledge graph — all without human intervention. The key distinction from AU2 is agency: the agent does not just identify what it needs to learn, it actually goes and learns it.

AU4 represents full autonomous operation with self-improvement. The agent sets its own learning goals based on an understanding of its capabilities and the demands placed on it. It optimizes its own reasoning processes, identifies systematic errors in its own behavior and corrects them, and continuously improves its performance over time. At this level, the agent is not just learning content but improving its own learning and reasoning mechanisms — a form of recursive self-improvement.
