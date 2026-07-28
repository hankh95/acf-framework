---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-073> a acf:Measure ;
    rdfs:label "Load/Unload Differential" ;
    acf:id "M-073" ;
    acf:name "load_unload_differential" ;
    acf:description "The domain-competence delta on module-domain tasks between the module loaded and the module unloaded (module-loaded task-success minus module-unloaded task-success), where the module-unloaded arm must collapse to abstention. The differential counts only when it is attributable to the module: a registry switch or a faked load that reproduces the competence scores 0. The primary Knowledge Transfer metric; target near-total (>= 0.9 at KTR4)." ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "knowledge-transfer" ;
    acf:collection "automated" ;
    acf:mapsTo <#KnowledgeTransfer> .

<#M-074> a acf:Measure ;
    rdfs:label "Unloaded Hallucination Rate" ;
    acf:id "M-074" ;
    acf:name "unloaded_hallucination_rate" ;
    acf:description "Percentage of module-domain queries that receive a confabulated (hallucinated) domain answer when the module is UNLOADED, instead of a competence-envelope right-reason abstention. Complements the differential by verifying the unload side is a clean abstention rather than residual, unattributable core knowledge; target 0." ;
    acf:unit "percent" ;
    acf:dataType "decimal" ;
    acf:category "knowledge-transfer" ;
    acf:collection "automated" ;
    acf:mapsTo <#KnowledgeTransfer> .
---

# Knowledge Transfer Measures

These measures quantify the **Knowledge Transfer (Modular Capability)** dimension — whether domain competence is a loadable/unloadable modular unit attributable to the module (see `knowledge/dimensions/knowledge-transfer.md`).

- **M-073 — Load/Unload Differential** (`load_unload_differential`): the primary metric. The competence delta between the module loaded and unloaded, counted only when attributable to the module (a faked load scores 0). Target near-total (`>= 0.9` at KTR4).
- **M-074 — Unloaded Hallucination Rate** (`unloaded_hallucination_rate`): the guardrail. The rate at which the system confabulates a domain answer when the module is unloaded instead of abstaining; target `0`.

Together they express H122.16 (Capability Transfer): a real modular capability confers competence on load and yields clean, right-reason abstention on unload — not residual confabulation.
