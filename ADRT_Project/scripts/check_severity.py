import xml.etree.ElementTree as ET
tree = ET.parse('../src/human_layer.xml')
for trans in tree.findall('.//transition'):
    g = trans.find('label[@kind="guard"]')
    if g is not None and 'severity' in g.text:
        print('Severity used in guard:', g.text)
    a = trans.find('label[@kind="assignment"]')
    if a is not None and 'severity' in a.text:
        print('Severity used in assignment:', a.text)
