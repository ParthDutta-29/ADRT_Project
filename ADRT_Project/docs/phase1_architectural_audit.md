# Phase 1: Architectural Audit & Semantic Mapping

## 1. Architectural Dependency Map
The current modularized architecture integrates 28 templates across 8 distinct layers. The system is structurally coupled through global variables and broadcast synchronization.
* **Control / Game Layer:** `Attack_Coordinator` -> Orchestrates stochastic attack starts (`start_net!`, `start_malware!`).
* **Adversarial Layer:** `Network_Attack`, `Malware_Attack`, etc. -> Receives triggers, increments cost metrics (`NET_MC`), increments queue load on defense gates (`fwQueueSize = min(100, fwQueueSize+5)`), and broadcasts `detect!`.
* **Network Gateway Layer:** `OR_L12`, `NOT_FW2`, `Voting_Gate` -> Acts as routing and filtering bottlenecks. Interacts with boolean flags (`firewall==true`) and evaluates aggregated queues.
* **Defensive Layer:** `Firewall_Defense`, `IDS_Defense`, etc. -> Listens for detection channels (`detect?`), manages isolated defense states (`FWD_Block`, `FWD_Contain`), and interacts with the SOC.
* **SOC / Human Layer:** `Defender_Response` -> Aggregates risk scores and triggers mitigation or hardening strategies.
* **Process / Physical Layer:** `Environment` -> Uses stochastic delays (exponential rates) mapped to `Env_Valve_Control`, `Env_PID_Control`. Currently loosely coupled to cyber state via global boolean metrics (`downtime`).

## 2. Semantic Weakness Inventory
* **Cyber-Physical Coupling is Heuristic:** The `Environment` template translates cyber breaches into generic `downtime` variables. It does not actively simulate physical flow, pressure (e.g., using Continuous-Time/Hybrid Automata variables like `clock pressure; pressure' == rate`), making the CPS aspect symbolic rather than mechanistic.
* **Adversary Policy is Static:** The `Attack_Coordinator` and attack templates rely heavily on fixed exponential rates and probabilistic branching (`probability 7 vs 3`) rather than adaptive game-theoretic decision making based on perceived defense strength.

## 3. Stochastic Consistency Analysis
* **Consistent:** The Markovian structure is preserved. Exponential transition delays correctly define the continuous-time Markov execution.
* **Inconsistent:** The integration of "Queue Size" limits (e.g., `fwQueueSize`) operates via deterministic assignment (`+5`, `+10`) inside stochastic transitions. Because queues do not "drain" via continuous service rates, they act as accumulators (integrators) rather than true stochastic queueing networks.

## 4. Parser-Risk Analysis
* **Low Risk:** The architecture strictly utilizes flat integer arrays, bounded integers (`[0,100]`), and UPPAAL standard logical operators (`&&`, `||`). By avoiding complex C-struct arrays or dynamically typed variables, the AST remains inherently parser-safe.

## 5. Synchronization-Risk Analysis
* **Medium Risk:** Broadcast channels are used heavily (e.g., `detect!`). UPPAAL's broadcast semantics are non-blocking—if a receiver is not in a state waiting for `detect?`, the message is silently dropped. While this avoids deadlocks, it risks *silent synchronization failures* where an attack triggers detection but the firewall is transitioning and misses the signal.

## 6. State-Space Explosion Risk Analysis
* **High Risk in Standard Reachability:** By introducing 5 queue variables bounded to `100` (`fwQueueSize`, `idsQueueSize`, etc.), the concurrent state space multiplies by $100^5$ ($10^{10}$) theoretical states simply from queue configurations. This renders exhaustive checks (`A[]`, `E<>`) highly computationally expensive, mandating Statistical Model Checking (SMC) for deep verification.

## 7. Queue Abstraction Limitations
* **Naive Accumulation:** Currently, `fwQueueSize` behaves like a damage counter rather than a queue. It increments during attacks but lacks an explicit, mathematically sound `service_rate` process that continuously dequeues packets. 
* **Missing Little's Law Mechanics:** There is no distinct relationship between queue length and stochastic processing delay.

## 8. Remaining Naive Symbolic Constructs
* **Boolean Compromise Flags:** Using `breach = true` or `plcCompromised = true` represents boolean certainty. Real-world CPS security operates under partial observability (POMDP), where defenders only perceive *alerts* or *sensor deviations*, not absolute system truth.
* **Gate Logic:** `OR_L12` and `AND_L2` templates use integer counters (`or_hits`) to represent converged conditions. This is functionally an IT logic gate, not a hybrid physical constraint.

## 9. Behavioral Inconsistency Risks
* **Cost Accumulation:** Templates increment global multi-objective metrics (`maintenanceCost := min(MAX_COST, maintenanceCost + NET_MC)`). Because these are triggered by asynchronous stochastic events across 28 templates, highly concurrent interleavings could saturate the `MAX_COST` prematurely, masking deeper execution branches if cost triggers fail states.

## 10. UPPAAL Tractability Constraints
* UPPAAL SMC is highly optimized for stochastic tracking but struggles with highly dense, globally coupled variables because every transition invalidates cached states. Heavy reliance on global variables (`riskScore`, `severity`, 5 separate queue variables) over local template state variables significantly reduces simulation throughput.

---

## PHASED REFINEMENT ROADMAP

* **Phase 1 [COMPLETE]:** Architectural Audit & Semantic Mapping
* **Phase 2:** Queue Semantics Strengthening (Implement explicit stochastic drain/service rates to validate bounded queues).
* **Phase 3:** Congestion & Timing Dynamics (Couple transition rates dynamically to queue sizes).
* **Phase 4:** Partial Observability (Shift from boolean `breach` flags to Bayesian-style localized belief variables).
* **Phase 5:** Adversarial Policy Refinement.
* **Phase 6:** Cyber-Physical Coupling Strengthening (Introduce ODE/Hybrid clock dynamics for OT processes).
* **Phase 7:** Risk Metric Re-Engineering.
* **Phase 8:** Recovery Semantics Refinement.
* **Phase 9:** Behavioral Validation Framework.
* **Phase 10:** Scalability & Tractability Optimization.
