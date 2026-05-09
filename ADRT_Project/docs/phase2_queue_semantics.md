# Phase 2: Queue Semantics Strengthening

## 1. Objective and Scope
The goal of Phase 2 was to advance the queue variables (e.g., `fwQueueSize`) from pure unbounded accumulators (which strictly increase during an attack) into bounded, stochastically draining approximations of congestion. This must be accomplished without implementing computationally expensive continuous queueing models (PDEs) or breaking finite-state SMC tractability.

## 2. Modifications Executed
The `defense_layer.xml` was refactored across all 5 mitigation templates (`Firewall_Defense`, `IDS_Defense`, `WAF_Defense`, `EDR_Defense`, `DLP_Defense`).

### A. Bounded Service Semantics (Queue Draining)
* **Idle Draining**: A self-loop transition was injected into the `Idle` locations (e.g., `FWD_Idle`). When the defense is not actively parsing an attack but the queue is populated (`fwQueueSize > 0`), it stochastically drains the queue by `-5`. 
* **Active Draining**: A self-loop transition was added to the `Analyse` locations. While the defense evaluates a rule, it actively processes backlogs, draining the queue by `-10`.
* **Mechanism**: Because UPPAAL evaluates these internal self-loops against the location's stochastic exponential rate, this perfectly approximates an M/M/1 continuous service process without explicitly requiring continuous clock PDEs.

### B. Congestion-Induced Observability Degradation (Missed Detections)
* The transition processing incoming detections (`detect?`) was split dynamically.
* If `QueueSize < 80`, the defense successfully enters the `Monitor` phase.
* If `QueueSize >= 80`, the defense is *saturated*. It ignores the transition, remaining in `Idle`, and sets the global flag `falseNegative = true`. This establishes a probabilistic link between congestion and blindness.

### C. Congestion-Induced Mitigation Failure
* The transition resolving mitigation rules (`success!` vs `fail!`) was similarly constrained.
* When executing a rule under extreme backlog (`QueueSize >= 80`), the defense is mathematically forced to route to the `Failed` location, guaranteeing mitigation collapse during extreme saturation.

## 3. Heuristics & Abstractions Retained
* **Approximate Queue Sizes**: Granularity remains coarse (increments/decrements of 5 or 10) to limit state space growth. 
* **Symbolic Service Rates**: The draining rate inherits the template's location exponential rate, approximating service delay without requiring complex secondary timer processes.

## 4. Expected Tractability & Scalability Impact
* **State-Space Impact**: Bounded queue values are strictly capped at `100`, preserving finite-state boundaries. Because variables now decrease as well as increase, the model reaches steady-state equilibrium distributions, heavily mitigating infinite "stray" paths.
* **SMC Tractability**: Bounded loops marginally increase localized transitions evaluated per step. However, reducing queue buildup prevents the system from permanently locking into saturated corner cases, vastly improving the realism of simulated bounds without degrading SMC computation limits.

## 5. Behavioral Improvements
The model no longer suffers from monotonically increasing queues. Congestion now genuinely causes defensive blindness, delays mitigations, and naturally dissipates during quiet periods. This significantly raises the cyber-physical realism above a simple counter.
