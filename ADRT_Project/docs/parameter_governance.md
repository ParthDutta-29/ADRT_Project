# Parameter Governance & Traceability Matrix

This document provides formal operational governance over key parameters used in the ADRT framework. This ensures interpretability, traceability, and tractability for statistical model checking.

## 1. Mitigation & Defense Parameters
| Parameter | Bounds | Operational Interpretation | Saturation / Resilience Rationale | Tractability Justification |
| :--- | :--- | :--- | :--- | :--- |
| `mitigationCapacity` | `[0,100]` | Total defensive orchestration bandwidth. | Subject to diminishing returns. High capacity reduces latency. | Replaces unbounded continuous processing constraints. |
| `congestionPressure` | `[0,100]` | Backlog and alert-queue stress on defenders. | Accumulates asymptotically via attacking; delays mitigations. | Avoids real-time queue-theoretic continuous modeling. |
| `detectionReliability` | `[0,100]` | Confidence that rules/signatures match threats. | Asymptotically scales `(100-x)/10`; never perfectly 100%. | Lightweight abstraction for Bayesian false-positive rates. |

## 2. Cyber-Physical & Operational Stress Parameters
| Parameter | Bounds | Operational Interpretation | Saturation / Resilience Rationale | Tractability Justification |
| :--- | :--- | :--- | :--- | :--- |
| `telemetryTrust` | `[0,100]` | Trustworthiness of physical sensor readings. | Degrades heavily under stealth/spoofing attacks. | Pomdp-lite scalar abstraction avoiding complex belief spaces. |
| `operationalStress` | `[0,100]` | Cumulative process/hardware fatigue in ICS. | Asymptotic growth representing accelerating systemic wear. | Bypasses floating-point physical ODE integration. |
| `processDeviation` | `[0,100]` | Drift from stable state (e.g. pressure imbalance, abnormal flow). | Rebounds non-linearly under safe mode execution. | Reduced-order alternative to industrial process emulation. |
| `controlLatency` | `[0,100]` | Delayed actuation in PLCs due to cyber lag. | Causes `processDeviation` and `operationalSafetyErosion`. | Preserves finite-time bounds while modeling network delays. |

## 3. Resilience & Recovery Metrics
| Parameter | Bounds | Operational Interpretation | Saturation / Resilience Rationale | Tractability Justification |
| :--- | :--- | :--- | :--- | :--- |
| `resilienceDegradation` | `[0,100]` | Global aggregate measure of system decay. | Evaluated via max bounding logic; never falls below zero. | Central index variable for SMC survivability queries. |
| `restorationConfidence` | `[0,100]` | Certainty of returning to known-good state. | Non-linearly affected by `backupIntegrity` dropping. | Tractable abstraction for stochastic recovery certainty. |

## 4. Sustainability & Cost Tracking
| Parameter | Bounds | Operational Interpretation | Saturation / Resilience Rationale | Tractability Justification |
| :--- | :--- | :--- | :--- | :--- |
| `energyCost` | `[0,MAX]` | KWh approximation during mitigation/recovery. | Non-linear escalation driven by `operationalStress`. | Replaces high-fidelity power-flow models. |
| `carbonCost` | `[0,MAX]` | Carbon equivalent overhead tracking. | Tracks ecological impact of prolonged fail-safe operations. | Enables high-level environmental tradeoff analysis. |

## 5. Distributed Pipeline Topology Variables
| Parameter | Bounds | Operational Interpretation | Saturation / Resilience Rationale | Tractability Justification |
| :--- | :--- | :--- | :--- | :--- |
| segmentStress_A/B | [0,100] | Localized pipeline strain and process risk. | Downstream propagation bounds limit infinite cascade loops. | Enables multi-zone simulation without fluid dynamics solvers. |
| localizedTelemetryTrust_A | [0,100] | Segment-specific monitoring reliability. | Bounded decay isolates uncertainty geographically. | Simplifies massive distributed state spaces into discrete bounds. |
| segmentShutdown_A | [0,1] | Emergency segment isolation state. | Binary bounding restricts operational availability. | Represents topological decoupling tractably. |

## 6. Phase 13: Arithmetic Validation & Decrement Governance
| Rule | Pattern | Structural Purpose | Phase 13 Tractability Guarantee |
| :--- | :--- | :--- | :--- |
| **Strict Guarded Decrements** | `(var >= dec) ? var - dec : 0` | Replaces unsafe `max(0, var - dec)`. | Ensures no intermediate negative assignments occur during stochastic SMC parsing, eliminating parser crashes and underflow exceptions. |
| **Saturating Increments** | `(var + inc <= MAX) ? var + inc : MAX` | Enforces upper bounds without external overflow. | Keeps state space finite and computationally stable. |
