---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ACF-1> a acf:CertificationLevel ;
    acf:id "ACF-1" ;
    acf:label "Elementary" ;
    acf:scoreMin 0.0 ;
    acf:scoreMax 20.0 ;
    acf:humanEquivalent "K-5 elementary education" ;
    acf:description "Can recall basic facts, perform simple pattern matching, and demonstrate foundational awareness of a domain." .
---

# ACF-1: Elementary

**Score Range:** 0 -- 20

**Human Equivalent:** K-5 elementary education

## What This Level Means

An AI system certified at ACF-1 demonstrates **foundational awareness** of a domain. It can:

- **Recall** basic facts, definitions, and terminology
- **Recognize** simple patterns and categories
- **Reproduce** memorized procedures when prompted
- **Identify** key concepts from structured input

## Cognitive Profile

At ACF-1, the system operates primarily at the **Remember** and basic **Understand** levels of Bloom's taxonomy. Responses are largely retrieval-based, with limited ability to generalize beyond training examples.

## Typical Capabilities

- Answer factual recall questions (who, what, when, where)
- Match terms to definitions
- Classify inputs into predefined categories with explicit cues
- Follow step-by-step instructions without adaptation

## Limitations

- Cannot explain *why* something is true
- Cannot transfer knowledge to novel contexts
- Cannot handle ambiguity or incomplete information
- Cannot self-correct when given contradictory evidence

## When to Use ACF-1 Certification

ACF-1 is appropriate for systems that serve as **lookup assistants** or **guided tutors** in low-stakes environments where factual accuracy on well-defined questions is the primary requirement.
