import xml.etree.ElementTree as ET
import json
import re
import argparse

def extract_svg_data(svg_text):
    root = ET.fromstring(svg_text)
    
    def extract_numbers(s):
        return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", s)]
    
    def process_element(element):
        data = {}
        if 'fill' in element.attrib:
            data['fill'] = element.attrib['fill']
        if 'stroke' in element.attrib:
            data['stroke'] = element.attrib['stroke']
        
        if element.tag.endswith('rect'):
            data['type'] = 'rect'
            data['x'] = float(element.attrib['x'])
            data['y'] = float(element.attrib['y'])
            data['width'] = float(element.attrib['width'])
            data['height'] = float(element.attrib['height'])
        elif element.tag.endswith('circle'):
            data['type'] = 'circle'
            data['cx'] = float(element.attrib['cx'])
            data['cy'] = float(element.attrib['cy'])
            data['r'] = float(element.attrib['r'])
        elif element.tag.endswith('path'):
            data['type'] = 'path'
            path_data = element.attrib['d']
            commands = re.findall(r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)', path_data)
            data['commands'] = []
            for cmd, params in commands:
                params = extract_numbers(params)
                data['commands'].append({'command': cmd, 'params': params})
        elif element.tag.endswith('linearGradient') or element.tag.endswith('radialGradient'):
            data['type'] = 'gradient'
            data['id'] = element.attrib['id']
            data['stops'] = []
            for stop in element.findall('{http://www.w3.org/2000/svg}stop'):
                data['stops'].append({
                    'offset': stop.attrib['offset'],
                    'color': stop.attrib.get('stop-color', '')
                })
        
        return data
    
    svg_data = {
        'shapes': [],
        'gradients': []
    }
    
    for elem in root.iter():
        if elem.tag.endswith(('rect', 'circle', 'path')):
            svg_data['shapes'].append(process_element(elem))
        elif elem.tag.endswith(('linearGradient', 'radialGradient')):
            svg_data['gradients'].append(process_element(elem))
    
    return json.dumps(svg_data, indent=2)

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", type=str, required=True)
args = ap.parse_args()

with open(args.file, "r") as f:
    svg_text = f.read()

res = extract_svg_data(svg_text)
print(res)
