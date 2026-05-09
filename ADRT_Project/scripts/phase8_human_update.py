import xml.etree.ElementTree as ET

tree = ET.parse('../src/human_layer.xml')
root = tree.getroot()

# Helper to find transition by ID
def get_transition(id_val):
    for t in root.findall('.//transition'):
        if t.attrib.get('id') == id_val:
            return t
    return None

# Helpers for updating label
def update_assignment(t, new_text):
    for l in t.findall('label'):
        if l.attrib.get('kind') == 'assignment':
            # preserve cost logic if possible, or we can just prepend/append
            old_text = l.text
            # keep the cost logic: lines containing MC, EC, CC
            cost_lines = [line.strip() for line in old_text.split(',\n') if 'Cost' in line or 'Cost :=' in line]
            
            # Combine
            l.text = new_text + ",\n" + ",\n".join(cost_lines)

# id571: DR_Contain -> DR_Isolate
t571 = get_transition('id571')
assign571 = """recoveryCapacity=(operationalStress>50)?((recoveryCapacity>10)?recoveryCapacity-10:0):recoveryCapacity,
restorationConfidence=(recoveryCapacity<50 || backupIntegrity<50)?((restorationConfidence>10)?restorationConfidence-10:0):restorationConfidence,
failSafeEngaged=(operationalSafetyErosion>70 && processDeviation>50)?true:failSafeEngaged,
safeModeOperation=(failSafeEngaged)?100:((telemetryTrust<50)?50:0),
downtime=(failSafeEngaged)?downtime+2:((operationalStress>50)?downtime+1:downtime)"""
update_assignment(t571, assign571)

# id572: DR_Isolate -> DR_Recover
t572 = get_transition('id572')
assign572 = """breach=(stealthPreference>70 && mitigationConfidence<50)?true:false,
downtime=(failSafeEngaged)?downtime+2:((operationalStress>50)?downtime+1:((downtime>0)?downtime-1:0))"""
update_assignment(t572, assign572)

# id573: DR_Recover -> DR_Harden
t573 = get_transition('id573')
assign573 = """scadaCompromised=(breach)?true:false,
plcCompromised=(safeModeOperation>0)?plcCompromised:false,
sensorCompromised=(telemetryTrust<50)?sensorCompromised:false,
resilienceDegradation=(safeModeOperation>0)?resilienceDegradation:((resilienceDegradation>10)?resilienceDegradation-10:0),
mitigationConfidence=min(100, mitigationConfidence + (recoveryCapacity/10)),
safetyMargin=(safeModeOperation>0)?safetyMargin:min(100, safetyMargin+10),
downtime=(downtime>0)?downtime-1:0"""
update_assignment(t573, assign573)

# id574: DR_Harden -> DR_Feedback
t574 = get_transition('id574')
assign574 = """fw_strength=min(10,fw_strength+1),
ids_strength=min(10,ids_strength+1),
waf_strength=min(10,waf_strength+1),
edr_strength=min(10,edr_strength+1),
dlp_strength=min(10,dlp_strength+1),
telemetryIntegrity=(safeModeOperation>0)?telemetryIntegrity:min(100,telemetryIntegrity+10),
controlLoopStability=(failSafeEngaged)?controlLoopStability:min(100,controlLoopStability+10),
actuatorTrust=min(100,actuatorTrust+10),
backupIntegrity=(backupIntegrity<100)?backupIntegrity+5:backupIntegrity"""
update_assignment(t574, assign574)

# id575: DR_Feedback -> DR_Log
t575 = get_transition('id575')
if t575:
    for l in t575.findall('label'):
        if l.attrib.get('kind') == 'assignment':
            l.text = """alertConfidence=(breach)?alertConfidence:0,
plcSuspicion=(breach)?plcSuspicion:0,
scadaSuspicion=(breach)?scadaSuspicion:0,
sensorSuspicion=(breach)?sensorSuspicion:0,
networkThreatConfidence=(breach)?networkThreatConfidence:0,
breachLikelihood=(breach)?breachLikelihood:0,
cpsInstabilityProbability=(safeModeOperation>0)?cpsInstabilityProbability:0,
""" + ",\n".join([line.strip() for line in l.text.split(',\n') if 'Cost' in line])

# id576: DR_Log -> DR_Reset
t576 = get_transition('id576')
if t576:
    for l in t576.findall('label'):
        if l.attrib.get('kind') == 'assignment':
            if 'Cost' in l.text:
                cost_part = ",\n".join([line.strip() for line in l.text.split(',\n') if 'Cost' in line])
                l.text = f"failSafeEngaged=false,\nsafeModeOperation=0,\n{cost_part}"
            else:
                l.text = "failSafeEngaged=false,\nsafeModeOperation=0"

tree.write('../src/human_layer.xml', xml_declaration=True, encoding='utf-8')
print("Successfully applied Phase 8 recovery updates to human_layer.xml")
