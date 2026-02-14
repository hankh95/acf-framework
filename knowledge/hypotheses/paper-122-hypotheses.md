---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#H122.1> a acf:Hypothesis ;
    acf:id "H122.1" ;
    rdfs:label "Breadth-Depth Independence" ;
    acf:description "Breadth and depth are independent dimensions; high breadth does not imply high depth, and vice versa." ;
    acf:target "r < 0.3 (weak correlation between breadth and depth scores)" ;
    acf:targetValue "0.3"^^xsd:decimal ;
    acf:comparison "LT" ;
    acf:metric "pearson_correlation" ;
    acf:dimension <#Breadth>, <#Depth> ;
    acf:category "dimensional-independence" .

<#H122.2> a acf:Hypothesis ;
    acf:id "H122.2" ;
    rdfs:label "Human Certification Equivalence" ;
    acf:description "AI systems can achieve measurable equivalence to human certification levels using the ACF framework." ;
    acf:target "System achieves ACF-3 or higher on trained domains" ;
    acf:targetValue "3"^^xsd:integer ;
    acf:comparison "GE" ;
    acf:metric "acf_level" ;
    acf:category "certification-validity" .

<#H122.3> a acf:Hypothesis ;
    acf:id "H122.3" ;
    rdfs:label "Service Orientation Correlation" ;
    acf:description "Higher ACF levels correlate with better real-world task completion; understanding maps to practical service capability." ;
    acf:target "r > 0.7 between ACF level and task completion rates" ;
    acf:targetValue "0.7"^^xsd:decimal ;
    acf:comparison "GT" ;
    acf:metric "pearson_correlation" ;
    acf:dimension <#ServiceOrientation> ;
    acf:category "dimensional-validity" .

<#H122.4> a acf:Hypothesis ;
    acf:id "H122.4" ;
    rdfs:label "Provenance Requirement" ;
    acf:description "Requiring provenance (traceability) for claims improves accuracy without reducing coverage." ;
    acf:target ">=95% accuracy with provenance vs <80% without; coverage >=90%" ;
    acf:targetValue "0.95"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "accuracy_with_provenance" ;
    acf:dimension <#FactualGrounding>, <#KnowledgeTransparency> ;
    acf:category "architectural-design" .

<#H122.5> a acf:Hypothesis ;
    acf:id "H122.5" ;
    rdfs:label "LLM Depth Ceiling" ;
    acf:description "Pure LLMs plateau at Bloom L3-L4 due to lack of structured knowledge; they cannot perform high-level reasoning (Evaluation/Creation) at scale." ;
    acf:target "LLMs achieve <60% on L5-L6 (Evaluate/Create) tasks" ;
    acf:targetValue "0.6"^^xsd:decimal ;
    acf:comparison "LT" ;
    acf:metric "bloom_l5_l6_accuracy" ;
    acf:dimension <#Depth> ;
    acf:category "paradigm-comparison" .

<#H122.6> a acf:Hypothesis ;
    acf:id "H122.6" ;
    rdfs:label "Understanding Efficiency Improvement" ;
    acf:description "Neurosymbolic learning achieves higher understanding per compute unit than LLM training paradigms." ;
    acf:target "Neurosymbolic UER >=10x better than LLM fine-tuning" ;
    acf:targetValue "10"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "uer_ratio" ;
    acf:category "paradigm-comparison" .

<#H122.7> a acf:Hypothesis ;
    acf:id "H122.7" ;
    rdfs:label "Compositional Generalization Gap" ;
    acf:description "Neurosymbolic systems demonstrate superior compositional generalization — the ability to combine learned components into novel combinations — compared to pure LLMs." ;
    acf:target "Neurosymbolic >=80%, LLM <20% on SCAN-style compositional tasks" ;
    acf:targetValue "0.8"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "compositional_accuracy" ;
    acf:dimension <#CompositionalGeneralization> ;
    acf:category "paradigm-comparison" .

<#H122.8> a acf:Hypothesis ;
    acf:id "H122.8" ;
    rdfs:label "Knowledge Transparency Enables Verification" ;
    acf:description "Explicit, queryable knowledge representation enables formal verification of AI reasoning; systems with high knowledge transparency achieve higher user trust and domain expert validation." ;
    acf:target "KT3 (full transparency) correlates with higher user trust scores" ;
    acf:metric "user_trust_score" ;
    acf:dimension <#KnowledgeTransparency> ;
    acf:category "dimensional-validity" .

<#H122.9> a acf:Hypothesis ;
    acf:id "H122.9" ;
    rdfs:label "GBA Distinguishes Expert Systems" ;
    acf:description "The GBA dimension distinguishes AI systems that understand their own limitations from those that overconfidently produce false information." ;
    acf:target "Expert systems GBA <50, neurosymbolic systems GBA >75" ;
    acf:targetValue "75"^^xsd:decimal ;
    acf:comparison "GT" ;
    acf:metric "gba_score" ;
    acf:dimension <#GeneralizationBoundary> ;
    acf:category "dimensional-validity" .

<#H122.10> a acf:Hypothesis ;
    acf:id "H122.10" ;
    rdfs:label "Paradigm Selection Capability" ;
    acf:description "Advanced AI systems with high GBA scores can dynamically select optimal reasoning paradigms for different task types." ;
    acf:target "System demonstrates paradigm selection; pure systems fail on mismatched tasks" ;
    acf:metric "paradigm_selection_accuracy" ;
    acf:dimension <#GeneralizationBoundary>, <#Autonomy> ;
    acf:category "meta-cognitive" .

<#H122.11> a acf:Hypothesis ;
    acf:id "H122.11" ;
    rdfs:label "Symbolic-to-Motor Transfer" ;
    acf:description "Embodied AI systems can read mathematical specifications and use symbolic knowledge to accelerate neural motor learning — a capability humans fundamentally cannot perform." ;
    acf:target "2-5x faster motor skill convergence with symbolic knowledge" ;
    acf:targetValue "2"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "motor_convergence_speedup" ;
    acf:category "embodied-ai" .

<#H122.12> a acf:Hypothesis ;
    acf:id "H122.12" ;
    rdfs:label "Autonomous Gap Detection" ;
    acf:description "AI systems can autonomously detect and identify gaps in their own knowledge without external prompting." ;
    acf:target "System detects 70%+ of knowledge gaps in evaluation domains" ;
    acf:targetValue "0.7"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "gap_detection_recall" ;
    acf:dimension <#Autonomy>, <#GeneralizationBoundary> ;
    acf:category "autonomy-validation" .

<#H122.13> a acf:Hypothesis ;
    acf:id "H122.13" ;
    rdfs:label "Crystallization Efficiency" ;
    acf:description "In-conversation learning (crystallization of neural answers into symbolic knowledge) achieves high precision without requiring extensive human validation loops." ;
    acf:target "99%+ precision in in-conversation learning" ;
    acf:targetValue "0.99"^^xsd:decimal ;
    acf:comparison "GE" ;
    acf:metric "crystallization_precision" ;
    acf:dimension <#Autonomy> ;
    acf:category "autonomy-validation" .

<#H122.14> a acf:Hypothesis ;
    acf:id "H122.14" ;
    rdfs:label "Self-Directed Learning" ;
    acf:description "AI systems can acquire knowledge from external sources and integrate it into their knowledge graph without explicit human instruction." ;
    acf:target "System acquires knowledge autonomously at AU3 validation level" ;
    acf:metric "autonomous_acquisition_rate" ;
    acf:dimension <#Autonomy> ;
    acf:category "autonomy-validation" .
---

# Paper 122 Hypotheses: AGI Certification Framework

This file defines the 14 core hypotheses of the AGI Certification Framework (ACF), originally formulated in Paper 122 — "Measuring Machine Understanding: A Neurosymbolic Approach to AGI Certification."

These hypotheses establish testable predictions about AGI measurement, dimensional independence, paradigm comparison, and system capability validation.

## Hypothesis Categories

### Dimensional Independence (H122.1)

**H122.1 — Breadth-Depth Independence**: Tests whether Breadth and Depth are genuinely independent dimensions. If they correlate strongly (r > 0.3), the framework has redundant dimensions. A weak or negative correlation validates the framework's dimensional structure.

**Validation**: Compute Pearson correlation between breadth and depth scores across multiple AI systems. Use `acf test H122.1 --data <dir>` to evaluate.

### Certification Validity (H122.2)

**H122.2 — Human Certification Equivalence**: Tests whether the ACF level assignments produce meaningful equivalence to human professional certifications. An AI system rated ACF-4 should perform comparably to a human with a Bachelor's degree in the relevant domain.

**Validation**: Administer professional certification exam samples (Bar Exam, USMLE, FE/PE, CFA) to AI systems and compare to human passing thresholds.

### Dimensional Validity (H122.3, H122.8, H122.9)

**H122.3 — Service Orientation Correlation**: Higher ACF levels should correlate with better task completion, validating that the framework measures practical capability, not just theoretical knowledge.

**H122.8 — Knowledge Transparency Enables Verification**: Systems with explicit, queryable knowledge representations should achieve higher trust scores from domain experts.

**H122.9 — GBA Distinguishes Expert Systems**: The Generalization Boundary Awareness dimension should reliably distinguish systems that know their limits from those that hallucinate confidently.

### Architectural Design (H122.4)

**H122.4 — Provenance Requirement**: Requiring source attribution for all claims should improve accuracy without sacrificing coverage — a key design principle for high-scoring ACF systems.

### Paradigm Comparison (H122.5, H122.6, H122.7)

These hypotheses compare neurosymbolic architectures against pure LLM approaches:

**H122.5 — LLM Depth Ceiling**: Pure LLMs should plateau at Bloom L3-L4, unable to reliably perform Evaluation (L5) and Creation (L6) tasks that require structured knowledge.

**H122.6 — Understanding Efficiency Improvement**: Neurosymbolic systems should achieve dramatically better understanding per compute unit (UER metric) compared to LLM training paradigms.

**H122.7 — Compositional Generalization Gap**: Neurosymbolic systems should vastly outperform LLMs on compositional generalization benchmarks (SCAN/COGS/CFQ-style tasks).

### Meta-Cognitive (H122.10)

**H122.10 — Paradigm Selection Capability**: Advanced systems should dynamically select the optimal reasoning paradigm (symbolic, neural, or hybrid) based on task characteristics.

### Embodied AI (H122.11)

**H122.11 — Symbolic-to-Motor Transfer**: Embodied AI systems should be able to read mathematical specifications and use that symbolic knowledge to accelerate motor learning — a superhuman capability that validates the neurosymbolic approach for robotics.

### Autonomy Validation (H122.12, H122.13, H122.14)

**H122.12 — Autonomous Gap Detection**: Systems should be able to identify what they don't know without being told.

**H122.13 — Crystallization Efficiency**: In-conversation learning should achieve near-perfect precision, validating that neural-to-symbolic knowledge transfer works reliably.

**H122.14 — Self-Directed Learning**: The highest autonomy level — systems that independently seek out and integrate new knowledge.

## Testing Hypotheses

Use the ACF CLI to evaluate hypotheses against collected data:

```bash
# Test a specific hypothesis
acf test H122.1 --data path/to/evaluation-data/

# Test all hypotheses
acf test --all --data path/to/evaluation-data/

# View hypothesis details
acf query "SELECT ?id ?label ?target WHERE {
  ?h a acf:Hypothesis ; acf:id ?id ; rdfs:label ?label ; acf:target ?target .
}"
```

## Status Tracking

Hypothesis evaluation results are stored as experiment-run records with `hypothesis_id` fields, enabling longitudinal tracking of evidence accumulation across system versions.
