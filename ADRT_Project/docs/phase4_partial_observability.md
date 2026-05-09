# Phase 4: Partial Observability & Belief-State Semantics (POMDP-lite)

## 1. Observability Improvements
- **Eliminated Omniscient Decision-Making:** The framework has been successfully transitioned from relying on Boolean ground truths (e.g., `riskScore`, `breach == true`) to using bounded probabilistic observability. Defenders no longer possess direct insight into system compromise.
- **Evidence Accumulation via SOC Intake:** The `Defender_Response` template no longer reacts deterministically to global variables. Instead, it accumulates `alertConfidence` dynamically based on the frequency of incoming alerts (the `detect?` synchronization) and the real-time reliability of the sensors (`telemetryTrust`).

## 2. Uncertainty Semantics
- **Bounded Belief States:** Introduced parser-safe integer belief approximations in `global_defs.xml`, including `alertConfidence`, `plcSuspicion`, `scadaSuspicion`, `networkThreatConfidence`, and `telemetryTrust`.
- **Stale Telemetry and Trust Degradation:** The defense layer (Firewall, IDS, WAF, EDR, DLP) was upgraded to capture network congestion instability. When localized queue sizes exceed processing capacity (e.g., `fwQueueSize >= 80`), the system models sensor exhaustion by actively degrading `telemetryTrust` by 10 points per missed packet alongside setting `falseNegative=true`.
- **Confidence-Sensitive Behaviors:** Defender behavior now strictly correlates with `alertConfidence`. Low-confidence evidence (`alertConfidence < 40`) slows escalation, pushing the SOC down cheaper, less aggressive strategic paths (`DR_Strat_Cheap`). High confidence forces aggressive mitigation and full system lockdowns (`DR_Strat_Aggr`).
- **Probabilistic Attack Persistence:** Because defenders now struggle under congestion (lowered trust yielding slower confidence growth), stealthy or heavy attacks organically survive longer without requiring arbitrary changes to attack graph transitions. 

## 3. Tractability Impact
- **Finite-State Adherence:** The implementation adheres to UPPAAL SMC scalability constraints by modeling belief states as discrete `int[0,100]` variables rather than mathematically dense continuous POMDP probability distributions. 
- **Lightweight Inference:** Evidence accumulation (`alertConfidence + (telemetryTrust/10)`) relies strictly on inexpensive integer arithmetic, keeping internal state explosions tightly bounded while offering POMDP-inspired abstractions.
- **Tractable Verification:** All logical updates guarantee synchronization safety and remain completely supported by SMC `Pr[<=bound]` reachability bounds without running into infinite dimensionality issues common with recursive Bayesian solvers.

## 4. Remaining Realism Limitations
- **Coarse Abstraction:** The belief-state variables represent aggregated "buckets" of confidence rather than rigorous, mathematically exact Bayesian inference graphs.
- **Absence of Correlated Hidden State Estimation:** Probabilities of false positives and true positives are simulated stochastically via confidence thresholding, but lack deep hidden Markov model filtering (like Kalman filters).
- **Synchronized Delays:** Communication of confidence and suspicion currently relies on instantaneous global variables instead of modeled discrete-time data packets traversing physical networks.

## 5. Future-Phase Readiness
- **Phase 5 (Adversarial Policy Refinement):** Attackers can now exploit observability gaps. Stealthy attacks that don't trigger large alerts will face delayed defender escalation, creating clear strategic opportunity windows.
- **Phase 6 (Cyber-Physical Coupling):** Bounded indicators like `telemetryTrust` and `plcSuspicion` provide an immediate integration point for simulating pressure instability and physical sensor spoofing without jumping straight to complex ODE definitions.
