# Break repeating-key XOR
# It is officially on, now.
# This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.
# There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.
# Here's how:
#     1. Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
#     2. Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
#     `this is a test`
#     and
#     `wokka wokka!!!`
#     is 37. Make sure your code agrees before you proceed.
#     3. For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
#     4. The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
#     5. Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
#     6. Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
#     7. Solve each block as if it was single-character XOR. You already have code to do this.
#     8. For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
# This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.
# No, that's not a mistake.

# We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.

from itertools import combinations
import statistics
from utils import (
    bytes_to_str,
    find_xor_key,
    from_base64,
    hamming_distance,
    read_file,
    xor_bytes,
)

if __name__ == "__main__":
    print("## Set 1 - Challenge 6")

    # There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
    input = from_base64(read_file("./set1-challenge6.input"))

    # 1. Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
    min_dist = float("inf")
    keysize = 0
    for curr_keysize in range(2, 40):
        # 3. For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.

        # We start by taking the first 4 blocks of size KEYSIZE
        # We then combine them into 6 distinct pairs
        # We then check the hamming_distance for each pair
        # Find the mean of distance and divide by KEYSIZE for normalizing the values
        blocks = []
        for times in range(0, 4):
            blocks.append(
                input[curr_keysize * times : curr_keysize * (times + 1)].decode()
            )
        pairs = combinations(blocks, 2)
        dist = (
            statistics.mean([hamming_distance(a, b) for (a, b) in pairs]) / curr_keysize
        )

        # 4. The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
        if dist < min_dist:
            min_dist = dist
            keysize = curr_keysize

    # 5. Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
    blocks = [input[i : i + keysize] for i in range(0, len(input), keysize)]

    # 6. Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
    transposed_blocks = [bytearray() for _ in range(keysize)]
    for block in blocks:
        for i, byte in enumerate(block):
            transposed_blocks[i].append(byte)

    # 7. Solve each block as if it was single-character XOR. You already have code to do this.
    key_bytes = []
    for transposed_block in transposed_blocks:
        # 8. For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
        result = find_xor_key(bytes(transposed_block))
        key_bytes.append(result.key)

    key = bytes(key_bytes)
    plaintext = bytes_to_str(xor_bytes(input, key))
    expected_first_100_chars = "I'm back and I'm ringin' the bell \nA rockin' on the mike while the fly girls yell \nIn ecstasy in the"

    print("✅ Passed" if expected_first_100_chars == plaintext[0:100] else "❌ Failed")
    print(f"Keysize: {keysize} - Key: {bytes_to_str(key)}")
    print("Result Excerpt:")
    print(plaintext[0:200], "...")
