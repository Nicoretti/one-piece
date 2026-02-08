#!/usr/bin/env python3
"""
JSON Generator Tool for Binary Message Encoder

This tool generates JSON input suitable for encode.py.
Outputs JSON to stdout.
"""

import argparse
import json
import sys


VALID_TRANSFORMATIONS = ["None", "Upper", "Lower"]


def generate_json(transformation, string_data):
    """Generate JSON for the encoder."""
    if transformation not in VALID_TRANSFORMATIONS:
        print(f"Error: Invalid transformation. Must be one of {VALID_TRANSFORMATIONS}", file=sys.stderr)
        sys.exit(1)
        
    # Check the length of the encoded byte string to ensure protocol compliance
    string_bytes = string_data.encode("utf-8")
    byte_length = len(string_bytes)
    if byte_length > 255:
        print(f"Error: String too long: {byte_length} bytes. Must be 255 bytes or less when encoded as UTF-8.", file=sys.stderr)
        sys.exit(1)
        
    return {
        "Transformation": transformation,
        "String": string_data
    }


def main():
    parser = argparse.ArgumentParser(description="Generate JSON for Binary Protocol Encoder")
    parser.add_argument(
        "-t", "--transformation", 
        default="None",
        choices=VALID_TRANSFORMATIONS,
        help="Transformation to apply (None, Upper, or Lower)"
    )
    parser.add_argument(
        "string",
        help="String data to encode (max 255 bytes when UTF-8 encoded)"
    )
    
    args = parser.parse_args()
    
    try:
        json_data = generate_json(args.transformation, args.string)
        json.dump(json_data, sys.stdout)
        print()  # Add newline
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()