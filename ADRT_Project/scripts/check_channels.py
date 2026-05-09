import xml.etree.ElementTree as ET
import re

tree = ET.parse('../build/main_system.xml')
root = tree.getroot()

# 1. Extract declared channels
decl_text = root.find('declaration').text or ""
# Match broadcast chan x, y, z; or chan x, y, z;
channels = set()
for line in decl_text.split(';'):
    line = line.strip()
    if 'chan ' in line:
        chans_part = line.split('chan ')[1]
        for ch in chans_part.split(','):
            channels.add(ch.strip())

# 2. Extract used channels in transitions
sends = set()
receives = set()

for t in root.findall('template'):
    for trans in t.findall('transition'):
        for label in trans.findall('label'):
            if label.get('kind') == 'synchronisation':
                sync_val = label.text.strip() if label.text else ""
                if sync_val.endswith('!'):
                    sends.add(sync_val[:-1])
                elif sync_val.endswith('?'):
                    receives.add(sync_val[:-1])

print(f"Declared channels: {len(channels)}")
print(f"Channels with sends: {len(sends)}")
print(f"Channels with receives: {len(receives)}")

# Check for dead channels (declared but never used)
unused = channels - (sends.union(receives))
if unused:
    print(f"WARNING: Unused declared channels: {unused}")

# Check for unmatched sends
unmatched_sends = sends - receives
if unmatched_sends:
    print(f"WARNING: Channels with sends but NO receives: {unmatched_sends}")

# Check for unmatched receives
unmatched_receives = receives - sends
if unmatched_receives:
    print(f"WARNING: Channels with receives but NO sends: {unmatched_receives}")

if not unmatched_sends and not unmatched_receives:
    print("SUCCESS: All synchronization channels are correctly matched.")
