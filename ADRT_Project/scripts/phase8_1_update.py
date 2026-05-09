import glob, re
import xml.etree.ElementTree as ET

def update_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    changed = False
    
    # Probability replacements
    prob_map = {
        'detectionReliability + telemetryTrust': '1 + detectionReliability/20 + telemetryTrust/25',
        'telemetryCoverage + telemetryTrust': '1 + telemetryCoverage/20 + telemetryTrust/25',
        'inspectionDepth + telemetryTrust': '1 + inspectionDepth/20 + telemetryTrust/25',
        'modelFidelity + telemetryTrust': '1 + modelFidelity/20 + telemetryTrust/25',
        'mitigationEffectiveness + telemetryTrust': '1 + mitigationEffectiveness/20 + telemetryTrust/25',
        '100 + congestionPressure - mitigationConfidence': '1 + congestionPressure/20 + operationalStress/25',
        'stealthPreference + congestionPressure': '1 + stealthPreference/25 + congestionPressure/20',
        'mitigationConfidence + telemetryTrust': '1 + mitigationConfidence/25 + telemetryTrust/20',
        'stealthPreference + processDeviation': '1 + stealthPreference/25 + processDeviation/20',
        'mitigationConfidence + controlLoopStability': '1 + mitigationConfidence/25 + controlLoopStability/20'
    }

    for t in root.findall('.//transition'):
        for l in t.findall('label'):
            # Update probabilities
            if l.attrib.get('kind') == 'probability':
                text = l.text.strip()
                if text in prob_map:
                    l.text = prob_map[text]
                    changed = True

            # Update assignments
            elif l.attrib.get('kind') == 'assignment':
                text = l.text
                
                # Improvement variables (diminishing returns)
                improvements = [
                    'detectionReliability', 'telemetryCoverage', 'inspectionDepth',
                    'modelFidelity', 'mitigationEffectiveness'
                ]
                for var in improvements:
                    old_str = f'{var}=min(100, {var} + 5)'
                    new_str = f'{var}=min(100, {var} + (100-{var})/10)'
                    if old_str in text:
                        text = text.replace(old_str, new_str)
                        changed = True
                    old_str2 = f'{var}=min(100,{var}+5)'
                    if old_str2 in text:
                        text = text.replace(old_str2, new_str)
                        changed = True
                    old_str3 = f'{var}=min(100, {var}+5)'
                    if old_str3 in text:
                        text = text.replace(old_str3, new_str)
                        changed = True

                # Queue variables
                queues = ['fwQueueSize', 'idsQueueSize', 'wafQueueSize', 'edrQueueSize', 'dlpQueueSize']
                for var in queues:
                    old_str = f'{var}=min(100,{var}+5)'
                    new_str = f'{var}=min(100,{var} + 1 + congestionPressure/20)'
                    if old_str in text:
                        text = text.replace(old_str, new_str)
                        changed = True
                    old_str2 = f'{var}=min(100, {var}+5)'
                    if old_str2 in text:
                        text = text.replace(old_str2, new_str)
                        changed = True
                    old_str3 = f'{var}=min(100, {var} + 5)'
                    if old_str3 in text:
                        text = text.replace(old_str3, new_str)
                        changed = True
                    old_str4 = f'{var}=min(100,{var}+10)'
                    new_str4 = f'{var}=min(100,{var} + 2 + congestionPressure/10)'
                    if old_str4 in text:
                        text = text.replace(old_str4, new_str4)
                        changed = True

                # Physical degradations
                if 'processDeviation=min(100,processDeviation+15)' in text:
                    text = text.replace('processDeviation=min(100,processDeviation+15)', 'processDeviation=min(100, processDeviation + operationalStress/10)')
                    changed = True
                
                if 'delayedTelemetry=min(100, delayedTelemetry+10)' in text:
                    text = text.replace('delayedTelemetry=min(100, delayedTelemetry+10)', 'delayedTelemetry=min(100, delayedTelemetry + processDeviation/15)')
                    changed = True
                
                if 'sensorDisagreement=min(100, sensorDisagreement+15)' in text:
                    text = text.replace('sensorDisagreement=min(100, sensorDisagreement+15)', 'sensorDisagreement=min(100, sensorDisagreement + processDeviation/10)')
                    changed = True

                if 'actuatorInconsistency=min(100, actuatorInconsistency+15)' in text:
                    text = text.replace('actuatorInconsistency=min(100, actuatorInconsistency+15)', 'actuatorInconsistency=min(100, actuatorInconsistency + operationalStress/10)')
                    changed = True
                    
                if 'controlLatency=min(100, controlLatency+20)' in text:
                    text = text.replace('controlLatency=min(100, controlLatency+20)', 'controlLatency=min(100, controlLatency + operationalStress/5)')
                    changed = True

                if 'processStabilizationLag=min(100, processStabilizationLag+10)' in text:
                    text = text.replace('processStabilizationLag=min(100, processStabilizationLag+10)', 'processStabilizationLag=min(100, processStabilizationLag + processDeviation/10)')
                    changed = True

                if 'operationalSafetyErosion=min(100, operationalSafetyErosion + processDeviation/5)' in text:
                    text = text.replace('operationalSafetyErosion=min(100, operationalSafetyErosion + processDeviation/5)', 'operationalSafetyErosion=min(100, operationalSafetyErosion + (processDeviation + controlLatency)/10)')
                    changed = True

                # Telemetry Integrity degradation
                if 'telemetryIntegrity=min(100,telemetryIntegrity+10)' in text:
                    text = text.replace('telemetryIntegrity=min(100,telemetryIntegrity+10)', 'telemetryIntegrity=min(100, telemetryIntegrity + (100-telemetryIntegrity)/10)')
                    changed = True

                # Actuator Trust
                if 'actuatorTrust=min(100,actuatorTrust+10)' in text:
                    text = text.replace('actuatorTrust=min(100,actuatorTrust+10)', 'actuatorTrust=min(100, actuatorTrust + (100-actuatorTrust)/10)')
                    changed = True

                if 'controlLoopStability=min(100,controlLoopStability+10)' in text:
                    text = text.replace('controlLoopStability=min(100,controlLoopStability+10)', 'controlLoopStability=min(100, controlLoopStability + (100-controlLoopStability)/10)')
                    changed = True

                # Resilience degradation
                if 'resilienceDegradation=min(100,resilienceDegradation+3)' in text:
                    text = text.replace('resilienceDegradation=min(100,resilienceDegradation+3)', 'resilienceDegradation=min(100, resilienceDegradation + congestionPressure/20)')
                    changed = True
                if 'resilienceDegradation=min(100,resilienceDegradation+4)' in text:
                    text = text.replace('resilienceDegradation=min(100,resilienceDegradation+4)', 'resilienceDegradation=min(100, resilienceDegradation + operationalStress/15)')
                    changed = True
                if 'resilienceDegradation=min(100,resilienceDegradation+vg_count*2)' in text:
                    text = text.replace('resilienceDegradation=min(100,resilienceDegradation+vg_count*2)', 'resilienceDegradation=min(100, resilienceDegradation + vg_count + congestionPressure/20)')
                    changed = True
                if 'resilienceDegradation=min(100,resilienceDegradation+or2_hits*2)' in text:
                    text = text.replace('resilienceDegradation=min(100,resilienceDegradation+or2_hits*2)', 'resilienceDegradation=min(100, resilienceDegradation + or2_hits + operationalStress/20)')
                    changed = True
                if 'resilienceDegradation=min(100,resilienceDegradation+or_hits)' in text:
                    text = text.replace('resilienceDegradation=min(100,resilienceDegradation+or_hits)', 'resilienceDegradation=min(100, resilienceDegradation + or_hits + congestionPressure/25)')
                    changed = True

                if l.text != text:
                    l.text = text
                    changed = True

    if changed:
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Updated {filename}")

for f in glob.glob('../src/*.xml'):
    update_xml(f)
