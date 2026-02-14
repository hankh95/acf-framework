---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ACF-2> a acf:CertificationLevel ;
    acf:id "ACF-2" ;
    acf:label "Middle School" ;
    acf:scoreMin 20.0 ;
    acf:scoreMax 40.0 ;
    acf:humanEquivalent "Middle school / GED preparation" ;
    acf:description "Can explain concepts, apply basic procedures, and demonstrate comprehension beyond rote memorization." .
---

# ACF-2: Middle School

**Score Range:** 20 -- 40

**Human Equivalent:** Middle school / GED preparation

## What This Level Means

An AI system certified at ACF-2 demonstrates **procedural comprehension** of a domain. It can:

- **Explain** concepts in its own words, not just recite definitions
- **Apply** basic procedures to straightforward problems
- **Summarize** information from multiple sources
- **Classify** inputs using learned criteria without explicit cues

## Cognitive Profile

At ACF-2, the system operates at the **Understand** and basic **Apply** levels of Bloom's taxonomy. It can paraphrase, give examples, and execute known procedures, but struggles with multi-step reasoning or novel problem formulations.

## Typical Capabilities

- Explain cause-and-effect relationships for well-known phenomena
- Solve problems using standard formulas or procedures
- Compare and contrast two concepts along given dimensions
- Produce structured summaries of provided text
- Follow multi-step instructions with minor adaptation

## Limitations

- Cannot analyze unfamiliar problems without scaffolding
- Cannot identify unstated assumptions
- Cannot evaluate conflicting sources of information
- Limited ability to transfer procedures across domains

## When to Use ACF-2 Certification

ACF-2 is appropriate for systems that serve as **explainers** or **guided problem solvers** in educational or consumer-facing contexts where users need comprehension support on well-defined topics.
