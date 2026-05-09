import glob
import xml.etree.ElementTree as ET
import re
import sys

def run_audit():
    issues_found = 0
    print("Running Formal Computational Validity Audit...")
    
    for filename in glob.glob('../src/*.xml'):
        try:
            tree = ET.parse(filename)
        except ET.ParseError as e:
            print(f"[FAIL] XML Parser Error in {filename}: {e}")
            issues_found += 1
            continue
            
        for t in tree.getroot().findall('.//transition'):
            t_id = t.attrib.get('id', 'unknown')
            for l in t.findall('label'):
                kind = l.attrib.get('kind')
                text = l.text
                if not text:
                    continue
                    
                if kind == 'assignment':
                    # Check dangling commas
                    if text.strip().endswith(','):
                        print(f"[FAIL] Dangling comma in {filename} (transition {t_id})")
                        issues_found += 1
                    
                    # Check unsafe subtraction
                    for line in text.split(','):
                        line = line.strip()
                        if '-' in line and '?' not in line and '=' in line and 'min(' not in line and 'max(' not in line:
                            # Exception for standard safe logic
                            if '100-' not in line and 'MAX_COST' not in line:
                                print(f"[WARN] Unsafe dynamic subtraction in {filename} (transition {t_id}): {line}")
                                issues_found += 1
                                
                        # Check unsafe addition
                        if '+' in line and 'min(' not in line and 'MAX_COST' not in line and '?' not in line and '=' in line and '/2' not in line:
                            print(f"[WARN] Unsafe linear accumulation in {filename} (transition {t_id}): {line}")
                            issues_found += 1
                            
                elif kind == 'probability':
                    # Check invalid branch weights
                    if '-' in text or '*' in text:
                        print(f"[FAIL] Invalid branch weight logic in {filename} (transition {t_id}): {text}")
                        issues_found += 1
                        
    if issues_found == 0:
        print("[OK] Bounded-State Safety Audit Passed. 0 issues found.")
    else:
        print(f"[ERROR] {issues_found} issues found during formal audit.")

if __name__ == '__main__':
    run_audit()
