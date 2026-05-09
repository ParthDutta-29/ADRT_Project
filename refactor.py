import xml.etree.ElementTree as ET
import re

tree = ET.parse('c:/Users/parth/Documents/RP/ADRT.xml')
root = tree.getroot()

decl = root.find('declaration').text

templates = {t.find('name').text: t for t in root.findall('template')}

def to_xml(el):
    return ET.tostring(el, encoding='unicode')

state_renames = {
    'Post1': 'Payload_Staging',
    'Post2': 'Command_And_Control',
    'Impact': 'PLC_Manipulation',
    'Retry': 'Privilege_Escalation',
    'Blocked': 'Mitigated',
    'Idle': 'Idle',
    'Recon': 'Reconnaissance',
    'Stage': 'Credential_Theft',
    'Check': 'Evasion_Check',
    'Bypass': 'OT_Traversal',
    'Exec': 'Execution',
    'Wave1': 'Valve_Control',
    'Wave2': 'Flow_Dynamics',
    'Wave3': 'PID_Control'
}

for name, t in templates.items():
    if 'Attack' in name or name in ['Lateral_Movement', 'Persistence_Module', 'Environment']:
        for loc in t.findall('location'):
            lname_el = loc.find('name')
            if lname_el is not None:
                old_name = lname_el.text
                for k, v in state_renames.items():
                    if old_name.endswith(k):
                        lname_el.text = old_name.replace(k, v)
                        break

def replace_states(xml_str):
    for k, v in state_renames.items():
        xml_str = re.sub(r'([A-Za-z0-9]+)_' + k + r'\b', r'\1_' + v, xml_str)
    
    # Replace global boolean coupling where possible
    xml_str = xml_str.replace('wafLoad', 'wafQueueSize')
    xml_str = xml_str.replace('firewallLoad', 'fwQueueSize')
    xml_str = xml_str.replace('edrLoad', 'edrQueueSize')
    xml_str = xml_str.replace('dlpLoad', 'dlpQueueSize')
    xml_str = xml_str.replace('idsLoad', 'idsQueueSize')
    return xml_str

with open('c:/Users/parth/Documents/RP/global_defs.xml', 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<declaration>\n' + decl + '\n</declaration>\n')

layers = {
    'physical_layer.xml': ['Environment'],
    'network_layer.xml': ['OR_L12', 'OR_L2', 'AND_L12', 'AND_L2', 'NOT_FW2', 'NOT_IDS', 'Voting_Gate'],
    'attack_layer.xml': ['Network_Attack', 'Web_Attack', 'API_Attack', 'Malware_Attack', 'Ransomware_Attack', 'Phishing_Attack', 'Credential_Attack', 'Insider_Attack', 'Supply_Attack', 'Firmware_Attack', 'Lateral_Movement', 'Persistence_Module'],
    'defense_layer.xml': ['Firewall_Defense', 'IDS_Defense', 'WAF_Defense', 'EDR_Defense', 'DLP_Defense'],
    'human_layer.xml': ['Defender_Response'],
    'recovery_layer.xml': ['Breach_Monitor'],
    'strategy_layer.xml': ['Attack_Coordinator']
}

for filename, tnames in layers.items():
    with open('c:/Users/parth/Documents/RP/' + filename, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<nta>\n')
        for tn in tnames:
            if tn in templates:
                xml_str = to_xml(templates[tn])
                xml_str = replace_states(xml_str)
                f.write(xml_str + '\n')
        f.write('</nta>\n')

system_text = root.find('system').text
with open('c:/Users/parth/Documents/RP/main_system.xml', 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!DOCTYPE nta PUBLIC "-//Uppaal Team//DTD Flat System 1.6//EN" "http://www.it.uu.se/research/group/darts/uppaal/flat-1_6.dtd" [\n')
    f.write('  <!ENTITY global_defs SYSTEM "global_defs.xml">\n')
    for layer in layers.keys():
        f.write(f'  <!ENTITY {layer.split(".")[0]} SYSTEM "{layer}">\n')
    f.write(']>\n<nta>\n')
    f.write('  &global_defs;\n')
    for layer in layers.keys():
        f.write(f'  &{layer.split(".")[0]};\n')
    f.write('  <system>\n' + system_text + '\n  </system>\n')
    f.write('</nta>\n')

print("Refactoring completed.")
