import xml.etree.ElementTree as ET

tree = ET.parse('../src/attack_layer.xml')
root = tree.getroot()

for template in root.findall('template'):
    tname = template.find('name').text

    qname = 'fwQueueSize'
    if tname in ['Web_Attack', 'API_Attack']: qname = 'wafQueueSize'
    if tname in ['Malware_Attack', 'Ransomware_Attack']: qname = 'edrQueueSize'
    if tname == 'Phishing_Attack': qname = 'dlpQueueSize'

    # Update exponential rates
    for loc in template.findall('location'):
        name_elem = loc.find('name')
        if name_elem is not None:
            lname = name_elem.text
            exp_label = loc.find('label[@kind="exponentialrate"]')
            if exp_label is not None:
                if lname.endswith('_Evasion_Evasion_Check'):
                    exp_label.text = f"({qname}>=80) ? 5 : 3"
                elif lname.endswith('_Execution'):
                    exp_label.text = f"(alertConfidence<=30 || stealthPreference>70) ? 1 : ({qname}>=80) ? 5 : 3"
                elif lname.endswith('_Payload_Staging'):
                    exp_label.text = f"(alertConfidence<=30 || stealthPreference>70) ? 1 : 2"
                elif lname.endswith('_OT_Traversal'):
                    # if queue is high, probability of traversal increases (represented by rate increase)
                    exp_label.text = f"({qname}>=80) ? 5 : 3"

    # Update transitions
    for trans in template.findall('transition'):
        src_elem = trans.find('source')
        tgt_elem = trans.find('target')
        if src_elem is None or tgt_elem is None: continue

        # Check if fail?
        sync = trans.find('label[@kind="synchronisation"]')
        if sync is not None and sync.text == 'fail?':
            assign = trans.find('label[@kind="assignment"]')
            if assign is None:
                assign = ET.SubElement(trans, 'label', {'kind': 'assignment'})
                assign.text = "stealthPreference=min(100,stealthPreference+10)"
            else:
                assign.text += ",\nstealthPreference=min(100,stealthPreference+10)"
        
        # Check if detect!
        if sync is not None and sync.text == 'detect!':
            assign = trans.find('label[@kind="assignment"]')
            if assign is None:
                assign = ET.SubElement(trans, 'label', {'kind': 'assignment'})
                assign.text = f"telemetryTrust=(telemetryTrust>10)?telemetryTrust-10:0"
            else:
                assign.text += f",\ntelemetryTrust=(telemetryTrust>10)?telemetryTrust-10:0"

tree.write('../src/attack_layer.xml', xml_declaration=True, encoding='utf-8')
print("Attack layer updated successfully.")
