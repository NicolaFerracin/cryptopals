# Detect single-character XOR
# One of the 60-character strings in this file has been encrypted by single-character XOR.
# Find it.

from utils import hex_to_bytes, read_string_array_file, find_xor_key
import re

if __name__ == "__main__":
    print("## Set 1 - Challenge 4")
    expected = "Now that the party is jumping"

    strings = read_string_array_file("set1-challenge4.input")

    for index, string in enumerate(strings):
        result = find_xor_key(hex_to_bytes(string))
        if re.fullmatch(r"[a-zA-Z\s']+", result.plaintext):
            print("✅ Passed" if expected == result.plaintext else "❌ Failed")
            print(f"String {string} at index {index} is encoded with key {result.key}")
            print(f"Output: {result.plaintext}")
