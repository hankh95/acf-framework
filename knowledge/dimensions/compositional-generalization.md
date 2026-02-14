---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#CompositionalGeneralization> a acf:Dimension ;
    acf:id "compositional-generalization" ;
    acf:label "Compositional Generalization" ;
    acf:shortName "CG" ;
    acf:subLevelCount 3 ;
    acf:weight 0.111 ;
    acf:description "Measures the ability to combine known concepts in novel ways. Compositional Generalization captures whether an agent can go beyond memorized combinations to systematically generate and reason about new compositions of familiar elements." .

<#CG1> a acf:SubLevel ;
    acf:id "CG1" ;
    acf:dimension <#CompositionalGeneralization> ;
    acf:level 1 ;
    acf:label "Basic Composition" ;
    acf:scoreRange "0-33" ;
    acf:description "Basic known-concept composition. The agent can combine familiar concepts in ways it has seen during training, but struggles with novel pairings." .

<#CG2> a acf:SubLevel ;
    acf:id "CG2" ;
    acf:dimension <#CompositionalGeneralization> ;
    acf:level 2 ;
    acf:label "Novel Combinations" ;
    acf:scoreRange "33-66" ;
    acf:description "Novel combinations of known concepts. The agent can combine familiar concepts in ways not explicitly seen during training, producing meaningful and correct compositions." .

<#CG3> a acf:SubLevel ;
    acf:id "CG3" ;
    acf:dimension <#CompositionalGeneralization> ;
    acf:level 3 ;
    acf:label "Systematic Compositional Generalization" ;
    acf:scoreRange "66-100" ;
    acf:description "Systematic compositional generalization at the SCAN/COGS benchmark level. The agent demonstrates algebraic compositionality — understanding the rules of combination well enough to handle arbitrary novel compositions." .
---

# Compositional Generalization

Compositional Generalization measures an agent's ability to combine known building blocks in novel ways — a capability that is considered a hallmark of genuine understanding versus mere memorization. This dimension draws on the rich literature in cognitive science and AI around systematic compositionality, including benchmarks like SCAN and COGS that test whether models can generalize combinatorially.

The three sub-levels (CG1 through CG3) capture a progression from rote combination to systematic generalization. At CG1, the agent can compose concepts it has seen combined before: if it learned "red ball" and "blue car" separately but also saw "red car" in training, it can handle that combination. However, it struggles when asked to combine concepts in ways it has never encountered, such as applying a spatial reasoning pattern from geometry to a social relationship in literature.

At CG2, the agent demonstrates the ability to produce novel combinations of familiar concepts. It understands each component well enough to combine them in untrained configurations and produce meaningful, correct results. For example, if it knows "comparative analysis" and "marine biology", it can perform a comparative analysis of marine ecosystems even if it never saw that specific task during training.

CG3 represents systematic compositional generalization — the ability to understand the abstract rules of composition themselves. At this level, the agent's generalization is algebraic: it can handle arbitrary novel compositions because it has internalized the structural rules that govern how concepts combine. This is the level tested by benchmarks like SCAN (Simplified Commands for Abstract Navigation) and COGS (Compositional Generalization Challenge), which probe whether an agent can handle exponentially many combinations from a finite set of primitives and rules.

Evaluation uses held-out compositional tasks: the agent is trained on concept A, concept B, and some combinations, then tested on novel A+B combinations it has never seen. Systematic scoring checks whether performance degrades gracefully or catastrophically as compositional distance from training data increases.
