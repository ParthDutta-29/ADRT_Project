import xml.etree.ElementTree as ET
import re

files = ['../src/attack_layer.xml', '../src/defense_layer.xml', '../src/human_layer.xml']

for file in files:
    tree = ET.parse(file)
    root = tree.getroot()
    changed = False

    for trans in root.findall('.//transition'):
        assign = trans.find('label[@kind="assignment"]')
        if assign is not None and assign.text:
            text = assign.text
            # Remove heuristic assignments
            text = re.sub(r'riskScore=[^\n,]+', '', text)
            text = re.sub(r'severity=[^\n,]+', '', text)
            text = re.sub(r'threat_score=[^\n,]+', '', text)
            text = re.sub(r'defense_score=[^\n,]+', '', text)
            text = re.sub(r'riskScore\s*:?=\s*[^\n,]+', '', text)
            
            # Clean up dangling commas and newlines
            lines = [line.strip() for line in text.split(',')]
            lines = [line for line in lines if line]
            text = ',\n'.join(lines)
            
            # Add probabilistic semantics at specific points
            sync = trans.find('label[@kind="synchronisation"]')
            if sync is not None:
                if sync.text in ['start_net?', 'start_web?', 'start_api?', 'start_malware?', 'start_ransom?', 'start_phish?', 'start_cred?', 'start_insider?', 'start_supply?', 'start_firmware?', 'start_lateral?', 'start_persist?']:
                    text += ",\nbreachLikelihood=min(100,breachLikelihood+5)"
                if sync.text == 'success?':
                    text += ",\ncpsInstabilityProbability=min(100,cpsInstabilityProbability+10)"
            
            if assign.text != text:
                assign.text = text
                changed = True

    # human_layer specific additions
    if 'human_layer' in file:
        for trans in root.findall('.//transition'):
            src = trans.find('source')
            tgt = trans.find('target')
            if src is not None and tgt is not None:
                # Add to Intake -> Classify (id542 -> id543)
                if src.attrib['ref'] == 'id542' and tgt.attrib['ref'] == 'id543':
                    assign = trans.find('label[@kind="assignment"]')
                    if assign is not None:
                        if 'mitigationConfidence' not in assign.text:
                            assign.text += ",\nmitigationConfidence=(telemetryTrust+actuatorTrust)/2,\nresilienceDegradation=min(100, processDeviation + (100-mitigationConfidence)/2)"
                            changed = True
                # Add to Classify -> Risk_Score (id543 -> id544)
                if src.attrib['ref'] == 'id543' and tgt.attrib['ref'] == 'id544':
                    assign = trans.find('label[@kind="assignment"]')
                    if assign is not None:
                        if 'operationalSafetyErosion' not in assign.text:
                            assign.text += ",\noperationalSafetyErosion=(100-safetyMargin)"
                            changed = True
                # Recover -> Harden
                if src.attrib['ref'] == 'id554' and tgt.attrib['ref'] == 'id555':
                    assign = trans.find('label[@kind="assignment"]')
                    if assign is not None:
                        if 'resilienceDegradation' not in assign.text:
                            assign.text += ",\nresilienceDegradation=(resilienceDegradation>10)?resilienceDegradation-10:0,\nmitigationConfidence=min(100,mitigationConfidence+10)"
                            changed = True

    if changed:
        tree.write(file, xml_declaration=True, encoding='utf-8')
        print(f"Updated {file}")
