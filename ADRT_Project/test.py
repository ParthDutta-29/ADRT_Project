import glob
import re
import xml.etree.ElementTree as ET

SEARCH_DIRS = ["src", "build"]

repair_count = 0

print("\n========================================")
print("DEEP DYNAMIC UNDERFLOW REPAIR")
print("========================================")

# detects:
# telemetryIntegrity-(sensorSpoofingIntent/10)

danger_pattern = re.compile(
    r'([a-zA-Z0-9_]+)\s*-\s*\(([a-zA-Z0-9_]+/[0-9]+)\)'
)

# detects unsafe guard:
# telemetryIntegrity>5

guard_pattern_template = r'VAR\s*>\s*[0-9]+'

for directory in SEARCH_DIRS:

    for xml_file in glob.glob(f"{directory}/*.xml"):

        print(f"\nSCANNING: {xml_file}")

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

        except Exception as e:
            print(f"PARSE ERROR: {e}")
            continue

        file_changed = False

        for transition in root.findall(".//transition"):

            tid = transition.attrib.get("id", "UNKNOWN")

            for label in transition.findall("label"):

                if label.attrib.get("kind") != "assignment":
                    continue

                if not label.text:
                    continue

                text = label.text
                original = text

                matches = list(danger_pattern.finditer(text))

                for match in matches:

                    variable = match.group(1)
                    dynamic_expr = match.group(2)

                    # Example:
                    # telemetryIntegrity>5
                    unsafe_guard_regex = (
                        guard_pattern_template
                        .replace("VAR", variable)
                    )

                    unsafe_guard_match = re.search(
                        unsafe_guard_regex,
                        text
                    )

                    if unsafe_guard_match:

                        old_guard = unsafe_guard_match.group(0)

                        # SAFE VERSION:
                        # telemetryIntegrity>=(sensorSpoofingIntent/10)

                        safe_guard = (
                            f"{variable}>=({dynamic_expr})"
                        )

                        text = text.replace(
                            old_guard,
                            safe_guard
                        )

                        repair_count += 1
                        file_changed = True

                        print("\n--------------------------------")
                        print(f"TRANSITION : {tid}")

                        print("\nOLD GUARD:")
                        print(old_guard)

                        print("\nNEW GUARD:")
                        print(safe_guard)

                if text != original:
                    label.text = text

        if file_changed:

            tree.write(
                xml_file,
                encoding="utf-8",
                xml_declaration=True
            )

            print(f"\n[SAVED] {xml_file}")

print("\n========================================")
print("REPAIR COMPLETE")
print("========================================")
print(f"TOTAL REPAIRS: {repair_count}")
print("========================================")