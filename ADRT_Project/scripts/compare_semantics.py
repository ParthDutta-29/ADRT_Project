import xml.etree.ElementTree as ET
import os

old_model_path = '../../ADRT.xml'
new_model_path = '../build/main_system.xml'

def extract_metrics(tree):
    metrics = {
        'templates': 0,
        'locations': 0,
        'transitions': 0,
        'clocks': 0
    }
    
    root = tree.getroot()
    metrics['templates'] = len(root.findall('template'))
    
    for t in root.findall('template'):
        metrics['locations'] += len(t.findall('location'))
        metrics['transitions'] += len(t.findall('transition'))
        
    decl = root.find('declaration').text or ""
    metrics['clocks'] = decl.count('clock ')
    return metrics

if __name__ == "__main__":
    if not os.path.exists(old_model_path) or not os.path.exists(new_model_path):
        print("Missing files for comparison.")
        exit(1)
        
    old_tree = ET.parse(old_model_path)
    new_tree = ET.parse(new_model_path)
    
    old_m = extract_metrics(old_tree)
    new_m = extract_metrics(new_tree)
    
    print("=== Structural Preservation Analysis ===")
    print(f"{'Metric':<15} | {'Original (ADRT.xml)':<20} | {'Modular (main_system.xml)':<20}")
    print("-" * 60)
    for k in old_m.keys():
        print(f"{k:<15} | {old_m[k]:<20} | {new_m[k]:<20}")
    
    print("\nConclusion:")
    if old_m == new_m:
        print("SUCCESS: Cardinality-preserving decomposition verified. The counts of templates, locations, transitions, and clocks match.")
    else:
        print("WARNING: Divergence detected in structural cardinality.")
