# Phase 6: Cyber-Physical Coupling Strengthening

## 1. Cyber-Physical Improvements
- **Reduced Symbolic Abstractions:** Shifted the framework away from arbitrary Boolean flags (e.g., `scadaCompromised == true`) toward bounded operational variables (e.g., `pipelinePressure`, `telemetryIntegrity`, `controlLoopStability`, `actuatorTrust`).
- **Cyber-to-Physical Influence:** Cyber attacks now actively decay physical stability. For example, during payload staging and command-and-control transitions, attackers with high stealth preferences increment `sensorSpoofingIntent`, which directly degrades `telemetryIntegrity`. Similarly, persistent stale telemetry forces `processDeviation` to rise gradually.
- **Physical-to-Cyber Feedback:** Implemented a full bidirectional feedback loop. Physical deviations now alert the SOC without needing direct cyber intrusion flags. High `processDeviation` organically increases `alertConfidence`. Furthermore, physically degraded `controlLoopStability` inherently erodes the SOC's `telemetryTrust`, altering defensive escalation behaviors.

## 2. Operational Degradation Semantics
- **Finite-State Operational Decay:** Replaced sudden catastrophic failures with gradual operational degradation.
- **Process Instability & Safety:** Prolonged cyber attacks systematically lower `controlLoopStability`, which in turn increases `operationalStress`. As `processDeviation` breaches safe limits (e.g., `> 50`), the physical `safetyMargin` actively degrades.
- **Consequential Downtime:** When operational stress reaches critical thresholds (`> 50`), the recovery phases of the SOC inherently suffer longer downtimes, successfully bridging cyber delays into real-world availability costs.
- **Actuator Deception:** As network congestion creates stale telemetry, `actuatorTrust` inherently decays, prompting defenders to evaluate risks differently before committing to physical mitigation responses.

## 3. Tractability Impact
- **SMC Scalability Preserved:** Replaced the necessity for deep continuous-time ODE systems with `int[0,100]` bounded operational tiers.
- **Parser-Safe Coupling:** All physical influences execute via finite-state threshold logic (e.g., `processDeviation=(telemetryTrust<50)?min(100,processDeviation+5):processDeviation`). 
- **Absence of SHS Explosion:** By keeping physical metrics discrete and bounded, the framework entirely avoids the infinite dimensionality common in Stochastic Hybrid Systems (SHS), preserving UPPAAL SMC's capability to bound-check probability limits effectively.

## 4. Remaining CPS Realism Limitations
- **Reduced-Order Mathematics:** The physics engine is purely semantic. Fluid dynamics, thermodynamics, and precise PID algorithms are abstracted away into linear bounded counters.
- **No Temporal Physical Lags:** While cyber timing is stochastic, the physical propagation of instability (e.g., pressure loss taking 10 minutes to reach a valve) occurs instantaneously in the model's global variables once a transition executes.
- **Lack of Protocol Fidelity:** Sensor spoofing degrades integer confidence buckets but does not emulate the actual payload manipulation of Modbus/DNP3 network packets.

## 5. Future-Phase Readiness
- **Phase 7 (Risk Metric Re-Engineering):** The detailed physical degradation metrics (`safetyMargin`, `operationalStress`, `processDeviation`) now serve as the perfect empirical foundation to construct a probabilistic cyber-physical risk equation.
- **Phase 8 (Recovery Semantics Refinement):** Since high operational stress now dynamically prolongs downtime, future recovery phases can explore stochastic fail-safe procedures, redundant loops, and staggered operational recovery mechanisms without inventing new state variables.
