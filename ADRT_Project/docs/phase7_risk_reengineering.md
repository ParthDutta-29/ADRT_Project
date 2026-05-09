# Phase 7: Risk Metric Re-Engineering & Probabilistic Resilience Semantics

## 1. Metric-Semantic Improvements
- **Removal of Heuristic Scoring:** All manually incremented heuristic variables (e.g., `riskScore`, `severity`, `threat_score`, `defense_score`) and their respective additive (`+=`) bookkeeping rules were completely stripped from the attack, defense, and human layers.
- **Probabilistic Interpretability:** Replaced arbitrary counters with operationally interpretable, bounded stochastic approximations representing actual resilience mechanics (`resilienceDegradation`, `mitigationConfidence`, `cpsInstabilityProbability`, `breachLikelihood`, `operationalSafetyErosion`).
- **Journal-Grade Causal Propagation:** Metrics no longer increment unconditionally because a transition fired. Instead, they dynamically scale based on real-time operational limits. For example, `mitigationConfidence` now calculates dynamically as a function of `telemetryTrust` and `actuatorTrust`, meaning compromised observability explicitly degrades confidence. 

## 2. Uncertainty-Propagation Improvements
- **Confidence Tiers:** The model evaluates uncertainty propagation implicitly. When attackers bypass observability layers (stale telemetry), the degraded `telemetryTrust` lowers the `mitigationConfidence` of the SOC, causing a cascaded mathematical rise in `resilienceDegradation`.
- **Bounded Evidence Accumulation:** Metrics update probabilistically. Instead of static additions, the system bounds probability states dynamically, allowing SMC limits to evaluate edge-case uncertainty (e.g., evaluating cases where `mitigationConfidence < 50` while `stealthPreference > 50`).

## 3. Resilience-Modeling Improvements
- **Operational Continuity Focus:** The objective function shifted from quantifying "attack success" to measuring "resilience failure". `operationalSafetyErosion` inherently responds to drops in `safetyMargin`, binding physical CPS degradation to formal risk metrics.
- **Tractable Impact Chains:** Delayed SOC response (caused by `fwQueueSize` overflow) now translates functionally into `resilienceDegradation` and `cpsInstabilityProbability`, bridging cyber delays to physical resilience decay.

## 4. Tractability Impact
- **Maintained UPPAAL SMC Computability:** Replaced mathematically unscalable recursive continuous probability distributions with bounded integer semantics (`int[0,100]`) and lightweight discrete assignments.
- **No Continuous Bayesian Explosion:** All uncertainty propagation relies strictly on finite-state bounds, bypassing the infinite-state dimensionality risks of formal probabilistic graphical inference matrices.
- **SMC Scalability Testing:** Scalability checks evaluate `Pr[<=limit]` bounding accurately over the new resilience parameters without producing dense clock or floating-point memory explosions.

## 5. Remaining Realism Limitations
- **Lack of True Bayesian Filtering:** The bounded integer thresholds simulate confidence aggregation but do not execute exact quantitative Bayesian theorem updates or online probabilistic graph resolution.
- **Reduced-Order Risk Quantification:** The framework emulates emergent severity rather than calibrating exactly against formal actuarial CVSS risk matrices or dense industrial control reliability scores.

## 6. Future-Phase Readiness
- **Phase 8 (Recovery Semantics Refinement):** Now that metrics measure resilience degradation dynamically, recovery strategies can be modeled not just to "reset" the system, but to stochastically decrease `resilienceDegradation` over variable, uncertainty-driven time horizons.
- **Phase 9 (Behavioral Validation):** The framework is now robustly metricized for formal experimental validation. Monte Carlo distributions via SMC can output genuine probabilistic resilience scores suitable for journal evaluation.
