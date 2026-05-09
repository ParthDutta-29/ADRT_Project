import xml.etree.ElementTree as ET
import glob

def clean_expr(text):
    if not text: return text
    # Let's split by comma carefully, but there are function calls min(x,y).
    # Since we know the exact string to remove is 'riskScore+1)' or 'riskScore+2)'
    # we can just use replace.
    text = text.replace(',\nriskScore+1)', '')
    text = text.replace(',riskScore+1)', '')
    text = text.replace('riskScore+1),', '')
    text = text.replace('riskScore+1)\n', '')
    
    text = text.replace(',\nriskScore+2)', '')
    text = text.replace(',riskScore+2)', '')
    text = text.replace('riskScore+2),', '')
    text = text.replace('riskScore+2)\n', '')
    
    return text.strip()

for f in glob.glob('../src/*.xml'):
    tree = ET.parse(f)
    changed = False
    for elem in tree.findall('.//label'):
        if elem.text:
            new_text = clean_expr(elem.text)
            if new_text != elem.text:
                elem.text = new_text
                changed = True
    if changed:
        tree.write(f, xml_declaration=True, encoding='utf-8')
        print('Cleaned', f)
