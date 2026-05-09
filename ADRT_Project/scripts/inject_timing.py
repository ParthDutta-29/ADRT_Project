import xml.etree.ElementTree as ET

def add_timing_dynamics_human():
    tree = ET.parse('../src/human_layer.xml')
    root = tree.getroot()
    
    for template in root.findall('template'):
        if template.find('name').text == 'Defender_Response':
            for loc in template.findall('location'):
                name_elem = loc.find('name')
                if name_elem is not None:
                    name = name_elem.text
                    # Apply delay to Intake, Classify, Risk_Score, Sev, Strat, Act
                    if any(x in name for x in ['Intake', 'Classify', 'Risk_Score', 'Sev', 'Strat', 'Act']):
                        expr_label = loc.find('label[@kind="exponentialrate"]')
                        if expr_label is not None:
                            old_val = expr_label.text
                            # Introduce telemetry staleness & SOC delay
                            expr_label.text = f"(fwQueueSize>50 || idsQueueSize>50) ? 1 : {old_val}"
                            
    tree.write('../src/human_layer.xml', xml_declaration=True, encoding='utf-8')

def add_timing_dynamics_defense():
    tree = ET.parse('../src/defense_layer.xml')
    root = tree.getroot()
    
    q_vars = {
        'Firewall_Defense': 'fwQueueSize',
        'IDS_Defense': 'idsQueueSize',
        'WAF_Defense': 'wafQueueSize',
        'EDR_Defense': 'edrQueueSize',
        'DLP_Defense': 'dlpQueueSize'
    }
    
    for template in root.findall('template'):
        name = template.find('name').text
        if name in q_vars:
            qvar = q_vars[name]
            for loc in template.findall('location'):
                loc_name_elem = loc.find('name')
                if loc_name_elem is not None:
                    loc_name = loc_name_elem.text
                    if any(x in loc_name for x in ['Alert', 'Analyse', 'Rule', 'Block', 'Contain']):
                        expr_label = loc.find('label[@kind="exponentialrate"]')
                        if expr_label is not None:
                            old_val = expr_label.text
                            # Introduce delayed mitigation
                            expr_label.text = f"({qvar}>50) ? 1 : {old_val}"
                            
    tree.write('../src/defense_layer.xml', xml_declaration=True, encoding='utf-8')

if __name__ == '__main__':
    add_timing_dynamics_human()
    add_timing_dynamics_defense()
    print("Timing dynamics injected successfully.")
