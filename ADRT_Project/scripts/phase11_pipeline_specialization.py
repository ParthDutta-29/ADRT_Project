import os
import glob

# Mapping for wholesale string replacement across the framework
replacements = {
    # Attack Templates & Instances
    "Network_Attack": "SCADA_Compromise",
    "NA_": "SCADA_",
    "Web_Attack": "Sensor_Spoofing",
    "WA_": "SENS_",
    "API_Attack": "Flow_Falsification",
    "AA_": "FLOW_",
    "Malware_Attack": "PLC_Logic_Manipulation",
    "MAL_": "PLC_",
    "Ransomware_Attack": "Control_Center_Ransomware",
    "RAN_": "CRAN_",
    "Phishing_Attack": "Compressor_Intrusion",
    "PHI_": "COMP_",
    "Credential_Attack": "Remote_RTU_Compromise",
    "CRE_": "RTU_",
    "Insider_Threat": "Malicious_Valve_Actuation",
    "INS_": "VALVE_",
    "Supply_Chain_Attack": "Telemetry_Delay_Attack",
    "SUP_": "TDELAY_",
    "Firmware_Attack": "Supervisory_Stealth_Persistence",
    "FWA_": "STEALTH_",

    # Defense Templates
    "Firewall_Defense": "SCADA_Firewall",
    "IDS_Defense": "Telemetry_Validator",
    "WAF_Defense": "Protocol_Analyzer",
    "EDR_Defense": "RTU_Endpoint_Defense",
    "DLP_Defense": "Flow_Sanity_Checker",

    # Recovery
    "Defender_Response": "Pipeline_Incident_Response",
    "DR_": "PIR_",
    
    # Environment
    "Environment": "Pipeline_Physical_Dynamics",
    "Env_": "Pipe_",

    # Human / Network
    "Human_Layer": "Supervisory_Control",
    "Network_Layer": "Pipeline_Network_Routing"
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    for old, new in replacements.items():
        # Ensure we don't accidentally replace subsets (e.g. NA_ inside something else)
        # But our prefixes are quite unique. We will do direct replace.
        content = content.replace(old, new)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    files_to_process = []
    files_to_process.extend(glob.glob('../src/*.xml'))
    files_to_process.extend(glob.glob('../validation/*.q'))
    files_to_process.extend(glob.glob('../config/*.json'))
    
    # Exclude global_defs just in case, but actually global_defs has constants. We might need to replace there too.
    for f in files_to_process:
        process_file(f)

if __name__ == '__main__':
    main()
