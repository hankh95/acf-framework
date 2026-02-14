---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-011> a acf:Measure ;
    rdfs:label "Processing Path Latency (P95)" ;
    acf:id "M-011" ;
    acf:name "processing_path_latency_p95_ms" ;
    acf:description "95th percentile latency for the system's primary processing path, from query receipt to response generation start" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-012> a acf:Measure ;
    rdfs:label "Parallel Assessment Ratio" ;
    acf:id "M-012" ;
    acf:name "parallel_assessment_ratio" ;
    acf:description "Ratio of parallel processing utilization to sequential processing, measuring how effectively the system leverages concurrent assessment pipelines" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-013> a acf:Measure ;
    rdfs:label "Knowledge Query Latency" ;
    acf:id "M-013" ;
    acf:name "knowledge_query_latency_ms" ;
    acf:description "Average time to execute a structured query against the system's knowledge graph or knowledge base and return results" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-014> a acf:Measure ;
    rdfs:label "Vector Search Latency" ;
    acf:id "M-014" ;
    acf:name "vector_search_latency_ms" ;
    acf:description "Average time to perform a vector similarity search across the system's embedding store, from query embedding to ranked result return" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-015> a acf:Measure ;
    rdfs:label "Total Response Latency" ;
    acf:id "M-015" ;
    acf:name "total_response_latency_ms" ;
    acf:description "Total time from query receipt to the completion of the system's response, including all internal processing stages but excluding network transport" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-016> a acf:Measure ;
    rdfs:label "End-to-End Response Time" ;
    acf:id "M-016" ;
    acf:name "end_to_end_response_time_ms" ;
    acf:description "Wall-clock time from user query submission to response delivery, including network transport, queuing, processing, and rendering" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .

<#M-017> a acf:Measure ;
    rdfs:label "Reasoning Pipeline Latency" ;
    acf:id "M-017" ;
    acf:name "reasoning_pipeline_latency_ms" ;
    acf:description "Time spent in the system's reasoning pipeline, including inference, chain-of-thought construction, and logical deduction stages" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#FormalReasoning>, <#ServiceOrientation> .

<#M-018> a acf:Measure ;
    rdfs:label "Decision Latency" ;
    acf:id "M-018" ;
    acf:name "decision_latency_ms" ;
    acf:description "Time from the availability of all relevant signals to the system's final action or response decision" ;
    acf:unit "milliseconds" ;
    acf:dataType "decimal" ;
    acf:category "latency" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy>, <#ServiceOrientation> .
---

# Latency Measures (M-011 to M-018)

Latency measures capture the time performance of an AI system's processing pipeline. Fast, predictable response times are critical for user experience, real-time applications, and system scalability. These measures track latency at multiple granularities: individual pipeline stages, end-to-end response time, and the decision-making layer.

## M-011: Processing Path Latency (P95)

**What it measures:** The 95th percentile latency for the system's primary processing path, measured from query receipt to the point where response generation begins. The P95 metric captures worst-case typical performance, excluding extreme outliers.

**How to collect:** Instrument the processing pipeline entry and exit points. Record latency for every query over a measurement window (minimum 1,000 queries recommended). Sort latencies and report the 95th percentile value.

**Target ranges:**
- Above 2,000ms: Unacceptable for interactive use
- 500-2,000ms: Adequate for background or batch processing
- 100-500ms: Good for interactive applications
- Below 100ms: Excellent; enables real-time conversational interaction

## M-012: Parallel Assessment Ratio

**What it measures:** The ratio of wall-clock time for parallel processing versus the sum of individual sequential processing times. This measures how effectively the system leverages concurrency when multiple assessments, evaluations, or signal-gathering operations can execute simultaneously.

**How to collect:** Measure the total sequential time (sum of all individual assessment durations) and the actual wall-clock time (with parallel execution). Calculate: `actual_wall_time / sequential_sum_time`. A ratio approaching `1/N` (where N is the number of parallel paths) indicates perfect parallelization.

**Target ranges:**
- Above 80% of sequential time: Minimal parallelization benefit
- 40-80%: Some parallelization, but bottlenecks remain
- 20-40%: Good parallel utilization
- Below 20%: Excellent; near-optimal parallel execution

## M-013: Knowledge Query Latency

**What it measures:** The average time to execute a structured query (e.g., SPARQL, graph traversal, or SQL) against the system's knowledge store and return results.

**How to collect:** Instrument the knowledge query interface. Record latency for each query, including parsing, execution, and result serialization. Report the average and P95 over a representative query workload.

**Target ranges:**
- Above 500ms: Knowledge store is a bottleneck; consider indexing or caching
- 100-500ms: Acceptable for moderate-complexity queries
- 10-100ms: Good performance for most knowledge retrieval patterns
- Below 10ms: Excellent; knowledge is highly optimized for query performance

## M-014: Vector Search Latency

**What it measures:** The average time to perform a vector similarity search across the system's embedding store, from computing the query embedding through returning ranked results.

**How to collect:** Instrument the vector search pipeline. Measure time from query text input to ranked result output. Include embedding computation time. Report average and P95 over a representative query set.

**Target ranges:**
- Above 200ms: Vector search is a performance bottleneck
- 50-200ms: Acceptable for non-real-time applications
- 10-50ms: Good performance for interactive use
- Below 10ms: Excellent; suitable for real-time applications with high query volume

## M-015: Total Response Latency

**What it measures:** The total server-side processing time from query receipt to response completion, including all internal stages (routing, retrieval, reasoning, generation) but excluding network transport time.

**How to collect:** Record timestamps at query receipt and response completion on the server side. Calculate the difference. Report average, P50, P95, and P99.

**Target ranges:**
- Above 5,000ms: Too slow for interactive use; consider architectural optimization
- 1,000-5,000ms: Acceptable for complex queries requiring multi-step reasoning
- 200-1,000ms: Good for typical interactive applications
- Below 200ms: Excellent; enables fluid, conversational interaction

## M-016: End-to-End Response Time

**What it measures:** The complete wall-clock time experienced by the user, from query submission to response delivery. This includes all server-side processing, network round-trips, queue wait times, and any client-side rendering.

**How to collect:** Instrument at the client or API gateway level. Record the timestamp when the query is submitted and when the complete response is received. Calculate the difference. Report average, P50, P95, and P99.

**Target ranges:**
- Above 10,000ms: Poor user experience; users will abandon interactions
- 2,000-10,000ms: Tolerable for complex tasks where users expect a wait
- 500-2,000ms: Good for most interactive applications
- Below 500ms: Excellent; feels instantaneous to users

## M-017: Reasoning Pipeline Latency

**What it measures:** The time spent specifically in the reasoning pipeline, including logical inference, chain-of-thought construction, multi-step deduction, and any formal proof steps. This isolates reasoning performance from retrieval and generation.

**How to collect:** Instrument the reasoning pipeline entry and exit points. Record latency for each reasoning invocation. Categorize by reasoning complexity (single-step vs. multi-step) if possible.

**Target ranges:**
- Above 3,000ms: Reasoning is the dominant bottleneck
- 500-3,000ms: Acceptable for complex multi-step reasoning tasks
- 100-500ms: Good for most reasoning scenarios
- Below 100ms: Excellent; reasoning adds minimal overhead

## M-018: Decision Latency

**What it measures:** The time from the point where all relevant signals and evidence are available to the system's final action or response decision. This measures the efficiency of the decision-making layer itself, independent of information-gathering time.

**How to collect:** Instrument the decision function or module. Record the timestamp when all input signals are ready and when the decision is emitted. Calculate the difference.

**Target ranges:**
- Above 500ms: Decision layer is a bottleneck; consider simplifying the decision model
- 100-500ms: Acceptable for decisions involving multiple weighted signals
- 10-100ms: Good performance for real-time decision-making
- Below 10ms: Excellent; near-instantaneous decisions
