import xml.etree.ElementTree as ET

tree = ET.parse('../src/defense_layer.xml')
root = tree.getroot()

for template in root.findall('template'):
    for trans in template.findall('transition'):
        sync = trans.find('label[@kind="synchronisation"]')
        if sync is not None and sync.text == 'detect?':
            guard = trans.find('label[@kind="guard"]')
            if guard is not None and '>= 80' in guard.text:
                assign = trans.find('label[@kind="assignment"]')
                if assign is not None and 'telemetryTrust' in assign.text:
                    if 'actuatorTrust' not in assign.text:
                        assign.text += ',\nactuatorTrust=(actuatorTrust>=5)?actuatorTrust-5:0,\ncontrolLoopStability=(controlLoopStability>=5)?controlLoopStability-5:0'

tree.write('../src/defense_layer.xml', xml_declaration=True, encoding='utf-8')
print('Defense layer updated.')
