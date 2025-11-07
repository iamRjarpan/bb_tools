#!/usr/bin/env python3

import argparse
import base64
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import string
import sys

def parse_and_extract(xml_file: Path):
    """
    Parses a Burp Suite XML export file to find, decode, and return unique Base64 encoded strings.

    Args:
        xml_file: The path to the XML file.

    Returns:
        A set of unique, decoded strings.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError):
        return set()

    decoded_strings = set()
    # This regex finds potential Base64 strings: quoted, and at least 20 chars long.
    base64_pattern = re.compile(b'"([A-Za-z0-9+/=]{20,})"')

    for item in root.findall('item'):
        for element_tag in ['request', 'response']:
            element = item.find(element_tag)
            if element is None or element.text is None:
                continue

            content_bytes = b''
            # Check if the content is marked as Base64 encoded
            if element.attrib.get('base64') == 'true':
                try:
                    content_bytes = base64.b64decode(element.text)
                except Exception:
                    continue # Skip if the body is not valid Base64
            else:
                # If not, it's plain text. Encode it to bytes for regex matching.
                content_bytes = element.text.encode('utf-8', 'ignore')

            # Find all potential Base64 strings within the content
            matches = base64_pattern.findall(content_bytes)
            for match in matches:
                try:
                    # The matched string is a candidate. Let's try to decode it.
                    # It might need padding.
                    padded_match = match + b'=' * (-len(match) % 4)
                    decoded_str = base64.b64decode(padded_match).decode('utf-8', 'ignore')
                    
                    # Add any non-empty, printable string to the results.
                    if decoded_str.strip() and all(c in string.printable for c in decoded_str.strip()):
                        decoded_strings.add(decoded_str.strip())
                except Exception:
                    # This is expected if a matched string is not valid Base64
                    continue

    return decoded_strings

def main():
    """Main function to handle argument parsing and orchestrate the extraction."""
    parser = argparse.ArgumentParser(
        description="Burp Base64 Extractor",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""Example usage:
  python {Path(__file__).name} burp_export.xml
"""
    )
    parser.add_argument("file", help="Path to the Burp Suite XML export file.")
    
    args = parser.parse_args()

    xml_file_path = Path(args.file)

    decoded_strings = parse_and_extract(xml_file_path)

    if not decoded_strings:
        return

    # Sort the unique strings for clean output
    sorted_strings = sorted(list(decoded_strings))

    for s in sorted_strings:
        print(s)

if __name__ == "__main__":
    main()
