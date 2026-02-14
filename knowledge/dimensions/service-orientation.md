---
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix acf: <https://acf-framework.dev/ns/> .

<#ServiceOrientation> a acf:Dimension ;
    acf:id "service-orientation" ;
    acf:label "Service Orientation" ;
    acf:shortName "SO" ;
    acf:subLevelCount 4 ;
    acf:weight 0.111 ;
    acf:description "Measures task completion capability and user trust calibration. Service Orientation captures how effectively an agent serves its users, from basic question-answering through professional-grade service with well-calibrated trust." .

<#SO1> a acf:SubLevel ;
    acf:id "SO1" ;
    acf:dimension <#ServiceOrientation> ;
    acf:level 1 ;
    acf:label "Basic Q&A" ;
    acf:scoreRange "0-25" ;
    acf:description "Basic question-and-answer capability. The agent can respond to direct questions with relevant information but lacks contextual awareness or task-oriented behavior." .

<#SO2> a acf:SubLevel ;
    acf:id "SO2" ;
    acf:dimension <#ServiceOrientation> ;
    acf:level 2 ;
    acf:label "Task-Oriented Responses" ;
    acf:scoreRange "25-50" ;
    acf:description "Task-oriented responses with context awareness. The agent understands the user's goal behind a question and shapes its response to advance that goal, maintaining conversational context." .

<#SO3> a acf:SubLevel ;
    acf:id "SO3" ;
    acf:dimension <#ServiceOrientation> ;
    acf:level 3 ;
    acf:label "Reliable Task Completion" ;
    acf:scoreRange "50-75" ;
    acf:description "Reliable task completion with explanations. The agent consistently completes requested tasks, explains its approach and reasoning, and proactively surfaces relevant information." .

<#SO4> a acf:SubLevel ;
    acf:id "SO4" ;
    acf:dimension <#ServiceOrientation> ;
    acf:level 4 ;
    acf:label "Professional-Grade Service" ;
    acf:scoreRange "75-100" ;
    acf:description "Professional-grade service with trust calibration. The agent delivers expert-level task completion, communicates confidence appropriately, manages user expectations, and builds warranted trust through consistent reliability." .
---

# Service Orientation

Service Orientation measures how effectively an agent serves the needs of its users and completes real-world tasks. While other dimensions focus on what an agent knows or how it reasons, Service Orientation focuses on the practical outcome: does the agent actually help? This dimension bridges the gap between cognitive capability and user value.

The four sub-levels (SO1 through SO4) trace a progression from passive information retrieval to proactive professional service. At SO1, the agent functions as a basic question-answering system — it can respond to direct queries with relevant information, but it treats each question in isolation without understanding the user's broader goals or maintaining meaningful context across interactions.

SO2 introduces task orientation: the agent recognizes that questions are usually asked in service of a larger goal and shapes its responses accordingly. It maintains conversational context, asks clarifying questions when needed, and provides information in a format that helps the user make progress on their actual task rather than just answering the literal question.

At SO3, the agent becomes a reliable task-completion partner. It consistently delivers on requests, explains its approach so users can evaluate and build on the results, and proactively surfaces information that the user might need but did not explicitly ask for. The key attribute at this level is reliability — users can depend on the agent to follow through.

SO4 represents professional-grade service with sophisticated trust calibration. The agent not only completes tasks at an expert level but also manages the trust relationship with its users. It communicates confidence levels honestly, sets appropriate expectations about what it can and cannot do, and builds warranted trust through a track record of consistent, transparent performance. At this level, the agent functions as a trusted professional colleague rather than a tool.
