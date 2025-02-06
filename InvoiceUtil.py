# Author: Juan Carlos Ruiz
# Company: Google Cloud
# Role: Partner Engineer
# Email: juankruiz@google.com

import xml.etree.ElementTree as ET
from typing import List, Optional

def extract_cdata(xml_string: str) -> List[Optional[str]]:
    """
    Extracts CDATA blocks from an XML string and returns them as a list of strings.
    Returns None for CDATA blocks that are empty.
    """
    root = ET.fromstring(xml_string)
    cdata_elements = root.findall(".//cbc:Description", namespaces={"cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"})
    cdata_blocks = [cdata_element.text if cdata_element.text else None for cdata_element in cdata_elements]
    return cdata_blocks

def read_xml_file(filename: str) -> str:
    """
    Reads the content of an XML file and returns it as a string.
    """
    with open(filename, 'r') as f:
        xml_string = f.read()
    return xml_string