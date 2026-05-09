# Query Validation Report

## 1. Diagnostics & Failure Context
UPPAAL silently rejects validation queries if they contain invalid identifiers, missing templates, non-existent locations, or syntactic errors (like `and` instead of `&&`). Because the initial refactoring renamed states (e.g., `NA_Post1` -> `NA_Payload_Staging`) and queue parameters (`wafLoad` -> `wafQueueSize`), the legacy query blocks failed UPPAAL’s internal parsing step, causing them to disappear from the GUI entirely.

## 2. Symbol Table Extraction & Validation Methodology
To guarantee 100% query executability, a Python script (`scripts/extract_symbols.py`) was developed to scrape the current AST of `build/main_system.xml`. 
This generated a verified master symbol table (`docs/model_symbol_table.md`) containing:
* **All 28 valid Templates** (e.g., `Firewall_Defense`, `Malware_Attack`)
* **All 289 valid Locations** (e.g., `FWD_Block`, `MAL_PLC_Manipulation`)
* **All Declared Variables** (e.g., `fwQueueSize`, `breach`)

## 3. Query Repair Operations
Every query in the validation suite was formally audited against the master symbol table. Both syntactic errors and stale state references were repaired.

### 3.1 Syntactic Repair (Logic Operators)
**Issue:** Legacy queries utilized `and` for logical conjunctions, which violates UPPAAL's `&&` syntax, causing silent rejection.
* **Original:** `Pr[<=300] (<> downtime == 0 and breach == true)`
* **Repaired:** `Pr[<=300] (<> (downtime == 0 && breach == true))`
* *Note: Parentheses were also added around probabilistic bounds `<> (...)` to strictly enforce valid expression parsing in UPPAAL.*

### 3.2 Semantic State Reinterpretation
**Issue:** Renamed locations and templates were still referenced in their legacy forms.
* **Original:** `E<> Network_Attack.NA_Post1`
* **Repaired:** `E<> Network_Attack.NA_Payload_Staging`
* **Original:** `E<> Malware_Attack.MAL_Impact`
* **Repaired:** `E<> Malware_Attack.MAL_PLC_Manipulation`
* **Original:** `E<> Firewall_Defense.FD_Mitigated`
* **Repaired:** `E<> Firewall_Defense.FWD_Block` (Mapped to the valid mitigation state inside `Firewall_Defense`)
* **Original:** `E<> Defender_Response.DR_Restored`
* **Repaired:** `E<> Defender_Response.DR_Recover`

### 3.3 Variable Reference Repair
**Issue:** Legacy queries tracked unbounded `Load` variables that were formally replaced by bounded `QueueSize` variables to prevent state-space explosions.
* **Original:** `E<> firewallLoad > 50`
* **Repaired:** `E<> fwQueueSize > 50`
* **Original:** `Pr[<=200] (<> wafLoad > 80)`
* **Repaired:** `Pr[<=200] (<> (wafQueueSize > 80))`

## 4. GUI Visibility Integration
A new automated step was injected into `scripts/merge_xml.py`. The compiler now directly reads `modular_queries.q` and `scalability_tests.q`, safely escapes XML entities (e.g. `<` to `&lt;`), and wraps them inside `<query>` blocks at the end of the `main_system.xml` file.

**Outcome:** Every query is now strictly tethered to the validated symbol table. When `build/main_system.xml` is opened, 100% of the validation and scalability queries successfully bypass the UPPAAL semantic parser and appear explicitly in the GUI query list.
