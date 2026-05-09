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
Pr[<=300] (<> (riskScore >= 95))
Pr[<=600] (<> (maintenanceCost >= 500000))

/* 6. Large-Scale Congestion Scenarios */
Pr[<=500] (<> (fwQueueSize > 50 && downtime > 10 && severity > 5))

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
