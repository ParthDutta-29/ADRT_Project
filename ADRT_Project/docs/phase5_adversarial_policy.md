# Phase 5: Adversarial Policy Refinement & Strategic Adaptation

## 1. Adversarial Improvements
- **Elimination of Scripted Progressions:** Attackers no longer blindly execute deterministic state chains. Progression probabilities now actively adapt to real-time defensive posture.
- **Congestion-Aware Exploitation:** Attackers now infer defender exhaustion. If localized queue capacities exceed critical thresholds (e.g., `fwQueueSize >= 80`), the exponential rate governing `OT_Traversal` and `Evasion_Check` transitions dynamically increases from 3 to 5, modeling faster exploitation of delayed mitigations.

## 2. Strategic Adaptation Semantics
- **Bounded Attacker Policy States:** Introduced lightweight bounded variables (`stealthPreference`, `persistenceConfidence`, `exploitAggression`, `attackerPatience`) as an abstraction for adversarial intent.
- **Failure-Aware Adaptation:** Attack progression failures (via `fail?` synchronization loops) dynamically increment `stealthPreference`. When `stealthPreference` reaches high levels (`>70`), the attacker switches to dormant behavior by lowering execution and staging transition rates to 1, effectively trading speed for prolonged persistence.
- **Observability-Aware Persistence:** When attackers trigger detections (`detect!`), they implicitly observe the resulting defender trust decay. By leveraging the updated exponential rates, attackers adaptively prolong their survival windows while the SOC is occupied with lower-confidence anomalies.

## 3. Tractability Impact
- **Maintained UPPAAL SMC Compatibility:** The adversarial policies deliberately avoid exact stochastic game solvers, infinite-horizon Nash equilibrium computations, or deep reinforcement learning matrices.
- **Lightweight Abstraction:** By utilizing ternary operators `(condition) ? rate_A : rate_B` directly inside the location labels, strategic decisions are evaluated instantaneously without triggering combinatorial state explosions.
- **Low-Dimensional Logic:** The policy variables (e.g., `stealthPreference`) are bounded integer spaces (`[0, 100]`), preserving strictly finite-state boundaries.

## 4. Remaining Realism Limitations
- **Partial Context Blindness:** Attackers utilize queue congestion logic as a proxy for "inferred weakness" but still lack a rigorous probabilistic belief structure of the exact SOC analyst state.
- **Absence of Game-Theoretic Optimality:** The adaptation logic is built upon heuristic thresholds (e.g., `stealthPreference > 70`) rather than mathematically proven optimal adversarial policies or formal Stackelberg equilibrium guarantees.
- **Static Graph Topologies:** While transition *timing* adapts, the spatial routing and sequential steps of the kill-chain graph remain structurally static.

## 5. Future-Phase Readiness
- **Phase 6 (Cyber-Physical Coupling):** Introduced foundational variables (`controlSignalTargeting`, `sensorSpoofingIntent`, `plcTraversalConfidence`, `telemetryManipulationIntent`). These abstractions provide the strategic scaffolding necessary to trigger PLC instability and sensor spoofing logic when cyber-physical systems are fully introduced.
- **Phase 7 (Risk Metric Re-Engineering):** The adaptive persistence windows and congestion exploitation success rates establish the necessary emergent outcomes to drive a future dynamic probabilistic risk engine.
