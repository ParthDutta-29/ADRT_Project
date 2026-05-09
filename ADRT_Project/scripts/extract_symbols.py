import xml.etree.ElementTree as ET
import re

tree = ET.parse('../build/main_system.xml')
root = tree.getroot()

templates = {}
for t in root.findall('template'):
    name = t.find('name').text
    locs = [l.find('name').text for l in t.findall('location') if l.find('name') is not None]
    templates[name] = locs

global_decl = root.find('declaration').text or ""

# Simple variable extraction
vars = []
for line in global_decl.split(';'):
    line = line.strip()
    if not line or line.startswith('/*') or line.startswith('//') or line.startswith('typedef') or '{' in line:
        continue
    line = re.sub(r'const\s+', '', line)
    line = re.sub(r'broadcast\s+', '', line)
    line = re.sub(r'urgent\s+', '', line)
    parts = line.split()
    if len(parts) >= 2:
        var_list = " ".join(parts[1:])
        var_list = re.sub(r'=.*?(,|$)', r'\1', var_list)
        for v in var_list.split(','):
            v_name = v.strip().split()[0] if v.strip() else ""
            v_name = re.sub(r'\[.*\]', '', v_name)
            if v_name:
                vars.append(v_name)

print("Templates and Locations:")
for t, locs in templates.items():
    print(f"  {t}: {locs}")
    
print("\nGlobal Variables:")
print(f"  {vars}")
