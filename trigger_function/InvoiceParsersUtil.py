# Author: Juan Carlos Ruiz
# Company: Google Cloud
# Role: Partner Engineer
# Email: juankruiz@google.com


from typing import Optional

def get_text_or_none(element) -> Optional[str]:
    """Returns the text of the element if it exists, otherwise returns None."""
    return element.text if element is not None else None

def parse_line_count_numeric(root, namespaces) -> Optional[int]:
    """
    Extracts and parses the LineCountNumeric value from the XML.
    Handles potential errors and returns None if the value is invalid or missing.
    """
    try:
        line_count_numeric_text = get_text_or_none(root.find(".//cbc:LineCountNumeric", namespaces=namespaces))
        if line_count_numeric_text is not None:
            return int(line_count_numeric_text)
        else:
            return None
    except ValueError:
        #print(f"Error: Invalid LineCountNumeric value: {line_count_numeric_text}")
        return None