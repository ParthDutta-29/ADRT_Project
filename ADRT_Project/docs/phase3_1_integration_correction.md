# Phase 3.1: Timing Dynamics Integration & Architectural Consistency Correction

## 1. Architectural Corrections
- **Removed Disconnected Constructs:** Standalone toy automata such as `Defense_Node` and `Attack_Vector` were removed to ensure they do not bypass the core architectural design. 
- **Preserved Existing Templates:** All updates were performed entirely within the existing defense (`Firewall_Defense`, `IDS_Defense`, `WAF_Defense`, `EDR_Defense`, `DLP_Defense`) and attack (`Network_Attack`, `Malware_Attack`, `API_Attack`, etc.) templates. 
- **Unified Framework:** The timing refinements now natively extend the existing finite-state architecture, ensuring the model functions as one unified UPPAAL SMC application instead of several loosely connected demonstrations.

## 2. Parser and Syntax Corrections
- **Undefined Identifiers:** Replaced legacy and undefined variables (e.g., `defense_load`) with explicit, queue-specific definitions (`fwQueueSize`, `idsQueueSize`, etc.) integrated natively in `global_defs.xml`.
- **Logical Operators:** Validated that all logical operators use parser-safe C-style syntax (`&&` and `||`) instead of unsupported text variants (`and`, `or`).
- **SMC Syntax:** Removed experimental and potentially invalid query syntax (such as `E[max: ...]`). All queries strictly use the supported `Pr[<=limit] (<> ...)` form for SMC verification and `E<>` for reachability.
- **Removed Disconnected Mitigations:** Ensured mitigation delay paths are directly coupled to the actual state transitions (e.g., `FWD_Rule`, `FWD_Analyse`) rather than using disconnected probability functions.

## 3. Timing Semantic Reintegration
- **Congestion-Dependent Latency:** In defense templates, states such as `FWD_Alert`, `FWD_Analyse`, and `FWD_Rule` use bounded congestion conditions (e.g., `(fwQueueSize>50) ? 1 : 4`) to stochastically increase the time spent in these locations. High congestion leads to slower processing rates.
- **Stale Observability:** Implemented logic where excessive queue thresholds (e.g., `fwQueueSize >= 80`) trigger a transition back to the `Idle` state with `falseNegative=true`, representing dropped telemetry.
- **Attack Progression Advantage:** Attack templates now naturally gain probabilistic timing advantages without arbitrary attacker speed boosts. As the defense rates decrease due to load, the unhindered static attacker rates naturally yield a higher probability of advancing to the next attack phase before defensive mitigation can complete.
- **Delayed Defender Response:** Modified the `Defender_Response` template (in `human_layer.xml`) so that stages such as `DR_Intake` and `DR_Classify` experience congestion-induced latency via dynamic exponential rates dependent on queue sizes.

## 4. Tractability Impact
- **Finite-State Safety:** Re-integrating timing directly via dynamic exponential rates allows the model to remain tractable for Statistical Model Checking (SMC).
- **Bounded Constraints:** Queue sizes are strictly bounded (e.g., `[0, 100]`), and the timing degradation occurs over coarse discrete tiers, preventing dense clock product explosions.
- **Reduced-Order Abstraction:** The integration avoids micro-level continuous latency modeling, utilizing bounded stochastic latency approximation to maintain SMC tractability.

## 5. Remaining Limitations
- **Latency Discretization:** The congestion timing is modelled stochastically via discrete exponential rate changes rather than continuous real-time queuing dynamics.
- **Non-Protocol Specificity:** This abstraction provides bounded latency approximation but does not guarantee exact, protocol-level network queueing correctness.
- **State-Space Growth:** While the architecture is finite-state, severe concurrent combinations of large queues and parallel attack vectors may still strain traditional symbolic verification, hence the primary reliance on SMC simulation limits.
