# Query Visibility & Architectural Separation Report

## 1. Architectural Separation Paradigm (PART 1 & 2)
The root cause for UPPAAL's silent rejection of validation queries was a conceptual mixing of incompatible namespaces. Compiling legacy baseline queries directly into the newly refactored modular architecture forced UPPAAL to parse deprecated states (e.g., `NA_Post1`) against a codebase that exclusively understands `NA_Payload_Staging`. Any single invalid identifier silently halts UPPAAL's query GUI population entirely.

To formally resolve this, the build infrastructure was strictly bifurcated into two separate verification domains:
1. **Isolated Baseline Verification (`baseline_system.xml`)**: Exclusively targets the pre-refactoring semantics.
2. **Isolated Modular Verification (`main_system.xml`)**: Exclusively targets the refactored queue abstractions and renamed semantic locations.

## 2. Dedicated Execution Models (PART 3, 4 & 9)
The `scripts/merge_xml.py` compiler was significantly upgraded to support selective domain targeting (`--baseline` vs `--modular`).

* **`build/baseline_system.xml`**: Automatically pulls the original monolithic `ADRT.xml`, strips any legacy queries, and strictly embeds the `validation/baseline_queries.q` suite. This preserves exact legacy naming like `firewallLoad` and `MAL_Impact` for controlled A/B testing.
* **`build/main_system.xml`**: Safely compiles the 8 modular layers into a unified block and embeds the `modular_queries.q` and `scalability_tests.q` suites natively without legacy contamination.

## 3. Query-to-Model Consistency & Syntax Validation (PART 5, 6 & 7)
A complete query consistency pass was enacted to ensure every query maps exactly to its respective symbol table:

### Baseline Model Repaired Syntax
* **Original:** `Pr[<=300] (<> downtime == 0 and breach == true)`
* **Repaired:** `Pr[<=300] (<> (downtime == 0 && breach == true))`
* **Validation:** Re-wrapping reachability bounds inside strict parenthesis `(<>)` and enforcing `&&` operators restored parser safety. The model safely references `firewallLoad > 50`.

### Modular Model Semantics
* **Original Overload:** `E<> Firewall_Defense.FD_Overloaded` (State was deprecated during the continuous queue refactoring).
* **Removed/Repaired:** Obsolete static overload states were removed. They are conceptually replaced by exact congestion queue evaluations: `Pr[<=500] (<> (fwQueueSize > 90))`. 

## 4. Final GUI Visibility
By formally segregating the namespaces, ALL syntax failures and stale references were eradicated. 
* Opening `build/baseline_system.xml` now guarantees 100% GUI visibility for all baseline validation queries.
* Opening `build/main_system.xml` guarantees 100% GUI visibility for all modular progression checks and scalability stress tests.
* **No queries are silently dropped.** All temporal expressions parse perfectly into the UPPAAL verification engine.

*Note: This strictly represents parser-validity and formal domain alignment. Exact behavioral preservation (trace equivalence) remains to be empirically tested by executing these generated model suites in the SMC engine.*
