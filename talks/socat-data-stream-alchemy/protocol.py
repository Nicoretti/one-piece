#!/usr/bin/env python3
"""
Binary Message Encoder/Decoder CLI

Protocol Specification:
- Byte 0: Transformation (0x00: None, 0x01: Upper, 0x02: Lower)
- Byte 1: Length (0-255)
- Bytes 2+: String Data (ASCII/UTF-8)
"""

import argparse
import ctypes
import json
import sys


class MessageHeader(ctypes.Structure):
    """Message header: transformation byte + length byte."""

    _fields_ = [
        ("transformation", ctypes.c_ubyte),
        ("length", ctypes.c_ubyte),
    ]


TRANSFORMATIONS = {
    "None": 0x00,
    "Upper": 0x01,
    "Lower": 0x02,
}

TRANSFORMATIONS_REVERSE = {v: k for k, v in TRANSFORMATIONS.items()}
HEADER_SIZE = ctypes.sizeof(MessageHeader)


def decode(binary_data: bytes) -> dict:
    """Decode binary data to dictionary."""
    if len(binary_data) < HEADER_SIZE:
        raise ValueError(f"Binary data too short (min {HEADER_SIZE} bytes)")

    header = MessageHeader.from_buffer_copy(binary_data[:HEADER_SIZE])

    if header.transformation not in TRANSFORMATIONS_REVERSE:
        raise ValueError(f"Unknown transformation: 0x{header.transformation:02x}")

    if len(binary_data) < HEADER_SIZE + header.length:
        raise ValueError(
            f"Binary data incomplete: expected {HEADER_SIZE + header.length} bytes"
        )

    string_data = binary_data[HEADER_SIZE : HEADER_SIZE + header.length].decode("utf-8")
    transformation = TRANSFORMATIONS_REVERSE[header.transformation]

    return {
        "Transformation": transformation,
        "Length": header.length,
        "String": string_data,
    }


def encode(data: dict) -> bytes:
    """Encode dictionary to binary data."""
    transformation = data.get("Transformation", "None")
    string_data = data.get("String", "")

    if transformation not in TRANSFORMATIONS:
        raise ValueError(f"Unknown transformation: {transformation}")

    string_bytes = string_data.encode("utf-8")
    if len(string_bytes) > 255:
        raise ValueError(f"String too long: {len(string_bytes)} bytes (max 255)")

    header = MessageHeader(
        transformation=TRANSFORMATIONS[transformation],
        length=len(string_bytes),
    )

    return bytes(header) + string_bytes


def read_input(source: str, is_binary: bool):
    """Read input from stdin or file."""
    if source == "-":
        file_handle = sys.stdin.buffer if is_binary else sys.stdin
    else:
        file_handle = open(source, "rb" if is_binary else "r")

    try:
        data = file_handle.read()
        return json.loads(data) if not is_binary else data
    finally:
        if source != "-":
            file_handle.close()


def write_output(destination: str, data) -> None:
    """Write output to stdout or file."""
    if destination == "-":
        if isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        elif isinstance(data, dict):
            json.dump(data, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(data)
    else:
        mode = "wb" if isinstance(data, bytes) else "w"
        with open(destination, mode) as f:
            if isinstance(data, bytes):
                f.write(data)
            elif isinstance(data, dict):
                json.dump(data, f, indent=2)
                f.write("\n")
            else:
                f.write(data + "\n")


def cmd_decode(args):
    """Decode binary to JSON."""
    try:
        binary_data = read_input(args.input, is_binary=True)
        assert isinstance(binary_data, bytes)
        result = decode(binary_data)
        write_output(args.output, result)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_encode(args):
    """Encode JSON to binary."""
    try:
        json_data = read_input(args.input, is_binary=False)
        assert isinstance(json_data, dict)
        binary_data = encode(json_data)

        if args.hex:
            hex_output = " ".join(f"0x{byte:02x}" for byte in binary_data)
            write_output(args.output, hex_output)
        else:
            write_output(args.output, binary_data)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Binary Protocol Encoder/Decoder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    decode_parser = subparsers.add_parser("decode", help="Decode binary to JSON")
    decode_parser.add_argument(
        "-i", "--input", default="-", help="Input file (default: stdin)"
    )
    decode_parser.add_argument(
        "-o", "--output", default="-", help="Output file (default: stdout)"
    )
    decode_parser.set_defaults(func=cmd_decode)

    encode_parser = subparsers.add_parser("encode", help="Encode JSON to binary")
    encode_parser.add_argument(
        "-i", "--input", default="-", help="Input file (default: stdin)"
    )
    encode_parser.add_argument(
        "-o", "--output", default="-", help="Output file (default: stdout)"
    )
    encode_parser.add_argument("--hex", action="store_true", help="Output as hex")
    encode_parser.set_defaults(func=cmd_encode)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
