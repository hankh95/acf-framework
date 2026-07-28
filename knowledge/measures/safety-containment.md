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
