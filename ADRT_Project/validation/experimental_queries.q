/*
 * FORMAL QUERY TAXONOMY & EXPERIMENTAL EVALUATION
 * This suite maps directly to the publication-grade experimental categories for the ADRT framework.
 * Framework Position: A bounded stochastic cyber-physical resilience abstraction framework for tractable SMC experimentation.
 */

/* ====================================================
 * A. RESILIENCE QUERIES
 * Operational Interpretation: Measures ability to withstand and recover from attacks.
 * Research Purpose: Assess survivability probabilities and graceful degradation dynamics.
 * ==================================================== */

/* Probability of critical degradation (survivability failure) */
Pr[<=500] (<> (resilienceDegradation > 80))

/* Repeated stochastic run: Mean confidence of restoration under operational uncertainty */
simulate 100 [<=500] { restorationConfidence }

/* Graceful degradation: probability that safety margin drops but fail-safe saves the system */
Pr[<=600] (<> (safetyMargin < 30 && failSafeEngaged == true))


/* ====================================================
 * B. CONGESTION QUERIES
 * Operational Interpretation: Measures the systemic stress on the mitigation queues.
 * Research Purpose: Analyze mitigation latency escalation and overload-induced instability.
 * ==================================================== */

/* Probability of mitigation saturation (congestion collapse) */
Pr[<=500] (<> (fwQueueSize > 80 && idsQueueSize > 80))

/* Expected mitigation backlog over time */
simulate 100 [<=500] { congestionPressure }

/* Probability that congestion directly causes operational safety erosion */
Pr[<=400] (<> (congestionPressure > 80 && operationalSafetyErosion > 50))


/* ====================================================
 * C. CPS INSTABILITY QUERIES
 * Operational Interpretation: Measures translation of cyber delay into physical process failure.
 * Research Purpose: Analyze control latency escalation and delayed stabilization.
 * ==================================================== */

/* Process deviation trajectory due to control latency */
simulate 100 [<=500] { processDeviation }

/* Probability of entering manual supervisory fallback (safe mode) due to CPS instability */
Pr[<=500] (<> (safeModeOperation > 0 && processDeviation > 50))

/* Expected physical latency resulting from cyber lag */
simulate 100 [<=400] { controlLatency }


/* ====================================================
 * D. STEALTH PERSISTENCE QUERIES
 * Operational Interpretation: Measures adversary's ability to remain undetected while causing harm.
 * Research Purpose: Analyze delayed detection impact and stealth-induced degradation.
 * ==================================================== */

/* Probability of an adversary achieving deep persistence despite defenses */
Pr[<=500] (<> (stealthPreference > 80 && breach == true))

/* Impact of degraded telemetry on stealth persistence */
Pr[<=600] (<> (telemetryTrust < 40 && stealthPreference > 60))


/* ====================================================
 * E. RECOVERY QUERIES
 * Operational Interpretation: Measures systemic return to normal operations.
 * Research Purpose: Analyze delayed recovery probabilities and bounded recovery realism.
 * ==================================================== */

/* Expected recovery capacity over time */
simulate 100 [<=500] { recoveryCapacity }

/* Probability of recovery failure due to prolonged operational stress */
Pr[<=600] (<> (DR.PIR_Failed && operationalStress > 70))


/* ====================================================
 * F. SUSTAINABILITY QUERIES
 * Operational Interpretation: Measures energy, carbon, and financial overhead of resilience.
 * Research Purpose: Analyze tradeoff between prolonged defense and sustainability exhaustion.
 * ==================================================== */

/* Expected energy escalation during congestion scenarios */
simulate 100 [<=500] { energyCost }

/* Carbon cost trajectory during persistent safe-mode operations */
simulate 100 [<=600] { carbonCost }

/* Maintenance cost explosion probability under severe attack stress */
Pr[<=500] (<> (maintenanceCost > 50000 && congestionPressure > 80))


/* ====================================================
 * G. BOUNDED-STATE SAFETY QUERIES
 * Operational Interpretation: Verification of integer boundaries and safety guards.
 * Research Purpose: Guarantee tractability, parser-safety, and SMC validity.
 * ==================================================== */

A[] (telemetryTrust >= 0 && telemetryTrust <= 100)
A[] (resilienceDegradation >= 0 && resilienceDegradation <= 100)
A[] (safetyMargin >= 0 && safetyMargin <= 100)
A[] (recoveryCapacity >= 0 && recoveryCapacity <= 100)
A[] (congestionPressure >= 0 && congestionPressure <= 100)
A[] (operationalStress >= 0 && operationalStress <= 100)


/* ====================================================
 * H. COMPUTATIONAL VALIDITY QUERIES
 * Operational Interpretation: Ensures no state-space explosion or infinite loops occur.
 * Research Purpose: Validate bounded execution times and modular scalability.
 * ==================================================== */

/* Deadlock freedom across modular bounded logic */
A[] not deadlock

/* Assure system eventually can attempt recovery */
E<> DR.PIR_Intake

/* ====================================================
 * PHASE 11: OIL PIPELINE ICS EXPERIMENTATION
 * ==================================================== */

/* Probability of unsafe pipeline pressure escalation due to valve lag */
Pr[<=500] (<> (processDeviation > 80 && safeModeOperation == 0))

/* Stealth persistence survival under degraded flow telemetry */
Pr[<=600] (<> (stealthPreference > 70 && telemetryTrust < 40))

/* Congestion-induced operational degradation mapping */
simulate 100 [<=500] { congestionPressure, operationalStress }

/* Environmental risk escalation (carbon emissions due to degraded pump efficiency) */
simulate 100 [<=600] { carbonCost }


/* ====================================================
 * PHASE 12: DISTRIBUTED TOPOLOGY & COMPARATIVE EVALUATION
 * ==================================================== */

/* Distributed Pipeline Resilience: Downstream Instability Propagation */
Pr[<=500] (<> (segmentStress_B > 50 && segmentStress_A > 70))

/* Localized Recovery: Probability of isolating Segment A successfully */
Pr[<=400] (<> (segmentShutdown_A == 1 && compressorHealth_A < 50))

/* Comparative Baseline: Congestion-Aware vs Non-Aware (Simulate expected impact) */
simulate 100 [<=500] { resilienceDegradation } : 1 : (congestionAwareDefense == 1)
simulate 100 [<=500] { resilienceDegradation } : 1 : (congestionAwareDefense == 0)

/* Distributed Telemetry Trust Evaluation */
simulate 100 [<=600] { localizedTelemetryTrust_A, localizedTelemetryTrust_B }


/* ====================================================
 * PHASE 13: PUBLICATION-GRADE DISTRIBUTED RESILIENCE & COMPARATIVE EVALUATION
 * ==================================================== */

/* Segment Isolation Survivability Analysis */
Pr[<=500] (<> (segmentShutdown_A == 1 && segmentStress_B < 50))
simulate 100 [<=600] { segmentStress_A, segmentStress_B }

/* Distributed Degradation Propagation */
Pr[<=500] (<> (resilienceDegradation > 80 && telemetryTrust < 40))

/* Localized Telemetry Collapse and Cascade */
Pr[<=600] (<> (localizedTelemetryTrust_A < 20 && compressorHealth_A < 40))

/* Compressor Dependency Stress and Downstream Instability */
simulate 100 [<=500] { compressorHealth_A, segmentStress_A }

/* Comparative Evaluation: Telemetry-Aware Defense vs Baseline */
simulate 100 [<=500] { resilienceDegradation } : 1 : (telemetryAwareDefense == 1)
simulate 100 [<=500] { resilienceDegradation } : 1 : (telemetryAwareDefense == 0)

/* Resilience Envelope Evaluations */
simulate 100 [<=500] { safetyMargin, resilienceDegradation }
