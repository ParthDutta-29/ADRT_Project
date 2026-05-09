import xml.etree.ElementTree as ET
import os

src_file = 'c:/Users/parth/Documents/RP/ADRT.xml'
dst_file = 'c:/Users/parth/Documents/RP/ADRT_Project/src/global_defs.xml'

tree = ET.parse(src_file)
decl = tree.getroot().find('declaration')
with open(dst_file, 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write(ET.tostring(decl, encoding='unicode'))
