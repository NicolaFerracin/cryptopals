from base64 import b64encode

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
    bytesA = hex_to_bytes(a if len(a) > len(b) else b) # This is always going to be longer in case they have different length
    bytesB = hex_to_bytes(b if len(b) < len(a) else a)
    
    xored = bytearray()
    for index, value in enumerate(bytesA):
        xored.append(bytesA[index] ^ bytesB[index % len(bytesB)])

    return xored.hex()

def find_xor_key(input: str) -> str:
    """Takes an input string and finds the single hex character that xored to the input, results in plaintext English"""
    # Attempt xoring each ASCII character
    for x in range(0x00, 0xFF):
        key = format(x, '02x') # Removing the 0x prefix so that the utils function work
        output = xor_hex_strings(input, key) # xor input against current key
        human_readable_output = (hex_to_bytes(output).decode('utf-8', errors="replace")) # make human readable - ignore errors as we are going to have broken strings
        # is it plaintext English?
        if (re.fullmatch(r"[a-zA-Z\s']+", human_readable_output)):
            return [key, human_readable_output]

