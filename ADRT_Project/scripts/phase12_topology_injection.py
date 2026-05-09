import xml.etree.ElementTree as ET
import glob
import re

def process_file(filename):
    tree = ET.parse(filename)
    changed = False
    
    for t in tree.getroot().findall('.//transition'):
        t_id = t.attrib.get('id')
        labels = t.findall('label')
        
        # We need to find assignments to modify
        for l in labels:
            if l.attrib.get('kind') == 'assignment' and l.text:
                new_text = l.text
                
                # 1. SCADA Compromise Differentiation
                if 'telemetryTrust' in new_text and 'telemetryTrust=max(0, telemetryTrust-' in new_text:
                    # Make it hit localized telemetry and delayed telemetry harder
                    new_text = re.sub(r'telemetryTrust=max\(0, telemetryTrust-([0-9]+)\)', r'telemetryTrust=max(0, telemetryTrust-\1), localizedTelemetryTrust_A=max(0, localizedTelemetryTrust_A-20), delayedTelemetry=min(100, delayedTelemetry + 10)', new_text)

                # 2. PLC Logic Manipulation Differentiation
                # Look for processDeviation increments and accelerate them
                if 'processDeviation=min(100, processDeviation' in new_text:
                    # Accelerate
                    new_text = re.sub(r'processDeviation=min\(100, processDeviation \+ \(\(100-processDeviation\)/10\)\)', r'processDeviation=min(100, processDeviation + ((100-processDeviation)/5))', new_text)
                    
                # 3. Malicious Valve Actuation Differentiation
                # Look for controlLatency
                if 'controlLatency=min(100, controlLatency' in new_text:
                    new_text = new_text + ", segmentStress_A=min(100, segmentStress_A + 15)"
                    
                # 4. Pipeline Physical Dynamics (Propagating downstream)
                if 'operationalStress=min(100, operationalStress' in new_text:
                    # Add segmented propagation logic
                    # If segmentStress_A gets high, it spills to segmentStress_B
                    propagation_logic = ", segmentStress_B=(segmentStress_A>=70)?min(100, segmentStress_B + 10):segmentStress_B"
                    if propagation_logic not in new_text:
                        new_text = new_text + propagation_logic
                        
                # 5. Incident Response / Isolation
                if 'safeModeOperation' in new_text and 'safeModeOperation=min(100' in new_text:
                    isolation_logic = ", segmentShutdown_A=(segmentStress_A>=80)?1:0"
                    if isolation_logic not in new_text:
                        new_text = new_text + isolation_logic
                
                if new_text != l.text:
                    l.text = new_text
                    changed = True

    if changed:
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Updated operational semantics in {filename}")

for f in glob.glob('../src/*.xml'):
    process_file(f)
