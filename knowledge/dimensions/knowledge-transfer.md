---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#KnowledgeTransfer> a acf:Dimension ;
    acf:id "knowledge-transfer" ;
    acf:label "Knowledge Transfer (Modular Capability)" ;
    acf:shortName "KTR" ;
    acf:subLevelCount 4 ;
    acf:weight 0.06 ;
    acf:description "Measures whether domain competence is a loadable/unloadable modular unit whose presence is attributable to a loaded module rather than latent in the core. As AI systems acquire competence by loading executable capability modules (COG-style units carrying knowledge and code), a distinct, measurable property appears: loading the module confers the domain competence, unloading it removes the competence cleanly — the same queries then yield competence-envelope right-reason abstentions rather than confabulation — and the differential is attributable to the module, not the core. This is a capability-transfer axis, orthogonal to compositional recombination of primitives (Compositional Generalization) and to knowing one's limits (GBA)." .

<#KTR1> a acf:SubLevel ;
    acf:id "KTR1" ;
    acf:dimension <#KnowledgeTransfer> ;
    acf:level 1 ;
    acf:label "Load-Time Capability Acquisition" ;
    acf:scoreRange "0-25" ;
    acf:description "Loading a capability module measurably adds the domain competence the module declares: with the module loaded the system performs module-domain tasks (P1/P2/P4-class queries) that it could not perform before the load. Capability is acquired at load time, not baked into the core." .

<#KTR2> a acf:SubLevel ;
    acf:id "KTR2" ;
    acf:dimension <#KnowledgeTransfer> ;
    acf:level 2 ;
    acf:label "Unload Abstention (Competence Envelope)" ;
    acf:scoreRange "25-50" ;
    acf:description "Unloading the module removes the competence cleanly: the SAME queries that succeeded with the module loaded now yield competence-envelope right-reason abstentions — the system says it is outside its loaded competence rather than confabulating. Without the module the hallucinated-domain-answer rate is 0; abstention is the correct behaviour, not silence and not a guess." .

<#KTR3> a acf:SubLevel ;
    acf:id "KTR3" ;
    acf:dimension <#KnowledgeTransfer> ;
    acf:level 3 ;
    acf:label "Module-Attributable Differential" ;
    acf:scoreRange "50-75" ;
    acf:description "The load/unload differential is provably attributable to the loaded module, not latent in the core. A registry switch that merely claims a module is present, or a faked load, does not reproduce the competence: the capability rides in the module. The differential is reproducible and ~total — competence with the module, abstention without it." .

<#KTR4> a acf:SubLevel ;
    acf:id "KTR4" ;
    acf:dimension <#KnowledgeTransfer> ;
    acf:level 4 ;
    acf:label "Provable Inter-Agent Transfer" ;
    acf:scoreRange "75-100" ;
    acf:description "Capability transfers between agents by moving the module: a second agent that loads the same signed module acquires the same domain competence with the same attribution and the same unload-abstention guarantee, auditably and reproducibly. Under adversarial probing — faked loads, registry switches, hidden core dependence — the module-attributable differential holds and the unloaded hallucinated-domain-answer rate stays 0." .
---

# Knowledge Transfer (Modular Capability)

Knowledge Transfer measures a property that only becomes meaningful once a system acquires competence by **loading executable modules** — units that carry both knowledge and code and can be transferred between agents. In such systems a new, testable question appears: **is a domain competence a loadable/unloadable unit whose presence is attributable to the module, or is it latent in the core?** A system whose competence is a hot-swappable, attributable module is a fundamentally different — and more auditable — kind of system than one whose capabilities are an inseparable monolith.

This dimension is deliberately **orthogonal** to the two dimensions it is most often confused with. It is not Compositional Generalization (CG): CG is about recombining known *primitives* into novel compositions, whereas Knowledge Transfer is about acquiring — and cleanly relinquishing — a whole domain competence as a loadable unit. It is not Generalization Boundary Awareness (GBA): GBA is the metacognitive property of knowing what one does not know and abstaining. Knowledge Transfer *uses* that abstention as its unload signal (KTR2), but the axis it measures is the **transfer and attribution** of modular capability, not boundary awareness in general. Forcing modular capability transfer into either existing dimension distorts the framework; it earns its own.

The four sub-levels progress from a single load event to a provable inter-agent transfer guarantee. At **KTR1 (Load-Time Capability Acquisition)** the system does the basic thing: loading a module measurably adds the domain competence the module declares — tasks that failed before the load now succeed. Capability is acquired at load time, not pre-baked into the core.

**KTR2 (Unload Abstention)** hardens the guarantee on the *other* side of the load. Unloading the module must remove the competence cleanly: the same queries that just succeeded now yield competence-envelope right-reason abstentions, and the unloaded hallucinated-domain-answer rate is 0. A system that keeps answering module-domain questions after the module is gone — from residual, unattributable core knowledge — fails KTR2, because its competence was never really the module's.

**KTR3 (Module-Attributable Differential)** rules out the cheap fake. A registry switch that flips a "loaded" flag, or a stubbed load that does no real work, must not reproduce the competence. At KTR3 the load/unload differential is provably attributable to the module itself — it is reproducible and ~total (competence with, abstention without), and it survives an attempt to fake the load.

At **KTR4 (Provable Inter-Agent Transfer)** the property becomes a transfer guarantee. Moving the signed module to a second agent confers the same competence, with the same attribution and the same unload-abstention behaviour, auditably. The test of KTR4 is adversarial: under faked loads, registry switches, and probes for hidden core dependence — including a fresh agent that has never seen the domain — the module-attributable differential holds and the unloaded hallucinated-domain-answer rate stays 0.
