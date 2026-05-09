import glob, xml.etree.ElementTree as ET, re

repairs = []

for filename in glob.glob('../src/*.xml'):
    tree = ET.parse(filename)
    changed = False
    
    for t in tree.getroot().findall('.//transition'):
        t_id = t.attrib.get('id')
        for l in t.findall('label'):
            if l.attrib.get('kind') == 'assignment' and l.text:
                new_text = l.text
                
                # telemetryTrust=(controlLoopStability<50 && telemetryTrust>5)?telemetryTrust-5:telemetryTrust
                if 'telemetryTrust=(controlLoopStability<50 && telemetryTrust>5)?telemetryTrust-5:telemetryTrust' in new_text:
                    new_val = 'telemetryTrust=(controlLoopStability<50)?((telemetryTrust>=5)?telemetryTrust-5:0):telemetryTrust'
                    new_text = new_text.replace('telemetryTrust=(controlLoopStability<50 && telemetryTrust>5)?telemetryTrust-5:telemetryTrust', new_val)
                    repairs.append((filename, t_id, 'telemetryTrust=(controlLoopStability<50 && telemetryTrust>5)?telemetryTrust-5:telemetryTrust', new_val, 'UNDERFLOW_REPAIR', 'Saturated unsafe decrement'))
                    changed = True

                if 'resilienceDegradation=(resilienceDegradation>10)?resilienceDegradation-10:0' in new_text:
                    new_val = 'resilienceDegradation=(resilienceDegradation>=10)?resilienceDegradation-10:0'
                    new_text = new_text.replace('resilienceDegradation=(resilienceDegradation>10)?resilienceDegradation-10:0', new_val)
                    repairs.append((filename, t_id, 'resilienceDegradation=(resilienceDegradation>10)?resilienceDegradation-10:0', new_val, 'UNDERFLOW_REPAIR', 'Fixed threshold'))
                    changed = True

                if 'safetyMargin=(processDeviation>50 && safetyMargin>=10)?safetyMargin-10:safetyMargin' in new_text:
                    new_val = 'safetyMargin=(processDeviation>50)?((safetyMargin>=10)?safetyMargin-10:0):safetyMargin'
                    new_text = new_text.replace('safetyMargin=(processDeviation>50 && safetyMargin>=10)?safetyMargin-10:safetyMargin', new_val)
                    repairs.append((filename, t_id, 'safetyMargin=(processDeviation>50 && safetyMargin>=10)?safetyMargin-10:safetyMargin', new_val, 'UNDERFLOW_REPAIR', 'Saturated unsafe decrement'))
                    changed = True

                if 'recoveryCapacity=(operationalStress>50)?((recoveryCapacity>10)?recoveryCapacity-10:0):recoveryCapacity' in new_text:
                    new_val = 'recoveryCapacity=(operationalStress>50)?((recoveryCapacity>=10)?recoveryCapacity-10:0):recoveryCapacity'
                    new_text = new_text.replace('recoveryCapacity=(operationalStress>50)?((recoveryCapacity>10)?recoveryCapacity-10:0):recoveryCapacity', new_val)
                    repairs.append((filename, t_id, 'recoveryCapacity=(operationalStress>50)?((recoveryCapacity>10)?recoveryCapacity-10:0):recoveryCapacity', new_val, 'UNDERFLOW_REPAIR', 'Fixed threshold'))
                    changed = True
                    
                if 'restorationConfidence=(recoveryCapacity<50 || backupIntegrity<50)?((restorationConfidence>10)?restorationConfidence-10:0):restorationConfidence' in new_text:
                    new_val = 'restorationConfidence=(recoveryCapacity<50 || backupIntegrity<50)?((restorationConfidence>=10)?restorationConfidence-10:0):restorationConfidence'
                    new_text = new_text.replace('restorationConfidence=(recoveryCapacity<50 || backupIntegrity<50)?((restorationConfidence>10)?restorationConfidence-10:0):restorationConfidence', new_val)
                    repairs.append((filename, t_id, 'restorationConfidence...', new_val, 'UNDERFLOW_REPAIR', 'Fixed threshold'))
                    changed = True

                if 'or_hits=(web==true)?or_hits+1:or_hits' in new_text:
                    new_val = 'or_hits=(web==true)?min(100, or_hits+1):or_hits'
                    new_text = new_text.replace('or_hits=(web==true)?or_hits+1:or_hits', new_val)
                    repairs.append((filename, t_id, 'or_hits=(web==true)?or_hits+1:or_hits', new_val, 'OVERFLOW_REPAIR', 'Bound or_hits variable'))
                    changed = True

                if 'or_hits=(api==true)?or_hits+1:or_hits' in new_text:
                    new_val = 'or_hits=(api==true)?min(100, or_hits+1):or_hits'
                    new_text = new_text.replace('or_hits=(api==true)?or_hits+1:or_hits', new_val)
                    repairs.append((filename, t_id, 'or_hits=(api==true)?or_hits+1:or_hits', new_val, 'OVERFLOW_REPAIR', 'Bound or_hits variable'))
                    changed = True
                    
                if 'or2_hits=(ransom==true)?or2_hits+1:or2_hits' in new_text:
                    new_val = 'or2_hits=(ransom==true)?min(100, or2_hits+1):or2_hits'
                    new_text = new_text.replace('or2_hits=(ransom==true)?or2_hits+1:or2_hits', new_val)
                    repairs.append((filename, t_id, 'or2_hits=(ransom==true)?or2_hits+1:or2_hits', new_val, 'OVERFLOW_REPAIR', 'Bound or2_hits variable'))
                    changed = True

                if 'or2_hits=(phishing==true)?or2_hits+1:or2_hits' in new_text:
                    new_val = 'or2_hits=(phishing==true)?min(100, or2_hits+1):or2_hits'
                    new_text = new_text.replace('or2_hits=(phishing==true)?or2_hits+1:or2_hits', new_val)
                    repairs.append((filename, t_id, 'or2_hits=(phishing==true)?or2_hits+1:or2_hits', new_val, 'OVERFLOW_REPAIR', 'Bound or2_hits variable'))
                    changed = True

                if 'vg_count=(firmware==true)?vg_count+1:vg_count' in new_text:
                    new_val = 'vg_count=(firmware==true)?min(100, vg_count+1):vg_count'
                    new_text = new_text.replace('vg_count=(firmware==true)?vg_count+1:vg_count', new_val)
                    repairs.append((filename, t_id, 'vg_count=(firmware==true)?vg_count+1:vg_count', new_val, 'OVERFLOW_REPAIR', 'Bound vg_count variable'))
                    changed = True

                if 'vg_count=(insider==true)?vg_count+1:vg_count' in new_text:
                    new_val = 'vg_count=(insider==true)?min(100, vg_count+1):vg_count'
                    new_text = new_text.replace('vg_count=(insider==true)?vg_count+1:vg_count', new_val)
                    repairs.append((filename, t_id, 'vg_count=(insider==true)?vg_count+1:vg_count', new_val, 'OVERFLOW_REPAIR', 'Bound vg_count variable'))
                    changed = True

                if new_text != l.text:
                    l.text = new_text
                    changed = True

    if changed:
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f'Wrote {filename}')

with open('repairs.log', 'w') as f:
    for r in repairs:
        f.write(f'{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}|{r[5]}\n')
