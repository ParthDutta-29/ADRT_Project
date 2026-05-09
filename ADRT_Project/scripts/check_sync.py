import xml.etree.ElementTree as ET
import glob
from collections import defaultdict

syncs = defaultdict(list)
for f in glob.glob('../src/*.xml'):
    tree = ET.parse(f)
    for elem in tree.findall('.//label'):
        if elem.attrib.get('kind') == 'synchronisation' and elem.text:
            text = elem.text.strip()
            syncs[text].append(f)

for s in sorted(syncs.keys()):
    print(f'{s}: {len(syncs[s])} times')
    if s.endswith('!'):
        q = s[:-1] + '?'
        if q not in syncs:
            print('  -> WARNING: Missing receiver for', s)
    elif s.endswith('?'):
        ex = s[:-1] + '!'
        if ex not in syncs:
            print('  -> WARNING: Missing sender for', s)
