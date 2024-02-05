import xml.etree.ElementTree as ET

def create_kml(new_coordinates,nombre,name_kml):
    tree = ET.parse(r"/home/chiky/Projects/Polydect/Tools/format.kml")
    root = tree.getroot()

    document_name = root.find(".//kml:Document/kml:name", namespaces={"kml": "http://www.opengis.net/kml/2.2"})
    document_name.text = f'{nombre}.kml'

    placemark_name = root.find(".//kml:Placemark/kml:name", namespaces={"kml": "http://www.opengis.net/kml/2.2"})
    placemark_name.text = f'{nombre}'

    coordinates_elem = root.find(".//{http://www.opengis.net/kml/2.2}coordinates")
    #new_coordinates = "-77.05,-12.03,0"
    coordinates_elem.text = new_coordinates

    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

    tree.write(f'Output/{name_kml}/{nombre}.kml',encoding='utf-8',xml_declaration=True)
