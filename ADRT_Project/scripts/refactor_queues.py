import xml.etree.ElementTree as ET
import os

def refactor_defense_layer():
    tree = ET.parse('../src/defense_layer.xml')
    root = tree.getroot()

    # We will iterate through each defense template
    # Firewall_Defense, IDS_Defense, WAF_Defense, EDR_Defense, DLP_Defense
    
    # Map for queue variables
    q_vars = {
        'Firewall_Defense': 'fwQueueSize',
        'IDS_Defense': 'idsQueueSize',
        'WAF_Defense': 'wafQueueSize',
        'EDR_Defense': 'edrQueueSize',
        'DLP_Defense': 'dlpQueueSize'
    }

    for template in root.findall('template'):
        name = template.find('name').text
        if name not in q_vars:
            continue
            
        qvar = q_vars[name]
        
        # Find locations
        locs = {loc.find('name').text: loc.get('id') for loc in template.findall('location')}
        
        # 1. Idle -> Monitor on detect?
        # We need to add guard qvar < 80 to existing, and create a new one for qvar >= 80
        transitions = template.findall('transition')
        
        # Determine prefix from locations (e.g. FWD, IDSD)
        idle_name = [n for n in locs.keys() if 'Idle' in n][0]
        monitor_name = [n for n in locs.keys() if 'Monitor' in n][0]
        rule_name = [n for n in locs.keys() if 'Rule' in n][0]
        block_name = [n for n in locs.keys() if 'Block' in n][0]
        failed_name = [n for n in locs.keys() if 'Failed' in n][0]
        analyse_name = [n for n in locs.keys() if 'Analyse' in n][0]

        max_id = max([int(t.get('id').replace('id', '')) for t in template.findall('transition')] + 
                     [int(l.get('id').replace('id', '')) for l in template.findall('location')])
                     
        new_transitions = []

        for trans in transitions:
            source = trans.find('source').get('ref')
            target = trans.find('target').get('ref')
            
            sync = trans.find('label[@kind="synchronisation"]')
            sync_text = sync.text if sync is not None else ""
            
            # A) Idle -> Monitor (detect?)
            if source == locs[idle_name] and target == locs[monitor_name] and sync_text == 'detect?':
                # Add guard to existing
                guard = ET.Element('label', {'kind': 'guard', 'x': '70', 'y': '50'})
                guard.text = f"{qvar} < 80"
                trans.append(guard)
                
                # Create congestion failure transition (Idle -> Idle)
                max_id += 1
                t_fail = ET.Element('transition', {'id': f'id{max_id}'})
                ET.SubElement(t_fail, 'source', {'ref': locs[idle_name]})
                ET.SubElement(t_fail, 'target', {'ref': locs[idle_name]})
                g_fail = ET.SubElement(t_fail, 'label', {'kind': 'guard', 'x': '70', 'y': '10'})
                g_fail.text = f"{qvar} >= 80"
                s_fail = ET.SubElement(t_fail, 'label', {'kind': 'synchronisation', 'x': '70', 'y': '25'})
                s_fail.text = 'detect?'
                a_fail = ET.SubElement(t_fail, 'label', {'kind': 'assignment', 'x': '70', 'y': '40'})
                a_fail.text = "falseNegative=true"
                new_transitions.append(t_fail)
                
            # B) Rule -> Block (success!)
            if source == locs[rule_name] and target == locs[block_name] and sync_text == 'success!':
                guard = ET.Element('label', {'kind': 'guard', 'x': '430', 'y': '190'})
                guard.text = f"{qvar} < 80"
                trans.append(guard)
                
            # C) Rule -> Failed (fail!)
            if source == locs[rule_name] and target == locs[failed_name] and sync_text == 'fail!':
                # existing fail path is for normal failure. 
                # wait, if qvar >= 80, it should also go here. We can just change guard to empty or keep two transitions?
                # Actually, UPPAAL allows multiple transitions.
                # Let's just add qvar < 80 to this one, and create a NEW one without 'fail!' sync?
                # No, 'fail!' sync must be sent by Attack. If Attack sends fail! it's received here.
                # Wait, 'success!' and 'fail!' are broadcasts sent by DEFENSE! 
                # Let's check: "success!" is a broadcast. The defense template declares "success!". 
                # So the defense template is the sender.
                
                guard = ET.Element('label', {'kind': 'guard', 'x': '340', 'y': '260'})
                guard.text = f"{qvar} < 80"
                trans.append(guard)
                
                # Create guaranteed fail transition when congested
                max_id += 1
                t_sat = ET.Element('transition', {'id': f'id{max_id}'})
                ET.SubElement(t_sat, 'source', {'ref': locs[rule_name]})
                ET.SubElement(t_sat, 'target', {'ref': locs[failed_name]})
                g_sat = ET.SubElement(t_sat, 'label', {'kind': 'guard', 'x': '340', 'y': '310'})
                g_sat.text = f"{qvar} >= 80"
                s_sat = ET.SubElement(t_sat, 'label', {'kind': 'synchronisation', 'x': '340', 'y': '325'})
                s_sat.text = 'fail!'
                a_sat = ET.SubElement(t_sat, 'label', {'kind': 'assignment', 'x': '340', 'y': '340'})
                # Copy assignment from existing
                assign = trans.find('label[@kind="assignment"]')
                if assign is not None:
                    a_sat.text = assign.text
                new_transitions.append(t_sat)

        # D) Add draining transitions
        # Idle draining
        max_id += 1
        t_drain_idle = ET.Element('transition', {'id': f'id{max_id}'})
        ET.SubElement(t_drain_idle, 'source', {'ref': locs[idle_name]})
        ET.SubElement(t_drain_idle, 'target', {'ref': locs[idle_name]})
        g_di = ET.SubElement(t_drain_idle, 'label', {'kind': 'guard'})
        g_di.text = f"{qvar} > 0"
        a_di = ET.SubElement(t_drain_idle, 'label', {'kind': 'assignment'})
        a_di.text = f"{qvar}=({qvar}>=5)?{qvar}-5:0"
        new_transitions.append(t_drain_idle)

        # Analyse draining
        max_id += 1
        t_drain_ana = ET.Element('transition', {'id': f'id{max_id}'})
        ET.SubElement(t_drain_ana, 'source', {'ref': locs[analyse_name]})
        ET.SubElement(t_drain_ana, 'target', {'ref': locs[analyse_name]})
        g_da = ET.SubElement(t_drain_ana, 'label', {'kind': 'guard'})
        g_da.text = f"{qvar} > 0"
        a_da = ET.SubElement(t_drain_ana, 'label', {'kind': 'assignment'})
        a_da.text = f"{qvar}=({qvar}>=10)?{qvar}-10:0"
        new_transitions.append(t_drain_ana)

        # Append all new transitions
        for nt in new_transitions:
            template.append(nt)

    tree.write('../src/defense_layer.xml', xml_declaration=True, encoding='utf-8')

if __name__ == '__main__':
    refactor_defense_layer()
    print("defense_layer.xml updated successfully.")
