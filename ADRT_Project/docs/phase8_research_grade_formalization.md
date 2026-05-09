# Phase 8: Research-Grade Formalization and Stochastic Grounding

This phase completes the transition of the ADRT framework from a heuristic cybersecurity simulator into a defensible bounded stochastic cyber-physical resilience abstraction framework suitable for tractable SMC experimentation. 

## 1. Removal of Naive RPG-Like Semantics
The legacy "+1/-1 leveling" defense attributes have been structurally replaced with operational capabilities:
*   `fw_strength` -> `detectionReliability`
*   `ids_strength` -> `telemetryCoverage`
*   `waf_strength` -> `inspectionDepth`
*   `edr_strength` -> `modelFidelity`
*   `dlp_strength` -> `mitigationEffectiveness`

These variables now exhibit bounded asymptotic recovery (`min(100, variable + 5)`) under continuous defense engagement, effectively modeling gradual operational improvement rather than discrete level-ups.

## 2. Abstraction of Arbitrary Thresholds
Queue logic has been decoupled from rigid magic numbers (e.g., `queue < 80`). The `80` threshold has been explicitly formalized as `mitigationCapacity`. Operational stress dynamics now scale continuously relative to bounded thresholds (`congestionPressure`, `servicePressure`, `inspectionBacklog`), grounding congestion effects in experimentally justifiable service saturation rather than arbitrary packet limits.

## 3. Stochastic Grounding
Probabilistic decision nodes (branch points and stochastic edges) now dynamically compute their weights from the operational state rather than fixed constants:
*   **Attack Success** dynamically bounds against: `stealthPreference + congestionPressure`
*   **Defense Mitigation** dynamically scales by: `mitigationConfidence + telemetryTrust`
*   **Cyber-Physical Disruption** leverages continuous abstraction ratios: `stealthPreference + processDeviation` versus `mitigationConfidence + controlLoopStability`.

This fulfills the requirement that probabilities emerge from system state rather than manual, unexplainable constants, while avoiding computationally intractable continuous-time Bayesian inference systems. 

## 4. Cyber-Physical Semantics (CPS) Abstractions
The framework introduces a suite of reduced-order CPS abstraction variables:
*   `controlLatency`
*   `actuatorInconsistency`
*   `delayedTelemetry`
*   `sensorDisagreement`
*   `processStabilizationLag`

Instead of deploying exact nonlinear PDE solvers or physical digital twins, physical system deterioration is modeled as cascading operational bounds. For example, telemetry degradation automatically induces secondary penalties to `delayedTelemetry` and `sensorDisagreement`, organically cascading into `operationalSafetyErosion`.

## 5. Formal Tractability Verification
All dynamic calculations use strictly bounded integer spaces (`int[0,100]`), retaining complete compatibility with the UPPAAL SMC memory model. We completely avoided infinite state generation, cyclic non-terminating solvers, and exact ODE graphing.

## 6. Threats to Validity
The following threats must be acknowledged when writing subsequent research papers:
*   **Internal Validity:** The system models abstraction bounds (e.g., continuous service degradation) using reduced-order queue semantics rather than exact packet-by-packet fluid simulations.
*   **External Validity:** Real industrial telemetry logs have not been explicitly cross-calibrated against these variables. The framework demonstrates *theoretical behavioral topology* rather than *physical topological accuracy*. 
*   **Computational Validity:** By enforcing finite-state tractability for UPPAAL verification, we intentionally compress infinite-horizon recovery logic into sequential finite stages. 

### Final Experimental Positioning
The framework is now strictly positioned as **"A bounded stochastic cyber-physical resilience abstraction framework for tractable SMC experimentation of attack-defense-response-recovery dynamics under operational uncertainty."** It does not claim digital twin fidelity, but serves as a rigorous, interpretable statistical bounds checker for resilience engineering.
