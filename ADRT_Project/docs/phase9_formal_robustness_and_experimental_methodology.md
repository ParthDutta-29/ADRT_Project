# Phase 9: Formal Robustness & Experimental Methodology

This document outlines the Phase 9 transformation of the ADRT framework into a rigorous, publication-ready **bounded stochastic cyber-physical resilience abstraction framework for tractable SMC experimentation of attack-defense-response-recovery dynamics under operational uncertainty.**

> **Note on Research Positioning:** The framework does NOT attempt digital twin realism, exact industrial emulation, perfect continuous-time process modeling, or empirically validated industrial equivalence. Instead, it provides a strictly bounded finite-state abstraction of cyber-physical resilience dynamics suitable for tractable Statistical Model Checking (SMC).

## 1. Formal Probability Governance

To enforce formal stochastic consistency across UPPAAL SMC branch choices, absolute probabilistic increments (which risked stochastic dominance and state explosion) were systematically replaced with **normalized bounded relative weights**.

*   **Standardized Semantics:** Stochastic branches now strictly use bounded relative abstraction logic to represent weight advantages:
    *   `successWeight = 1 + telemetryTrust/25 + detectionReliability/20`
    *   `failureWeight = 1 + congestionPressure/20 + operationalStress/25`
*   This approach guarantees UPPAAL trace generators encounter smoothly bounded probabilities strictly driven by operational factors, explicitly eliminating zero-probability lockups and arbitrary integer overflows.

## 2. True Nonlinear Saturation Semantics

Residual linear parameter growth (e.g., `x = min(100, x + 5)`) was structurally eliminated. The framework now enforces genuine saturation logic matching asymptotic dynamics:

*   **Bounded Improvement Patterns:** `x = min(100, x + (100 - x)/10)`
    *   Growth naturally slows as metrics approach upper limits (e.g., trust limits, resilience ceilings), representing diminishing returns on mitigations.
*   **Bounded Degradation Envelopes:** `x = max(0, x - (operationalStress/10))`
    *   Declines dynamically accelerate or decelerate relative to existing systemic stress, mirroring material fatigue or operational bandwidth exhaustion without relying on complex, SMC-violating ODE solvers.

## 3. ICS-Specific Operational Grounding

The abstract elements of the framework are explicitly grounded toward a **Water Treatment ICS** deployment abstraction. Rather than renaming internal syntax (to preserve XML parser continuity), variables are mapped to operationally sound interpretations in this domain:

| Variable Identifier | Operational Abstraction Interpretation (Water Treatment) |
| :--- | :--- |
| `telemetryIntegrity` | Sensor Packet Consistency (e.g., pressure sensors, pH meters) |
| `processDeviation` | Dosing/Flow Deviation (e.g., over-chlorination, tank overflow) |
| `controlLatency` | Programmable Logic Controller (PLC) Response Lag |
| `safeModeOperation` | Manual Supervisory Fallback / Pump Shutoff Mode |
| `operationalStress` | Hydraulic Equipment Fatigue / Process Backpressure |

## 4. Sustainability-Aware Resilience (Energy & Carbon Semantics)

Resilience carries a direct cost. Phase 9 formalized bounds for sustainability overhead:

*   **Congestion-Induced Escalation:** Maintenance and energy expenditures scale directly with `congestionPressure`, meaning attacks targeting queues intrinsically degrade the sustainability envelope (`maintenanceCost + FWD_MC + congestionPressure/10`).
*   **Bounded Cost Accrual:** Total operational overhead evaluates bounded variables representing the environmental impact (Energy, Carbon) and financial load during mitigation and safe-mode recovery orchestration.

## 5. Formal Computational Validity Architecture

A structured, fully automated Python-based verification toolchain (`phase9_formal_verification.py`) has been embedded into the repository logic. It programmatically validates:

1.  **Underflow/Overflow Detection:** Disallows arbitrary integer manipulation outside defined saturating bounds.
2.  **Parser Safety:** Flags malformed `? :` ternary blocks, hanging XML expressions, or broken operators.
3.  **Invalid Branch Weights:** Flags illegal expressions in UPPAAL probability labels.
4.  **Saturating Guard Checks:** Ensures finite-state integers never expand unboundedly over loops.

## 6. Formal Experimental Methodology

The framework now natively supports highly reproducible verification categories through its extended UPPAAL `scalability_tests.q`:

*   **Sensitivity Analysis:** How `mitigationCapacity` inversely affects `processDeviation`.
*   **Congestion Collapse Analysis:** Checking state probability under severe `congestionPressure`.
*   **Survivability Trajectory Assessment:** Testing the likelihood of `operationalSafetyErosion > 50` while locked in `safeModeOperation`.
*   **Sustainability Tradeoff Analysis:** Checking whether `carbonCost` thresholds are breached during prolonged mitigation states.

### Calibration & Realism Limitations
To achieve SMC tractability, this framework accepts necessary limitations. It simplifies the underlying physical layer without utilizing high-dimensional Bayesian belief networks or continuous fluid-dynamic ODE models. Direct deployment to production ICS systems would require empirical calibration of relative transition weights against authentic network traffic traces and PLC logging behavior.
