from typing import List
from base64 import b64encode
from typing import NamedTuple


def hex_to_bytes(str: str) -> bytes:
    "Turns a hex string string to a list of bytes"
    return bytes.fromhex(str)


def hex_bytes_to_base64(hex_bytes: bytes) -> str:
    "Encodes the byte representation of a hex string to base64"
    return b64encode(hex_bytes).decode()


def xor_hex_strings(a: str, b: str) -> str:
    """
    Takes 2 hex strings and xor each of their bytes. Returns a new hex string.
    If one of the strings is shorter, we use % to wrap around it and keep xoring all the bytes in the longer string
    """
    bytesA = hex_to_bytes(
        a if len(a) > len(b) else b
    )  # This is always going to be longer in case they have different length
    bytesB = hex_to_bytes(b if len(b) < len(a) else a)

    xored = bytearray()
    for index in range(len(bytesA)):
        xored.append(bytesA[index] ^ bytesB[index % len(bytesB)])

    return xored.hex()


def english_string_score(string: str) -> int:
    string_score = 0
    freq = [" ", "e", "t", "a", "o", "i", "n", "s", "h", "r", "d", "l", "u"]
    for letter in string:
        if letter in freq:
            string_score += 1
    return string_score


class XorResult(NamedTuple):
    score: int
    key: str
    plaintext: str


def find_xor_key(input: str) -> XorResult:
    """Takes an input string and finds the single hex character that xored to the input, results in plaintext English"""
    # Attempt xoring each ASCII character
    best_score = 0
    result_key = None
    result_string = None
    for x in range(0x00, 0xFF):
        key = format(x, "02x")  # Removing the 0x prefix so that the utils function work
        output = xor_hex_strings(input, key)  # xor input against current key
        human_readable_output = hex_to_bytes(output).decode(
            "utf-8", errors="replace"
        )  # make human readable - ignore errors as we are going to have broken strings
        # find out how close to english this string is
        score = english_string_score(human_readable_output)
        if score > best_score:
            best_score = score
            result_key = key
            result_string = human_readable_output

    return XorResult(best_score, result_key, result_string)


def read_string_array_file(path: str) -> List[str]:
    "Takes a path to a file containing a list of strings and returns an array of strings"
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
        return lines


def str_to_hex(str: str) -> str:
    "Takes a plaintext string and encodes it to hex"
    return str.encode("utf-8").hex()
