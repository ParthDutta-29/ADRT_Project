/* 
 * SCALABILITY TESTS for Modular Architecture
 * These queries evaluate state-space explosion risk, queue congestion limits, and topology scaling.
 */

/* 1. Deep Reachability Queries (Testing for state space explosions) */
E<> (Firewall_Defense.FWD_Block && IDS_Defense.IDSD_Block && Defender_Response.DR_Recover)
E<> (scadaCompromised == true && plcCompromised == true && breach == true)

/* 2. Bounded-Time Probability Queries (SMC Tractability evaluation) */
Pr[<=500] (<> (fwQueueSize > 90))
Pr[<=500] (<> (idsQueueSize > 90))

/* 3. Queue Saturation Checks (Testing congestion capacity logic) */
Pr[<=300] (<> (fwQueueSize > 80 && wafQueueSize > 80 && edrQueueSize > 80))
E<> fwQueueSize == 100

/* 4. Concurrent Attack Propagation Checks */
Pr[<=400] (<> (Network_Attack.NA_Payload_Staging && Malware_Attack.MAL_Command_And_Control))
Pr[<=400] (<> (lateral == true && persistence == true && breach == true))

/* 5. Topology Stress Tests */
Pr[<=300] (<> (resilienceDegradation >= 95))
Pr[<=600] (<> (maintenanceCost >= 500000))

/* 6. Large-Scale Congestion Scenarios */
Pr[<=500] (<> (fwQueueSize > 50 && downtime > 10 && operationalSafetyErosion > 5))

/* 7. Congestion Persistence & Recovery Tests (Phase 2 Additions) */
E<> (fwQueueSize > 80 && falseNegative == true)
Pr[<=500] (<> (fwQueueSize > 0 && Firewall_Defense.FWD_Analyse))
Pr[<=600] (<> (fwQueueSize == 0 && idsQueueSize == 0 && wafQueueSize == 0))
E<> (Firewall_Defense.FWD_Failed && fwQueueSize >= 80)

/* 8. Timing Dynamics & Latency Tests (Phase 3 Additions) */
Pr[<=500] (<> (Defender_Response.DR_Intake && fwQueueSize > 50))
Pr[<=500] (<> (Firewall_Defense.FWD_Rule && fwQueueSize > 50))
Pr[<=400] (<> (falseNegative == true && Network_Attack.NA_Execution))
E<> (fwQueueSize > 50 && downtime > 5)

/* 9. POMDP-Lite Observability & Belief-State Tests (Phase 4 Additions) */
Pr[<=500] (<> (alertConfidence > 80))
Pr[<=500] (<> (telemetryTrust < 50))
E<> (telemetryTrust < 20 && breach == true)
E<> (alertConfidence < 40 && scadaCompromised == true)
Pr[<=600] (<> (plcSuspicion > 50))
E<> (telemetryTrust < 50 && Defender_Response.DR_Sev_Low)

/* 10. Adversarial Policy & Strategic Adaptation Tests (Phase 5 Additions) */
Pr[<=500] (<> (stealthPreference > 70 && Network_Attack.NA_Execution))
E<> (stealthPreference >= 80 && Defender_Response.DR_Sev_Low)
Pr[<=400] (<> (fwQueueSize >= 80 && Network_Attack.NA_OT_Traversal))
E<> (telemetryTrust < 40 && scadaCompromised == true && stealthPreference > 60)
Pr[<=600] (<> (stealthPreference > 50 && downtime < 5))

/* 11. Cyber-Physical Coupling & Operational Degradation Tests (Phase 6 Additions) */
Pr[<=500] (<> (telemetryIntegrity < 50 && sensorSpoofingIntent > 40))
Pr[<=600] (<> (processDeviation > 50 && telemetryTrust < 50))
E<> (controlLoopStability < 50 && operationalStress > 30)
Pr[<=500] (<> (actuatorTrust < 50 && fwQueueSize >= 80))
E<> (safetyMargin < 50 && downtime > 5)
Pr[<=600] (<> (processDeviation > 50 && alertConfidence > 50))

/* 12. Risk Metric Re-Engineering & Resilience Semantics (Phase 7 Additions) */
Pr[<=500] (<> (resilienceDegradation > 50))
Pr[<=500] (<> (cpsInstabilityProbability > 50))
Pr[<=400] (<> (mitigationConfidence < 40))
E<> (mitigationConfidence < 50 && stealthPreference > 50)
Pr[<=600] (<> (telemetryTrust < 50 && alertConfidence < 30))
E<> (operationalSafetyErosion > 50 && downtime > 5)
