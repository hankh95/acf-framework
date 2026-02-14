---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#FormalReasoning> a acf:Dimension ;
    acf:id "formal-reasoning" ;
    acf:label "Formal Reasoning" ;
    acf:shortName "FR" ;
    acf:subLevelCount 4 ;
    acf:weight 0.111 ;
    acf:description "Measures logical inference and formal proof capability. Formal Reasoning captures an agent's ability to perform structured logical deduction, from basic pattern matching through rigorous multi-step proof construction." .

<#FR1> a acf:SubLevel ;
    acf:id "FR1" ;
    acf:dimension <#FormalReasoning> ;
    acf:level 1 ;
    acf:label "Basic Pattern Matching" ;
    acf:scoreRange "0-25" ;
    acf:description "The agent can identify surface-level patterns and apply simple heuristic rules to match inputs to outputs." .

<#FR2> a acf:SubLevel ;
    acf:id "FR2" ;
    acf:dimension <#FormalReasoning> ;
    acf:level 2 ;
    acf:label "Single-Step Inference" ;
    acf:scoreRange "25-50" ;
    acf:description "The agent can perform single-step logical inference: given premises and a rule, derive an immediate conclusion (modus ponens, modus tollens)." .

<#FR3> a acf:SubLevel ;
    acf:id "FR3" ;
    acf:dimension <#FormalReasoning> ;
    acf:level 3 ;
    acf:label "Multi-Step Deduction" ;
    acf:scoreRange "50-75" ;
    acf:description "The agent can chain multiple deductive steps together, maintaining logical consistency across a reasoning chain of three or more steps." .

<#FR4> a acf:SubLevel ;
    acf:id "FR4" ;
    acf:dimension <#FormalReasoning> ;
    acf:level 4 ;
    acf:label "Formal Proof Construction" ;
    acf:scoreRange "75-100" ;
    acf:description "The agent can construct formal proofs with explicit justification for each step, handle counterexamples, and reason about proof validity." .
---

# Formal Reasoning

Formal Reasoning measures an agent's capacity for structured logical deduction and proof. Unlike general intelligence or common-sense reasoning, this dimension specifically targets the agent's ability to follow and construct valid logical arguments with explicit rules of inference. It is the dimension most closely aligned with classical AI and symbolic reasoning traditions.

The four sub-levels (FR1 through FR4) progress from surface-level pattern recognition to rigorous proof construction. At FR1, the agent recognizes patterns — "these inputs produce these outputs" — but without understanding why. FR2 introduces single-step logical inference: given "All X are Y" and "A is X", the agent can conclude "A is Y". This is the foundation of deductive reasoning.

FR3 raises the bar significantly by requiring multi-step deduction chains. The agent must maintain logical consistency across several inference steps, track which premises have been used, and avoid fallacies like affirming the consequent or circular reasoning. This level separates agents that can follow a logical thread from those that merely pattern-match on surface features.

At FR4, the agent can construct complete formal proofs. This includes choosing appropriate inference rules, structuring arguments with explicit justifications, handling edge cases and counterexamples, and reasoning about the validity and soundness of arguments. An FR4-capable agent can not only solve logical problems but explain its reasoning in a way that could be mechanically verified.

Formal Reasoning is evaluated through structured logic tasks: syllogism completion, truth-table verification, multi-step proof problems, and formal argument analysis. Performance is scored not only on correctness but on the quality and explicitness of the reasoning chain.
