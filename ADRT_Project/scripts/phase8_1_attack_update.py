import xml.etree.ElementTree as ET

tree = ET.parse('../src/attack_layer.xml')
root = tree.getroot()
changed = False

for t in root.findall('.//transition'):
    for l in t.findall('label'):
        if l.attrib.get('kind') == 'assignment':
            text = l.text

            if 'breachLikelihood=min(100,breachLikelihood+5)' in text:
                text = text.replace('breachLikelihood=min(100,breachLikelihood+5)', 'breachLikelihood=min(100, breachLikelihood + operationalStress/10)')
                changed = True
            if 'sensorSpoofingIntent=(stealthPreference>50)?min(100,\nsensorSpoofingIntent+10):sensorSpoofingIntent' in text:
                text = text.replace('sensorSpoofingIntent=(stealthPreference>50)?min(100,\nsensorSpoofingIntent+10):sensorSpoofingIntent', 'sensorSpoofingIntent=(stealthPreference>50)?min(100, sensorSpoofingIntent + stealthPreference/10):sensorSpoofingIntent')
                changed = True
            if 'telemetryIntegrity=(sensorSpoofingIntent>40 && telemetryIntegrity>=5)?telemetryIntegrity-5:telemetryIntegrity' in text:
                text = text.replace('telemetryIntegrity=(sensorSpoofingIntent>40 && telemetryIntegrity>=5)?telemetryIntegrity-5:telemetryIntegrity', 'telemetryIntegrity=(sensorSpoofingIntent>40)?((telemetryIntegrity>5)?telemetryIntegrity-(sensorSpoofingIntent/10):0):telemetryIntegrity')
                changed = True
            if 'processDeviation=(telemetryTrust<50)?min(100,\nprocessDeviation+5):processDeviation' in text:
                text = text.replace('processDeviation=(telemetryTrust<50)?min(100,\nprocessDeviation+5):processDeviation', 'processDeviation=(telemetryTrust<50)?min(100, processDeviation + (100-telemetryTrust)/10):processDeviation')
                changed = True
            if 'controlLoopStability=(controlLoopStability>=10)?controlLoopStability-10:0' in text:
                text = text.replace('controlLoopStability=(controlLoopStability>=10)?controlLoopStability-10:0', 'controlLoopStability=(controlLoopStability>=10)?controlLoopStability-(processDeviation/10):0')
                changed = True
            if 'processDeviation=min(100,\nprocessDeviation+10)' in text:
                text = text.replace('processDeviation=min(100,\nprocessDeviation+10)', 'processDeviation=min(100, processDeviation + operationalStress/10)')
                changed = True
            if 'cpsInstabilityProbability=min(100,cpsInstabilityProbability+10)' in text:
                text = text.replace('cpsInstabilityProbability=min(100,cpsInstabilityProbability+10)', 'cpsInstabilityProbability=min(100, cpsInstabilityProbability + processDeviation/10)')
                changed = True
            if 'stealthPreference=min(100,\nstealthPreference+10)' in text:
                text = text.replace('stealthPreference=min(100,\nstealthPreference+10)', 'stealthPreference=min(100, stealthPreference + (100-stealthPreference)/10)')
                changed = True
            if 'operationalStress=(controlLoopStability<50)?min(100,\noperationalStress+10):operationalStress' in text:
                text = text.replace('operationalStress=(controlLoopStability<50)?min(100,\noperationalStress+10):operationalStress', 'operationalStress=(controlLoopStability<50)?min(100, operationalStress + (100-controlLoopStability)/10):operationalStress')
                changed = True
            if 'fwQueueSize=min(100,\nfwQueueSize+5)' in text:
                text = text.replace('fwQueueSize=min(100,\nfwQueueSize+5)', 'fwQueueSize=min(100, fwQueueSize + 1 + congestionPressure/20)')
                changed = True
            if 'idsQueueSize=min(100,\nidsQueueSize+5)' in text:
                text = text.replace('idsQueueSize=min(100,\nidsQueueSize+5)', 'idsQueueSize=min(100, idsQueueSize + 1 + congestionPressure/20)')
                changed = True
            if 'wafQueueSize=min(100,\nwafQueueSize+5)' in text:
                text = text.replace('wafQueueSize=min(100,\nwafQueueSize+5)', 'wafQueueSize=min(100, wafQueueSize + 1 + congestionPressure/20)')
                changed = True
            if 'edrQueueSize=min(100,\nedrQueueSize+5)' in text:
                text = text.replace('edrQueueSize=min(100,\nedrQueueSize+5)', 'edrQueueSize=min(100, edrQueueSize + 1 + congestionPressure/20)')
                changed = True
            if 'dlpQueueSize=min(100,\ndlpQueueSize+5)' in text:
                text = text.replace('dlpQueueSize=min(100,\ndlpQueueSize+5)', 'dlpQueueSize=min(100, dlpQueueSize + 1 + congestionPressure/20)')
                changed = True

            if text != l.text:
                l.text = text

if changed:
    tree.write('../src/attack_layer.xml', encoding='utf-8', xml_declaration=True)
    print('Updated attack_layer.xml')
