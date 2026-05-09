# Validation Methodology and Verification Report

This document formally records the validation and verification of the modularized UPPAAL SMC architecture. The methodology strictly distinguishes between structural preservation (code artifacts) and behavioral consistency (stochastic execution semantics).

## 1. Structural Preservation Analysis (PART 2)
To ensure the modular decomposition did not inadvertently drop or duplicate templates, locations, or transitions, a cardinality-preserving decomposition check was executed.
The validation script `compare_semantics.py` aggregated the merged AST of `main_system.xml` and compared it against the original `ADRT.xml`:
* **Templates Preserved:** 28 / 28
* **Locations Preserved:** 289 / 289
* **Transitions Preserved:** 334 / 334
* **Clocks Preserved:** 2 / 2

**Conclusion:** Cardinality-preserving decomposition was verified. The counts of templates, locations, transitions, and clocks match exactly. This structural consistency validation ensures the static framework remains intact, but it does *not* automatically guarantee behavioral equivalence.

## 2. Synchronization Parity Validation (PART 4)
The script `check_channels.py` evaluated the compiled AST for synchronization pairs (`chan!` and `chan?`).
* **Declared channels:** 28
* **Channels with broadcast (Sends):** 15
* **Channels with receivers (Receives):** 15

**Conclusion:** Synchronization parity analysis detected no unmatched broadcast/send-receive channel declarations. While this confirms parity, it does not guarantee executable synchronization correctness, timing compatibility, or semantic synchronization validity. Those properties must be checked via trace equivalence and SMC execution.

## 3. Behavioral Consistency Validation (PART 5)
Structural preservation alone does not guarantee stochastic semantic equivalence. The modularization process (renaming variables, extracting systems) could alter stochastic transition structure or probabilistic execution semantics. 

To formally validate behavioral preservation, the framework must compare the original monolithic `ADRT.xml` against the modularized architecture using identical SMC queries.

**Methodology for Behavioral Preservation:**
1. **Comparative Reachability Analysis:** Run `baseline_queries.q` against `ADRT.xml` and `modular_queries.q` against `main_system.xml`. 
2. **Probabilistic Result Comparison:** Ensure `Pr[<=t]` queries yield probabilities within an expected statistical confidence interval across both models.
3. **Synchronization Trace Comparison:** Validate that critical event sequences (e.g., `start_net` -> `detect`) execute in the same order.
4. **Timing Distribution Analysis:** Check that delay bounds and rate exponentials still generate identical probability mass functions.

*Note: If probabilistic outputs diverge significantly after modularization, then synchronization semantics or stochastic interleavings may have changed.*

## 4. State-Space Explosion Risks & Queueing Semantics (PART 8)
**Refactored Variables:** Load abstractions (`wafLoad`, `firewallLoad`) were refactored toward queue-oriented semantics (`wafQueueSize`, `fwQueueSize`) to prepare for future queueing-theoretic formalization. True formal M/M/1 queuing semantics (arrival processes, service processes, continuous dequeue logic) are planned extensions, and the current integers serve as bounded abstractions.

**Scalability Risks:** The transition from bounded global booleans/ints to open queue metrics significantly increases synchronization density and topology coupling. This risks continuous-state complexity and combinatorial explosions during verification. 

**Recommended Strategies:**
1. Leverage bounded abstractions by setting strict limits (e.g., `fwQueueSize < 100`).
2. Utilize UPPAAL SMC for bounded-time probability evaluations (`Pr[<=time]`) to bypass infinite-state bottlenecks associated with exhaustive reachability checks (`E<>`).
3. Deploy reduced-order approximations if topology coupling produces excessive synchronization overhead.
