import glob, xml.etree.ElementTree as ET, re

def audit_and_repair():
    repairs = []
    
    for filename in glob.glob('../src/*.xml'):
        tree = ET.parse(filename)
        changed = False
        root = tree.getroot()
        for t in root.findall('.//transition'):
            trans_id = t.attrib.get('id')
            for l in t.findall('label'):
                if l.attrib.get('kind') == 'assignment' and l.text:
                    lines = l.text.split(',')
                    new_lines = []
                    for idx, line in enumerate(lines):
                        line_changed = False
                        orig_line = line.strip()
                        
                        if not orig_line:
                            if idx < len(lines) - 1:
                                new_lines.append(line)
                            continue

                        # Check for overflow: x=x+N without min(
                        match_plus = re.search(r'([a-zA-Z0-9_]+)\s*=\s*\1\s*\+\s*([a-zA-Z0-9_]+|[0-9]+)', orig_line)
                        if match_plus and 'min(' not in orig_line and 'MAX_COST' not in orig_line and 'downtime' not in orig_line and 'or_hits' not in orig_line and 'or2_hits' not in orig_line and 'vg_count' not in orig_line:
                            if '?' not in orig_line:
                                var = match_plus.group(1)
                                added = match_plus.group(2)
                                new_line = orig_line.replace(f'{var}={var}+{added}', f'{var}=min(100, {var}+{added})')
                                new_lines.append(new_line)
                                repairs.append((filename, trans_id, orig_line, new_line, 'OVERFLOW_REPAIR', f'Prevented {var} from exceeding bounded int[0,100].'))
                                line_changed = True
                                changed = True
                        
                        # Check for underflow: x=x-N without ternary ?
                        match_minus = re.search(r'([a-zA-Z0-9_]+)\s*=\s*\1\s*-\s*([a-zA-Z0-9_]+|[0-9]+)', orig_line)
                        if match_minus and '?' not in orig_line:
                            var = match_minus.group(1)
                            sub = match_minus.group(2)
                            new_line = orig_line.replace(f'{var}={var}-{sub}', f'{var}=({var}>={sub})?{var}-{sub}:0')
                            new_lines.append(new_line)
                            repairs.append((filename, trans_id, orig_line, new_line, 'UNDERFLOW_REPAIR', f'Prevented {var} from becoming negative.'))
                            line_changed = True
                            changed = True
                            
                        # Missing cases?
                        
                        if not line_changed:
                            new_lines.append(line)
                    
                    if changed:
                        l.text = ','.join(new_lines)
                        
                elif l.attrib.get('kind') == 'probability' and l.text:
                    orig_line = l.text.strip()
                    # Check for probability semantic errors
                    if '+' in orig_line and '1 +' not in orig_line and '/' not in orig_line:
                        parts = orig_line.split('+')
                        if len(parts) == 2:
                            p1 = parts[0].strip()
                            p2 = parts[1].strip()
                            new_line = f'1 + {p1}/20 + {p2}/25'
                            l.text = new_line
                            repairs.append((filename, trans_id, orig_line, new_line, 'PROBABILITY_NORMALIZATION', 'Converted unsafe additive probability into bounded UPPAAL weight.'))
                            changed = True
                            
        if changed:
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            print(f'Wrote {filename}')
            
    with open('repairs.log', 'w') as f:
        for r in repairs:
            f.write(f'{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}|{r[5]}\n')
            
audit_and_repair()
