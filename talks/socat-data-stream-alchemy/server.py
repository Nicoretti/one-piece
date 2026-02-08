#!/usr/bin/env python3
"""
Simple protocol server: reads JSON request, applies transformation, responds with result.
Assumes stdin/stdout for I/O.
"""

import json
import sys


def parse_message(json_data: dict) -> dict:
    """Parse JSON message to extract transformation and data."""
    transformation = json_data.get("Transformation", "None").lower()
    string_data = json_data.get("String", "")
    
    if transformation not in ["none", "upper", "lower"]:
        raise ValueError(f"Unknown transformation: {transformation}")
    
    return {
        "transformation": transformation,
        "data": string_data,
    }


def apply_transformation(text: str, transformation: str) -> str:
    """Apply transformation to text."""
    if transformation == "upper":
        return text.upper()
    elif transformation == "lower":
        return text.lower()
    return text


def format_response(text: str) -> dict:
    """Format response message as JSON."""
    return {
        "Transformation": "None",
        "String": text
    }


def main():
    try:
        json_request = json.load(sys.stdin)
        request = parse_message(json_request)

        result = apply_transformation(request["data"], request["transformation"])

        response = format_response(result)
        json.dump(response, sys.stdout)
        print()  # Add newline
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
