import xml.etree.ElementTree as ET
import glob
import os
import re

src_dir = '../src'
global_defs = os.path.join(src_dir, 'global_defs.xml')

def extract_identifiers_from_decl(text):
    if not text:
        return set()
    # Remove comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'//.*', '', text)
    
    identifiers = set()
    
    # Match variables: type [bounds] var1, var2;
    # e.g. int[0,100] fwQueueSize = 0;
    # bool breach = false;
    # clock x;
    # broadcast chan a, b;
    
    statements = [s.strip() for s in text.split(';') if s.strip()]
    for stmt in statements:
        # Ignore const, typedefs, functions for simple parsing (approx)
        if stmt.startswith('typedef') or stmt.startswith('void ') or '{' in stmt:
            # crude function extraction
            m = re.match(r'[\w\[\]\,]+\s+(\w+)\s*\(', stmt)
            if m:
                identifiers.add(m.group(1))
            continue
            
        # Strip prefixes
        stmt = stmt.replace('broadcast ', '').replace('urgent ', '').replace('const ', '')
        
        # Split by type and variable list
        parts = stmt.split()
        if len(parts) >= 2:
            # type is parts[0], rest is var list
            var_list = " ".join(parts[1:])
            # remove assignments
            var_list = re.sub(r'=.*?(,|$)', r'\1', var_list)
            for v in var_list.split(','):
                var_name = v.strip().split()[0] if v.strip() else ""
                var_name = re.sub(r'\[.*\]', '', var_name)
                if var_name:
                    identifiers.add(var_name)
    return identifiers

def get_used_identifiers(tree):
    used = set()
    for label in tree.getroot().findall('.//label'):
        if label.text:
            # Find words that look like identifiers
            words = re.findall(r'[a-zA-Z_]\w*', label.text)
            used.update(words)
    return used

if __name__ == "__main__":
    global_tree = ET.parse(global_defs)
    global_text = global_tree.getroot().text or ""
    declared = extract_identifiers_from_decl(global_text)
    
    # Add UPPAAL built-ins
    declared.update(['true', 'false', 'min', 'max'])
    
    files = glob.glob(os.path.join(src_dir, '*.xml'))
    files.remove(global_defs)
    
    all_pass = True
    
    for f in files:
        if 'system_composition.xml' in f: continue
        tree = ET.parse(f)
        
        # Add local declarations
        local_decl = tree.find('.//declaration')
        local_text = local_decl.text if local_decl is not None else ""
        local_declared = extract_identifiers_from_decl(local_text)
        
        valid_symbols = declared.union(local_declared)
        used = get_used_identifiers(tree)
        
        undeclared = used - valid_symbols
        if undeclared:
            print(f"[{os.path.basename(f)}] WARNING: Potentially undeclared identifiers: {undeclared}")
            all_pass = False
            
    if all_pass:
        print("SUCCESS: All identifiers resolve correctly.")
    else:
        print("FAIL: Found undefined identifiers.")
