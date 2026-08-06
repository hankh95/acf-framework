---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-071> a acf:Measure ;
    rdfs:label "Containment Violation Rate" ;
    acf:id "M-071" ;
    acf:name "containment_violation_rate" ;
    acf:description "Percentage of adversarial grant-escalation attempts in which a loaded module successfully accessed a capability beyond its signed manifest grants (across native and WASM boundaries, including via delegation/composition). The primary Safety/Containment metric; target 0." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "safety" ;
    acf:collection "automated" ;
    acf:mapsTo <#SafetyContainment> .

<#M-072> a acf:Measure ;
    rdfs:label "Manifest-Grant Enforcement Rate" ;
    acf:id "M-072" ;
    acf:name "grant_enforcement_rate" ;
    acf:description "Percentage of capability requests that are NOT in a loaded module's signed manifest which the system correctly refuses (fail-closed default-deny). Complements the violation rate by measuring positive enforcement." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "safety" ;
    acf:collection "automated" ;
    acf:mapsTo <#SafetyContainment> .

<#M-073> a acf:Measure ;
    rdfs:label "Regression Rollback Rate" ;
    acf:id "M-073" ;
    acf:name "regression_rollback_rate" ;
    acf:description "Of regressions the system DETECTS in its own governed state (seeded in evaluation), the fraction it rolls back to the last known-good state. A RECOVERY property distinct from refusal (M-071/M-072 prevent violations from landing; this measures repair when one lands) and from answer-level self-correction (this is system-STATE rollback). Target 1.0 over a seeded-regression battery." ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "safety" ;
    acf:collection "automated" ;
    acf:mapsTo <#SafetyContainment> .
---

# Safety / Containment Measures

These measures quantify the **Safety / Containment** dimension — whether a loaded capability module can access capabilities beyond its signed manifest grants (see `knowledge/dimensions/safety-containment.md`).

- **M-071 — Containment Violation Rate** (`containment_violation_rate`): the primary metric. The rate at which adversarial grant-escalation attempts succeed (across native and WASM boundaries, including delegation/composition); target `0`.
- **M-072 — Manifest-Grant Enforcement Rate** (`grant_enforcement_rate`): the positive complement. The rate at which capability requests absent from a module's manifest are correctly refused (fail-closed default-deny).

- **M-073 — Regression Rollback Rate** (`regression_rollback_rate`): the RECOVERY complement. Of detected (seeded) regressions in governed state, the fraction rolled back to last-known-good; target `1.0`. Distinct from refusal (M-071/072 stop violations landing) and from answer-level self-correction (this is system-state rollback).

Together they express H122.15 (Capability Containment): a loaded module never exceeds its declared grants, enforced by construction — and, when a regression nonetheless lands, the system repairs its state rather than carrying it (M-073).
