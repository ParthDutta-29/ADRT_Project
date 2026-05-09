import xml.etree.ElementTree as ET

tree = ET.parse('../src/attack_layer.xml')
root = tree.getroot()

for template in root.findall('template'):
    tname = template.find('name').text
    
    for trans in template.findall('transition'):
        src_elem = trans.find('source')
        tgt_elem = trans.find('target')
        if src_elem is None or tgt_elem is None: continue
        
        sync = trans.find('label[@kind="synchronisation"]')
        assign = trans.find('label[@kind="assignment"]')
        
        # Check success? transitions (OT_Traversal -> Execution)
        if sync is not None and sync.text == 'success?':
            if assign is not None and 'threat_score' in assign.text:
                if 'controlLoopStability' not in assign.text:
                    assign.text += ",\ncontrolLoopStability=(controlLoopStability>=10)?controlLoopStability-10:0,\nprocessDeviation=min(100,processDeviation+10)"
                    
        # Check transition Payload_Staging -> Command_And_Control
        if sync is None:
            if assign is not None and 'maintenanceCost' in assign.text and 'breach' not in assign.text and 'downtime' not in assign.text:
                if 'telemetryIntegrity' not in assign.text:
                    assign.text += ",\nsensorSpoofingIntent=(stealthPreference>50)?min(100,sensorSpoofingIntent+10):sensorSpoofingIntent,\ntelemetryIntegrity=(sensorSpoofingIntent>40 && telemetryIntegrity>=5)?telemetryIntegrity-5:telemetryIntegrity,\nprocessDeviation=(telemetryTrust<50)?min(100,processDeviation+5):processDeviation"
                    
        # Check transition Command_And_Control -> PLC_Manipulation (where breach=true)
        if assign is not None and 'breach=true' in assign.text:
            if 'safetyMargin' not in assign.text:
                assign.text += ",\nsafetyMargin=(processDeviation>50 && safetyMargin>=10)?safetyMargin-10:safetyMargin,\noperationalStress=(controlLoopStability<50)?min(100,operationalStress+10):operationalStress"

tree.write('../src/attack_layer.xml', xml_declaration=True, encoding='utf-8')
print('Attack layer updated.')
