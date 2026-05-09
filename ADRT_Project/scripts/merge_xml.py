import os
import re
import sys
import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET

src_dir = '../src'
build_dir = '../build'

def build_queries(query_files):
    query_xml = "<queries>\n"
    for qfile in query_files:
        qpath = os.path.join('../validation', qfile)
        if os.path.exists(qpath):
            with open(qpath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('/*') and not line.startswith('*') and not line.startswith('*/'):
                        query_xml += f"    <query>\n        <formula>{saxutils.escape(line)}</formula>\n        <comment>Imported from {qfile}</comment>\n    </query>\n"
    query_xml += "</queries>\n"
    return query_xml

def build_modular():
    print("Building modular architecture: build/main_system.xml")
    with open(os.path.join(src_dir, 'global_defs.xml'), 'r', encoding='utf-8') as f:
        global_content = f.read()
        match = re.search(r'<declaration>(.*?)</declaration>', global_content, re.DOTALL)
        global_decl = match.group(1) if match else ''

    layers = [
        'physical_layer.xml', 'network_layer.xml', 'attack_layer.xml',
        'defense_layer.xml', 'human_layer.xml', 'recovery_layer.xml',
        'strategy_layer.xml'
    ]

    templates_text = ""
    for layer in layers:
        layer_path = os.path.join(src_dir, layer)
        if os.path.exists(layer_path):
            with open(layer_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r'(<template>.*?</template>)', content, re.DOTALL)
                for m in matches:
                    templates_text += m + "\n"

    sys_comp_path = os.path.join(src_dir, 'system_composition.xml')
    if os.path.exists(sys_comp_path):
        with open(sys_comp_path, 'r', encoding='utf-8') as f:
            sys_content = f.read()
            match = re.search(r'<system>(.*?)</system>', sys_content, re.DOTALL)
            system_text = match.group(1) if match else "system Environment;"
    else:
        system_text = "system Environment;"

    queries_text = build_queries(['modular_queries.q', 'scalability_tests.q'])

    with open(os.path.join(build_dir, 'main_system.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<!DOCTYPE nta PUBLIC "-//Uppaal Team//DTD Flat System 1.6//EN" "http://www.it.uu.se/research/group/darts/uppaal/flat-1_6.dtd">\n')
        f.write('<nta>\n')
        f.write('  <declaration>' + global_decl + '</declaration>\n')
        f.write(templates_text)
        f.write('  <system>\n' + system_text + '\n  </system>\n')
        f.write(queries_text)
        f.write('</nta>\n')
    print("SUCCESS: Generated build/main_system.xml")

def build_baseline():
    print("Building baseline architecture: build/baseline_system.xml")
    original_adrt = '../../ADRT.xml'
    if not os.path.exists(original_adrt):
        print(f"ERROR: Cannot find original monolithic file at {original_adrt}")
        return
        
    with open(original_adrt, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Strip any existing queries
    content = re.sub(r'<queries>.*?</queries>', '', content, flags=re.DOTALL)
    
    # Inject baseline queries just before </nta>
    queries_text = build_queries(['baseline_queries.q'])
    content = content.replace('</nta>', queries_text + '\n</nta>')
    
    with open(os.path.join(build_dir, 'baseline_system.xml'), 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Generated build/baseline_system.xml")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if '--baseline' in sys.argv:
            build_baseline()
        elif '--modular' in sys.argv:
            build_modular()
        else:
            print("Unknown argument. Use --baseline or --modular")
    else:
        # Default behavior: build both
        build_baseline()
        build_modular()
