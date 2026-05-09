import xml.etree.ElementTree as ET
import glob

def check_expr(expr):
    if not expr: return []
    errors = []
    if expr.count('(') != expr.count(')'):
        errors.append('Unmatched parentheses')
    if ',,' in expr:
        errors.append('Double comma')
    if expr.strip().endswith(','):
        errors.append('Dangling comma')
    if '?' in expr:
        if ':' not in expr:
            errors.append('Incomplete ternary (missing :)')
    return errors

for f in glob.glob('../src/*.xml'):
    tree = ET.parse(f)
    for elem in tree.findall('.//label'):
        if elem.attrib.get('kind') in ['assignment', 'guard', 'exponentialrate']:
            errs = check_expr(elem.text)
            if errs:
                print(f, elem.attrib['kind'], errs, repr(elem.text))
