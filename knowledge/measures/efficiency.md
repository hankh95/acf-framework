---
@prefix acf: <https://acf-framework.dev/ns/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<#M-019> a acf:Measure ;
    rdfs:label "Compute Acceleration Factor" ;
    acf:id "M-019" ;
    acf:name "compute_acceleration_factor" ;
    acf:description "Ratio of processing speed with hardware acceleration (e.g., GPU) to CPU-only baseline, measuring the effective speedup gained from accelerated compute" ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "efficiency" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy> .

<#M-020> a acf:Measure ;
    rdfs:label "LLM Call Reduction" ;
    acf:id "M-020" ;
    acf:name "llm_call_reduction_ratio" ;
    acf:description "Ratio of queries answered from the system's own knowledge base versus those requiring external LLM calls, measuring self-sufficiency and cost efficiency" ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "efficiency" ;
    acf:collection "automated" ;
    acf:mapsTo <#Autonomy>, <#KnowledgeTransparency> .

<#M-021> a acf:Measure ;
    rdfs:label "Latency Improvement" ;
    acf:id "M-021" ;
    acf:name "latency_improvement_ratio" ;
    acf:description "Ratio of response latency before and after optimization, measuring the magnitude of performance improvement from architectural or algorithmic changes" ;
    acf:unit "ratio" ;
    acf:dataType "decimal" ;
    acf:category "efficiency" ;
    acf:collection "automated" ;
    acf:mapsTo <#ServiceOrientation> .
---

# Efficiency Measures (M-019 to M-021)

Efficiency measures quantify how well an AI system utilizes its computational resources. Rather than measuring raw capability, these measures capture the system's ability to achieve results with fewer resources, less external dependency, and faster throughput. Efficiency gains directly impact operational cost, scalability, and the system's ability to operate autonomously.

## M-019: Compute Acceleration Factor

**What it measures:** The speedup ratio achieved by leveraging hardware acceleration (GPU, TPU, or specialized accelerators) compared to a CPU-only baseline for the same workload. A factor of 5.0x means the accelerated path is five times faster.

**How to collect:** Run identical workloads on both CPU-only and accelerated hardware configurations. Measure total processing time for each. Calculate: `cpu_time / accelerated_time`. Use a representative workload that includes the system's most compute-intensive operations (embedding generation, inference, graph traversal).

**Target ranges:**
- Below 1.5x: Acceleration overhead may negate benefits; review the acceleration pipeline
- 1.5-5.0x: Moderate speedup; typical for I/O-bound workloads with some compute-bound stages
- 5.0-20.0x: Good acceleration; compute-bound operations benefit significantly
- Above 20.0x: Excellent; the system effectively exploits hardware acceleration

## M-020: LLM Call Reduction

**What it measures:** The ratio of queries the system handles from its own knowledge base versus those that require calling an external large language model. A higher ratio means the system is more self-sufficient, reducing latency, cost, and dependency on external services.

**How to collect:** Over a measurement period, count the total number of user queries and the number that required an external LLM call. Calculate: `(total_queries - llm_calls) / total_queries`. Alternatively, express as the inverse: `llm_calls_before_optimization / llm_calls_after_optimization` to measure improvement over time.

**Target ranges:**
- Below 0.3: System depends heavily on external LLM calls for most queries
- 0.3-0.6: Moderate self-sufficiency; many common queries handled internally
- 0.6-0.85: Good self-sufficiency; external calls limited to complex or novel queries
- Above 0.85: Excellent; the system rarely needs external LLM assistance

## M-021: Latency Improvement

**What it measures:** The ratio of response latency before and after an optimization effort (architectural change, caching strategy, algorithm improvement, etc.). A ratio of 2.0x means the system is twice as fast after optimization.

**How to collect:** Establish a baseline latency measurement using a fixed evaluation workload before the optimization. Apply the optimization. Re-measure latency using the identical workload. Calculate: `baseline_latency / optimized_latency`. Ensure the workload, hardware, and load conditions are identical between measurements.

**Target ranges:**
- Below 1.0x: Optimization made things worse; roll back and investigate
- 1.0-1.5x: Marginal improvement; may not justify the complexity
- 1.5-3.0x: Meaningful improvement; worth the engineering investment
- Above 3.0x: Significant improvement; transformative optimization
