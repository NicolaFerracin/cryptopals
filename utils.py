import bitarray
from typing import List
from base64 import b64encode, b64decode
from typing import NamedTuple


# Probably unnecessary but useful while I'm learning
def hex_to_bytes(hex_str: str) -> bytes:
    """Converts hex string to bytes"""
    return bytes.fromhex(hex_str)


# Probably unnecessary but useful while I'm learning
def bytes_to_hex(data: bytes) -> str:
    """Converts bytes to hex string"""
    return data.hex()


def hex_to_base64(hex_str: str) -> str:
    """Encodes hex string to base64"""
    return b64encode(hex_to_bytes(hex_str)).decode()


def from_base64(b64_str: str) -> bytes:
    """Decodes base64 string to bytes"""
    return b64decode(b64_str)


def str_to_bytes(text: str) -> bytes:
    """Convert string to bytes"""
    return text.encode("utf-8")


def bytes_to_str(data: bytes) -> str:
    """Convert bytes to string, replacing invalid characters"""
    return data.decode("utf-8", errors="replace")


def str_to_hex(text: str) -> str:
    """Convert string to hex"""
    return bytes_to_hex(str_to_bytes(text))


# Currently unused
# def hex_to_str(hex_str: str) -> str:
#     """Convert hex to string"""
#     return bytes_to_str(hex_to_bytes(hex_str))


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    XOR two byte sequences.
    If one of the strings is shorter, we repeat it.
    """
    if len(a) < len(b):
        a, b = b, a
    xored = bytearray()
    for index in range(len(a)):
        xored.append(a[index] ^ b[index % len(b)])

    return bytes(xored)


def xor_hex_strings(hex_a: str, hex_b: str) -> str:
    """XOR two hex strings and return hex result"""
    return bytes_to_hex(xor_bytes(hex_to_bytes(hex_a), hex_to_bytes(hex_b)))


def english_score(text: str) -> int:
    """Score how English-like a text is based on character frequency"""
    score = 0
    common_chars = " etaoinshrdlcumwfgypbkjqxz"
    for char in text.lower():
        if char in common_chars:
            score += 1
    return score


class XorResult(NamedTuple):
    score: int
    key: str
    plaintext: str


def find_xor_key(ciphertext: str) -> XorResult:
    """Find the single byte XOR key that produces the most English-like plaintext"""
    # Attempt xoring each ASCII character
    best_score = 0
    best_key = None
    plaintext = None
    for key_byte in range(256):
        key = bytes([key_byte])
        plaintext_bytes = xor_bytes(ciphertext, key)  # xor input against current key
        plaintext = bytes_to_str(plaintext_bytes)
        score = english_score(plaintext)
        if score > best_score:
            best_score = score
            best_key = key_byte
            best_plaintext = plaintext.strip()

    return XorResult(best_score, best_key, best_plaintext)


def read_string_array_file(path: str) -> List[str]:
    "Takes a path to a file containing a list of strings and returns an array of strings"
    with open(path, "r") as f:
        return [line.strip() for line in f]


def read_file(path: str) -> str:
    "Returns the content of the file at path"
    with open(path, "r") as f:
        return f.read().strip()


def hamming_distance(a: str, b: str) -> int:
    """Calculates the Hamming distance between 2 strings.
    The Hamming distance is calculated by xoring the 2 strings and returning the sum of the 1bits
    Example:
    00011010
    10010011
    vvvvvvvv xor
    10001001 => 3
    """
    bytes_a = str_to_bytes(a)
    bytes_b = str_to_bytes(b)
    xored = xor_bytes(bytes_a, bytes_b)
    return sum(bin(byte).count("1") for byte in xored)
