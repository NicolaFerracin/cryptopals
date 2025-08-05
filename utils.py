import bitarray
from typing import List
from base64 import b64encode, b64decode
from typing import NamedTuple


def hex_to_bytes(str: str) -> bytes:
    "Turns a hex string string to a list of bytes"
    return bytes.fromhex(str)


def hex_bytes_to_base64(hex_bytes: bytes) -> str:
    "Encodes the byte representation of a hex string to base64"
    return b64encode(hex_bytes).decode()


def from_base64(str: str) -> bytes:
    "Decodes a base64-encrypted string into its bytes representation"
    return b64decode(str)


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


def read_file(path: str) -> str:
    "Returns the content of the file at path"
    file = open(path, "r")
    content = file.read()
    file.close()
    return content


def str_to_hex(str: str) -> str:
    "Takes a plaintext string and encodes it to hex"
    return str.encode("utf-8").hex()


def hex_to_str(str: str) -> str:
    "Takes a hex string and decodes it to a plaintext string"
    return hex_to_bytes(str).decode("utf-8", errors="replace").encode("utf-8")


def str_to_bytes(str: str) -> bytes:
    "Turns a plaintext string into its bytes representation"
    return str.encode()


def hamming_distance(a: str, b: str) -> int:
    """Calculates the Hamming distance between 2 strings.
    The Hamming distance is calculated by xoring the 2 strings and returning the sum of the 1bits
    Example:
    00011010
    10010011
    vvvvvvvv xor
    10001001 => 3
    """
    xored = hex_to_str(xor_hex_strings(str_to_hex(a), str_to_hex(b)))
    ba = bitarray.bitarray()
    ba.frombytes(xored)  # turns the string into a list of 0|1 bits
    return sum(ba.tolist())  # the Hamming distance is the xored
