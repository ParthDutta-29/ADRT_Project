import glob, xml.etree.ElementTree as ET, re

def process_file(filename):
    tree = ET.parse(filename)
    changed = False
    
    for t in tree.getroot().findall('.//transition'):
        t_id = t.attrib.get('id')
        for l in t.findall('label'):
            if l.attrib.get('kind') == 'assignment' and l.text:
                new_text = l.text
                
                # Replace +3, +1, +2 with nonlinear if appropriate
                new_text = re.sub(r'([a-zA-Z0-9_]+)=min\(100,\s*\1\s*\+\s*[0-9]+\)', r'\1=min(100, \1 + (100-\1)/10)', new_text)
                
                # Introduce energy escalation with congestion
                new_text = re.sub(r'maintenanceCost\+([A-Z0-9_]+_MC)\*([0-9]+)', r'maintenanceCost+\1*\2 + congestionPressure/10', new_text)
                new_text = re.sub(r'energyCost\+([A-Z0-9_]+_EC)\*([0-9]+)', r'energyCost+\1*\2 + (operationalStress/10)', new_text)
                new_text = re.sub(r'carbonCost\+([A-Z0-9_]+_CC)\*([0-9]+)', r'carbonCost+\1*\2 + (operationalStress/10)', new_text)
                
                # Nonlinear degradation envelope (example for telemetryTrust dropping)
                # telemetryTrust=(telemetryTrust>=10)?telemetryTrust-10:0
                # Let's replace with: telemetryTrust=(telemetryTrust>=(operationalStress/10))?telemetryTrust-(operationalStress/10):0
                new_text = re.sub(r'telemetryTrust=\(telemetryTrust>=10\)\?telemetryTrust-10:0', r'telemetryTrust=(telemetryTrust>=(operationalStress/10))?telemetryTrust-(operationalStress/10):0', new_text)
                
                if new_text != l.text:
                    l.text = new_text
                    changed = True

    if changed:
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f'Wrote {filename}')

for f in glob.glob('../src/*.xml'):
    process_file(f)
