from base64 import b64encode

def hex_to_bytes(str: str) -> bytes:
    "Turns a hex string string to a list of bytes"
    return bytes.fromhex(str)

def hex_bytes_to_base64(hex_bytes: bytes) -> str:
    "Encodes the byte representation of a hex string to base64"
    return b64encode(hex_bytes).decode()

def xor_hex_strings(a: str, b: str) -> str:
    "Takes 2 hex strings and xor each of their bytes. Returns a new hex string"
    bytesA = bytes.fromhex(a)
    bytesB = bytes.fromhex(b)
    xored = bytes([x ^ y for x, y in zip(bytesA, bytesB)])
    return xored.hex()