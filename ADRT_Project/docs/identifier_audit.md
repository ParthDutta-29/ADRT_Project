# Identifier Audit Report

## 1. Global Analysis Context
A global static analysis was performed across all 9 modules to trace identifier declarations against usage in transition labels (guards, assignments, updates, synchronizations). 

## 2. Identified Inconsistencies (Pre-Repair)

### 2.1 Undeclared Queue Identifiers
The following queue variables were actively utilized in probability logic and congestion checks throughout `attack_layer.xml` and `defense_layer.xml`, but were completely missing from the global bounds in `global_defs.xml`:
* `fwQueueSize`
* `wafQueueSize`
* `idsQueueSize`
* `edrQueueSize`
* `dlpQueueSize`

### 2.2 Orphaned Variables
The following variables were declared in `global_defs.xml` but entirely unreferenced in the modularized architecture (orphaned due to semantic refactoring):
* `firewallLoad`
* `idsLoad`
* `wafLoad`
* `edrLoad`
* `dlpLoad`

### 2.3 Probable Intended Replacements
The audit confirms a 1:1 mapping error introduced during modular semantic renaming. The `Load` terminology was migrated to `QueueSize` across operational guards and assignments, but the `global_defs.xml` was not aligned to support the new symbolic namespace.

## 3. Post-Repair Status
* **Duplicate Identifiers:** None detected.
* **Orphaned Declarations:** Removed the deprecated `*Load` variables.
* **Broken References:** Repaired by reinstantiating the missing `QueueSize` boundaries in the master symbol table.
* **Resolution:** 100% of identifier references across all templates now map cleanly to a declared variable in `global_defs.xml` or within local template `<declaration>` blocks.
