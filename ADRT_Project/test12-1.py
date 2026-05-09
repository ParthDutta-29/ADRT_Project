import os
import re
import glob
import xml.etree.ElementTree as ET

# ============================================================
# Phase 12.1 — Dynamic Arithmetic Stability Repair
# ------------------------------------------------------------
# Fixes:
#
# 1. Unsafe:
#       max(0, VAR - X)
#
#    Converts to:
#       (VAR >= X) ? VAR - X : 0
#
# 2. Unsafe mismatched guards:
#       (VAR >= 10) ? VAR - (dynamic_expr) : 0
#
#    Converts to:
#       (VAR >= (dynamic_expr)) ? VAR - (dynamic_expr) : 0
#
# 3. Generates detailed repair log
#
# ============================================================

ROOTS = ["src", "build"]

REPORT_FILE = "phase12_1_dynamic_arithmetic_repair_report.txt"

total_repairs = 0
report_lines = []

# ============================================================
# REGEX PATTERNS
# ============================================================

# Pattern 1:
# VAR=max(0, VAR-EXPR)
MAX_PATTERN = re.compile(
    r'(\w+)\s*=\s*max\s*\(\s*0\s*,\s*\1\s*-\s*([^)]+?)\s*\)'
)

# Pattern 2:
# (VAR>=CONST)?VAR-(EXPR):0
GUARD_PATTERN = re.compile(
    r'\(\s*(\w+)\s*>=\s*([^)]+?)\s*\)\s*\?\s*'
    r'\1\s*-\s*\(?([^)?:]+?)\)?\s*:\s*0'
)

# ============================================================
# HELPERS
# ============================================================

def log_change(file_path, transition_id, old, new):
    global total_repairs

    total_repairs += 1

    entry = f"""
================================================
FILE       : {file_path}
TRANSITION : {transition_id}

OLD:
{old}

NEW:
{new}
================================================
"""
    report_lines.append(entry)

    print(entry)


# ============================================================
# FIX MAX(0, x-y)
# ============================================================

def repair_max_pattern(text, file_path, transition_id):

    changed = False

    def repl(match):
        nonlocal changed

        var = match.group(1).strip()
        expr = match.group(2).strip()

        old = match.group(0)

        new = f"{var}=({var}>={expr})?{var}-{expr}:0"

        log_change(file_path, transition_id, old, new)

        changed = True

        return new

    new_text = MAX_PATTERN.sub(repl, text)

    return new_text, changed


# ============================================================
# FIX MISMATCHED GUARDS
# ============================================================

def repair_guard_pattern(text, file_path, transition_id):

    changed = False

    def repl(match):
        nonlocal changed

        var = match.group(1).strip()
        old_guard = match.group(2).strip()
        decrement = match.group(3).strip()

        old = match.group(0)

        # Normalize
        decrement_clean = decrement.strip()

        # Already correct
        if old_guard == decrement_clean:
            return old

        new = (
            f"({var}>={decrement_clean})?"
            f"{var}-{decrement_clean}:0"
        )

        log_change(file_path, transition_id, old, new)

        changed = True

        return new

    new_text = GUARD_PATTERN.sub(repl, text)

    return new_text, changed


# ============================================================
# PROCESS XML FILE
# ============================================================

def process_xml(file_path):

    changed = False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

    except Exception as e:
        print(f"[ERROR] Failed parsing {file_path}: {e}")
        return

    print("\n================================================")
    print(f"SCANNING: {file_path}")
    print("================================================")

    for transition in root.findall(".//transition"):

        tid = transition.attrib.get("id", "UNKNOWN")

        for label in transition.findall("label"):

            if label.attrib.get("kind") != "assignment":
                continue

            if not label.text:
                continue

            original = label.text
            updated = original

            # ----------------------------------------
            # PASS 1 — max(0, x-y)
            # ----------------------------------------

            updated, c1 = repair_max_pattern(
                updated,
                file_path,
                tid
            )

            # ----------------------------------------
            # PASS 2 — mismatched guards
            # ----------------------------------------

            updated, c2 = repair_guard_pattern(
                updated,
                file_path,
                tid
            )

            if c1 or c2:
                label.text = updated
                changed = True

    # ========================================================
    # SAVE FILE
    # ========================================================

    if changed:
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"[SAVED] {file_path}")


# ============================================================
# MAIN
# ============================================================

print("\n================================================")
print("PHASE 12.1 — DYNAMIC ARITHMETIC STABILITY REPAIR")
print("================================================")

for root_dir in ROOTS:

    if not os.path.exists(root_dir):
        continue

    xml_files = glob.glob(os.path.join(root_dir, "*.xml"))

    for xml_file in xml_files:
        process_xml(xml_file)

# ============================================================
# WRITE REPORT
# ============================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("""
================================================
PHASE 12.1 — DYNAMIC ARITHMETIC STABILITY REPAIR
================================================
""")

    for line in report_lines:
        f.write(line)

    f.write(f"""

================================================
TOTAL REPAIRS: {total_repairs}
================================================
""")

print("\n================================================")
print("REPAIR COMPLETE")
print("================================================")
print(f"TOTAL REPAIRS: {total_repairs}")
print(f"REPORT FILE  : {REPORT_FILE}")
print("================================================")