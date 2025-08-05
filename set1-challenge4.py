# Detect single-character XOR
# One of the 60-character strings in this file has been encrypted by single-character XOR.
# Find it.

from utils import read_string_array_file, find_xor_key
import re

if __name__ == "__main__":
    print("## Set 1 - Challenge 4")

    strings = read_string_array_file("set1-challenge4.input")

    for index, string in enumerate(strings):
        [score, key, result] = find_xor_key(string)
        if re.fullmatch(r"[a-zA-Z\s']+", result):
            print("✅ Passed")
            print(f"String {string} at index {index} is encoded with key {key}")
            print(f"Output: {result}")
