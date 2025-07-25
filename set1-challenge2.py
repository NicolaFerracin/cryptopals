# Fixed XOR
# Write a function that takes two equal-length buffers and produces their XOR combination.
# If your function works properly, then when you feed it the string:
# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:
# 686974207468652062756c6c277320657965
# ... should produce:
# 746865206b696420646f6e277420706c6179

from utils import xor_hex_strings

if __name__ == "__main__":
    print("## Set 1 - Challenge 2")
    a = "1c0111001f010100061a024b53535009181c"
    b = "686974207468652062756c6c277320657965"
    expected = "746865206b696420646f6e277420706c6179"
    
    output = xor_hex_strings(a, b)
    
    print("✅ Passed" if expected == output else "❌ Failed")
    print(f"Input: {a} {b}")
    print(f"Output: {output}")
