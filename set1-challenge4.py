# Detect single-character XOR
# One of the 60-character strings in this file has been encrypted by single-character XOR.
# Find it.

from utils import read_string_array_file, find_xor_key

if __name__ == "__main__":
    print("## Set 1 - Challenge 4")

    strings = read_string_array_file("set1-challenge4.input")

    for index, string in enumerate(strings):
        result = find_xor_key(string)
        if (result is not None):
            print("✅ Passed")
            print(f"String {string} at index {index} is encoded with key {result[0]}")
            print(f"Output: {result[1]}")