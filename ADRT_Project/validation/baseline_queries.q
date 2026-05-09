/* 
 * BASELINE QUERIES for Original Monolithic ADRT.xml
 * These queries test the original framework before semantic renaming.
 */

/* 1. Deadlock Checks */
A[] not deadlock

/* 2. Reachability Checks */
E<> Network_Attack.NA_Post1
E<> Malware_Attack.MAL_Impact
E<> Firewall_Defense.FD_Blocked
E<> Defender_Response.DR_Restored

/* 3. Breach Probability Queries */
Pr[<=100] (<> breach == true)
Pr[<=150] (<> scadaCompromised == true)
Pr[<=150] (<> plcCompromised == true)

/* 4. Recovery Probability Queries */
Pr[<=300] (<> (downtime == 0 && breach == true))
Pr[<=200] (<> (resilienceDegradation < 20))

/* 5. Attack Progression Queries */
Pr[<=100] (<> Network_Attack.NA_Exec)
Pr[<=100] (<> API_Attack.AA_Bypass)

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
