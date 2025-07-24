# Single-byte XOR cipher
# The hex encoded string:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.
# You can do this by hand. But don't: write code to do it for you.
# How? Devise some method for "scoring" a piece of English plaintext.
# Character frequency is a good metric. Evaluate each output and choose the one with the best score.

from utils import find_xor_key

if __name__ == "__main__":
    print("## Set 1 - Challenge 3")
    input = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    # To revert a XOR we apply XOR again.
    # We need to find the character that xored to the input, produces plaintext English
    [key, output] = find_xor_key(input)

    print("✅ Passed")
    print(f"Key: {key} - Output: {output}")
