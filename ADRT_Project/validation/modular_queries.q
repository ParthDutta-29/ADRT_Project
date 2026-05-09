/* 
 * MODULAR QUERIES for Refactored Modular Architecture
 * These queries test the modular framework to ensure stochastic consistency.
 */

/* 1. Deadlock Checks */
A[] not deadlock

/* 2. Reachability Checks */
E<> Network_Attack.NA_Payload_Staging
E<> Malware_Attack.MAL_PLC_Manipulation
E<> Firewall_Defense.FWD_Block
E<> Defender_Response.DR_Recover

/* 3. Breach Probability Queries */
Pr[<=100] (<> breach == true)
Pr[<=150] (<> scadaCompromised == true)
Pr[<=150] (<> plcCompromised == true)

/* 4. Recovery Probability Queries */
Pr[<=300] (<> (downtime == 0 && breach == true))
Pr[<=200] (<> (riskScore < 20))

/* 5. Attack Progression Queries */
Pr[<=100] (<> Network_Attack.NA_Execution)
Pr[<=100] (<> API_Attack.AA_OT_Traversal)

/* 6. Congestion Queries */
E<> fwQueueSize > 50
E<> idsQueueSize > 50
Pr[<=200] (<> (wafQueueSize > 80))

/* 7. Topology Propagation Queries */
Pr[<=150] (<> lateral == true)
Pr[<=150] (<> persistence == true)

/* 8. Observability Queries */
Pr[<=100] (<> truePositive == true)
Pr[<=100] (<> falseNegative == true)
