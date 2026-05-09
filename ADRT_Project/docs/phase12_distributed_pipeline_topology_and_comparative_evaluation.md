# Phase 12: Distributed Pipeline Topology & Comparative Evaluation

This phase explicitly formalizes the framework's capability to model bounded distributed failure phenomena, topology-aware resilience semantics, and journal-grade comparative evaluation methodologies.

The framework asserts its academic positioning as: *"A bounded stochastic cyber-physical resilience abstraction framework for tractable SMC experimentation of distributed oil pipeline attack-defense-response-recovery dynamics under operational uncertainty."*

## 1. True Operational Differentiation
Previously, generic attack vectors were relabeled to pipeline concepts without sufficient behavioral differences. Phase 12 injected mathematically distinct bounds-logic into the transition states:
*   **`SCADA_Compromise`**: Aggressively degrades `localizedTelemetryTrust_A` by a factor of 20 and propagates immediately to `delayedTelemetry`.
*   **`PLC_Logic_Manipulation`**: Accelerates `processDeviation` bounds significantly faster than generic malware, representing immediate physical feedback loop corruption.
*   **`Malicious_Valve_Actuation`**: Directly escalates `controlLatency` and localized `segmentStress_A`, representing downstream starvation or upstream overpressure.

## 2. Distributed Pipeline Topology Semantics
The framework introduced lightweight, bounded topology variables reflecting a segmented architecture without necessitating infinite-state Geographic Information Systems (GIS) routing.
*   **Segment Stress Mapping:** `segmentStress_A`, `segmentStress_B`
*   **Localized Trust Mapping:** `localizedTelemetryTrust_A`, `localizedTelemetryTrust_B`
*   **Asset Health:** `compressorHealth_A`

## 3. Localized Degradation & Recovery
*   **Cascading Instability:** Through bounded ternary logic, high instability in one segment naturally spills downstream. `segmentStress_B=(segmentStress_A>=70)?min(100, segmentStress_B+10):segmentStress_B`. This permits finite-state distributed cascading failures.
*   **Segmented Recovery:** `Pipeline_Incident_Response` now incorporates isolation abstractions via `segmentShutdown_A`. Recovery actions no longer magically heal the entire geometry but can perform segmented operational shutdowns to preserve bounded global survivability.

## 4. Advanced Comparative Evaluation Framework
To support journal-grade publication metrics, comparative operational flags were introduced (`congestionAwareDefense`, `telemetryAwareDefense`).
These allow direct baseline comparisons natively inside the SMC:
*   *Congestion-Aware vs. Non-Congestion Aware Defenses*
*   *Telemetry-Aware Defense vs. Basic Defense*

## 5. Statistical Experimentation Runner
The automation scaffolding (`scripts/experiment_runner.py`) was entirely overhauled.
*   **Statistical Outputs:** Automatically computes mean degradation, variance, and 95% Confidence Intervals over repeated stochastic SMC iterations.
*   **Traceability & Reproducibility:** Every run generates timestamped metadata logs, raw trace datasets, and structured CSV files tracking comparative parameter sweeps perfectly suited for academic plotting suites.

## 6. Empirical Grounding & Methodology Limitations
To prevent false equivalencies, the methodology formally documents the empirical grounding abstraction:
*   *`telemetryTrust`* is NOT an empirically calibrated Modbus packet-loss tracker. It is a synthetic bounded abstraction of SCADA reliability approximation.
*   *`controlLatency`* bounds approximate PLC cycle lag but do not map identically to real-world continuous latency distributions.
*   *`segmentStress`* is a reduced-order pressure/fatigue model.

The framework trades infinite continuous precision for guaranteed statistical tractability and bounds safety, meaning any direct deployment to real hardware necessitates prior calibration of these parameters against true industrial PCAP profiles.
