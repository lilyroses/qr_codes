# encode.py
from string import digits


# STEP 1: DETERMINE ENCODING SCHEME
def get_encoding_scheme(msg):
    """
    Determine appropriate encoding scheme for the message, so that the fewest
    number of bits are used. If the message contains only numbers, use NUMERIC
    encoding. If the message uses numbers, capital letters, and a few select 
    symbols (see ALPHANUM tuple above), use ALPHANUMERIC encoding. Otherwise,
    use BYTE encoding. (KANJI mode, although part of the QR code specification,
    is not implemented in this software.)
    """
    msg_chars = set(msg)
    a = msg_chars & set(NUM)
    if len(a) == len(msg_chars):
        return "NUM"
    b = msg_chars & set(ALPHANUM)
    if len(b) == len(msg_chars):
        return "ALPHANUM"
    return "BYTE"



# STEP 2: DETERMINE ERROR CORRECTION LEVEL
def 


def encode_numeric(msg):
    """Split numeric msg into chunks of 3 numbers each. The last chunk of
    numbers may be only 1 or 2 digits long. If a chunk has one leading zero,
    it is considered a 2 digit long chunk. If a chunk has 2 leading zeroes, it
    is a 1 digit long chunk.
    Convert a 3 digit chunk to a 10 digit binary number. Convert a 2 digit
    chunk to a 7-bit binary number. Convert a 1 digit chunk to a 4 digit
    binary number.

    A chunk of only zeroes is a non-binary digit? TODO!
    """
    MODE_INDICATOR = "001"
    chunk_size = 3  
    msg_chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]
    binary_digits = [bin(int(chunk)) for chunk in msg_chunks]
    encoded_msg = MODE_INDICATOR + "".join(binary_digits)
    return binary_digits



def encode_msg(msg):
    encoding_scheme = get_encoding_scheme(msg)

    if encoding_scheme == "NUM":
        encoded_msg = encode_numeric(msg)

    elif encoding_scheme == "ALPHANUM":
        encoded_msg = encode_alphanum(msg)

    else:
        encoded_msg = encode_bytes(msg)
    
    return encoded_msg



print(encode_msg("8675309"))