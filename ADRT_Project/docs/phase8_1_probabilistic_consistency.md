# Phase 8.1: Probabilistic Consistency, Asymptotic Dynamics & Parameter Formalization

This stabilization pass explicitly addresses statistical correctness, parameter semantics, and the eradication of remaining linear heuristic artifacts to complete the framework's mathematical rigor.

## 1. Probabilistic Branch Semantics Repaired
Previous probability expressions (e.g., `detectionReliability + telemetryTrust`) mathematically represented invalid relative probability distributions by allowing weights to arbitrarily inflate into hundreds.
These labels have been refactored into **bounded relative stochastic weights** using normalization offsets:
*   `1 + detectionReliability/20 + telemetryTrust/25`
*   `1 + stealthPreference/25 + processDeviation/20`
*   `1 + congestionPressure/20 + operationalStress/25`

These normalized equations constrain branch weights into a roughly `1..10` range, guaranteeing formal semantic stability and avoiding extreme model dominance under UPPAAL SMC. The `+1` base acts as an operational floor ensuring absolute determinism is never reached (stochastic competition is preserved).

## 2. Asymptotic Operational Dynamics Implemented
Handcrafted linear dynamics such as `+5`, `+10`, and `-15` were identified as structurally heuristic. These have been rewritten into **bounded asymptotic dynamics**.
*   **Improvement diminishing returns:** `detectionReliability = min(100, detectionReliability + (100 - detectionReliability) / 10)` enforces progressively harder capability improvements rather than arbitrary RPG leveling.
*   **Stress scaling:** Variables like `processDeviation` and `controlLatency` now scale functionally off connected operational factors (`operationalStress / 10`, `(processDeviation + controlLatency) / 10`), simulating continuous interconnected service saturation.

## 3. Parameter Justification & Interpretability Framework
The framework variables represent **reduced-order stochastic abstractions**, not perfectly isomorphic physical parameters:
*   **`congestionPressure`**: Models the asymptotic failure boundary of sequential processing buffers. Essential for approximating network overhead without tracking exact packet queuing delays.
*   **`telemetryTrust`**: Represents the relative Bayesian confidence of operators reviewing incoming sensor data under stress. Used because explicit packet-level false-positive/negative inference requires computationally explosive Bayesian networks.
*   **`operationalStress`**: Represents holistic systemic degradation (fatigue, thermal load, backlog). Used as the continuous anchor point for stochastic mitigation decay.
*   **`controlLatency` & `processDeviation`**: Abstract physical momentum and fluid/thermal inertia. These allow the model to propagate latency feedback into recovery mechanisms without requiring nonlinear continuous ODE solvers.

## 4. Preservation of UPPAAL SMC Tractability
*   No exact queue theory (`M/M/1` or `G/G/1`) mathematics were hardcoded.
*   No floating-point mathematics were used (avoiding SMC floating-point explosions).
*   All parameters remain inside strictly bounded `int[0,100]` arithmetic spaces.
*   Calculations exist strictly as assignment transitions on discrete finite-state machines, guaranteeing linear state-space tractability.

## 5. Formal Validation Queries
New queries have been integrated into `validation/scalability_tests.q` to allow parameter sweeps and sensitivity experimentation. We test:
*   Asymptotic degradation (`detectionReliability > 80 && mitigationConfidence > 80`)
*   Delayed recovery persistence (`controlLatency > 50 && operationalSafetyErosion > 50`)
*   Operational stochastic competition (`processDeviation > 80 && safeModeOperation > 0`)

## 6. Research Positioning and Realism Limitations
This framework MUST be academically presented as: **"A bounded stochastic cyber-physical resilience abstraction framework for tractable SMC experimentation."**
*   **Limitation 1:** Recovery and congestion mathematically decay using discrete approximations rather than true continuous calculus. 
*   **Limitation 2:** Relative probability weights (like `/20` or `/25`) are heuristically tuned to guarantee stochastic spread for statistical model checking, rather than perfectly matching empirical observations. 
*   **Future Work:** High-tier journal publication would require empirical validation tuning (e.g., matching the probability curve of `mitigationEffectiveness / 20` against real SOC incident resolution times or specific PLC traversal logs).
