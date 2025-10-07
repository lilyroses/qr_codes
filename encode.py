# encode.py
import json
from data import (
    ALPHANUMERIC_CHARSET,
    ALPHANUMERIC_CHARSET_VALUES,
    CHARACTER_CAPACITIES,
    CHARACTER_COUNT_INDICATORS,
    ERROR_CORRECTION_LEVELS,
    MODE_NAMES,
    MODE_NAME_INDICATOR_BITS,
    NUMERIC_CHARSET
)


###############################################################################


# STEP 1. ANALYZE DATA
# ----------------------------------------------------------------
# Determine which encoding scheme is needed for the message data in order
# to produce the smallest amount of bits possible. Kanji mode is also an
# encoding scheme supported by the QR code specification, but it is not
# implemented here. This may change in future versions.
#
# Encoding schemes supported by this tool are:
# 	NUMERIC 	(0-9)
#	ALPHANUMERIC	(0-9, A-Z, several symbols)
# 	BYTE		(0-9, A-Z, a-z, symbols)


def analyze_data(msg:str) -> str:
    """Determine appropriate encoding scheme for the message so the fewest
    bits are used."""
    msg_chars = set(msg)
    # Numeric mode
    if set(msg).issubset(NUMERIC_CHARSET):
        return "NUMERIC"
    # Alphanumeric mode
    if set(msg).issubset(ALPHANUMERIC_CHARSET):
        return "ALPHANUMERIC"
    # Byte mode
    return "BYTE"


##############################################################################


# STEP 2. ENCODE DATA
# ----------------------------------------------------------------
# Consists of the following steps:
# 	1. Choose error correction level (given as parameter for encode())
#     	2. Determine smallest version for data
#     	3. Add mode indicator
#     	4. Add character count indicator
#     	5. Encode using the selected mode
#     	6. Break up into 8-bit codewords and add pad bytes if necessary


# 2.1 CHOOSE ERROR CORRECTION LEVEL
# ----------------------------------------------------------------
# There are 4 levels of error correction, each denoted by a letter.
# The value associated with each level indicates the maximum percentage
# of the QR code that can be damaged while still being readable by QR scanners.
#
# The error correction level can be set as an argument for the
# `encode()` function.
#
# ERROR CORRECTION LEVELS AND PERCENT MAXIMUM DAMAGE ALLOWED:
#	L:  7
#	M: 15 %
#	Q: 25 %
#	H: 30 %


# 2.2 DETERMINE VERSION NUMBER
# ----------------------------------------------------------------
# QR code version numbers refer to the size of the QR matrix in pixel
# height and width. Each QR matrix is exactly as wide as it is tall.
# The single value associated with each version number indicates the
# pixel height as well as the pixel width.
#
# The smallest version, Version 1, is 21 x 21 pixels. Each sucessive
# version increments in size by 4 pixels, capping at 177 x 177 pixels
# for Version 40. Each version number is capable of encoding a specific
# number of data codewords and error correction codewords. Each error
# correction level and version number combination has a specific number
# of data codewords and error correction codewords that can be encoded
# by that size QR code. The values denoting bit storage for each mode
# and error correction level combination are stored in `data.py` and
# can be accessed with `CHARACTER_CAPACITIES[ec_lvl][mode]`.
#
# +-----------+------+
# | Version # | Size |
# +-----------+------+
# |    1      |  21  |
# |    2      |  25  |
# |    3      |  29  |
# |    4      |  33  |
# |    5      |  37  |
# |   ...     | (+4) |
# |   40      | 177  |
# +-----------+------+


def get_version_number(msg:str, mode:str, ec_lvl="Q"):
    """
    Find the minumum QR matrix size required to contain the characters in
    msg, using the message length, the encoding mode, and the error correction
    level."""
    n = len(msg)

    for version_num, info in CHARACTER_CAPACITIES.items():
        char_cap = info[ec_lvl][mode]
        if char_cap >= n:
            return version_num

    return f"Message is too long for mode {mode} with EC level {ec_lvl}"


###################################################################>


# STEP 2. ADD MODE INDICATOR
def get_mode_indicator(mode):
    """Return mode indicator bit string for message encoding type."""
    assert mode in MODE_NAMES, f"{mode} not recognized (options are {MODE_NAMES})"

    mode_indicator = MODE_NAME_INDICATOR_BITS[mode]
    return mode_indicator


###################################################################>


# STEP 3. ADD CHARACTER COUNT INDICATOR
def get_character_count_indicator(msg, version, mode):
    """
    The character count indicator is a string of bits that represents the
    number of encoded characters. The character count indicator must be placed
    after the mode indicator. The character count indicator is a certain number
    of bits, depending on the version number.
    """
    n = len(msg)
    bin_str = bin(n)[2:]

    indicator_str_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
    pad_zeroes = "0" * (indicator_str_len - len(bin_str))

    char_count_indicator = pad_zeroes + bin_str
    return char_count_indicator


###################################################################>


# STEP 4. ENCODE USING DETERMINED MODE
def encode_numeric(msg):
    """Split the message into groups of 3 numbers. The final group may be 1 or
    2 numbers. If a group starts with one zero it is a 2-digit number. If a
    group starts with 2 zeroes it is a 1-digit number. Convert 3-digit numbers
    to 10-bit binary numbers. Convert 2-digit numbers to 7-bit binary numbers.
    1-digit chunks should be converted to 4-digit binary numbers."""
    chunk_size = 3
    msg_chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]

    # convert each chunk into a 10, 7, or 4-bit binary number.
    binary_strs = [bin(int(chunk))[2:] for chunk in msg_chunks]
    return binary_strs


def encode_alphanumeric(msg):
    """Split message into pairs of characters. Each character is represented
    by a numeric value; refer to ALPHANUMERIC_CHARSET_VALUE_MAP for the
    character mapping. Obtain the values for each pair of characters. Multiply
    the first character's value by 45. Then add that number to the value of
    the second character. Convert this value to an 11-bit binary string. If
    the final grouping of characters only had one character (in the case of an
    odd number of characters in the message), take the value of that character
    and convert it to a 6-bit binary string."""
    chunk_size = 2
    char_values = [ALPHANUMERIC_CHARSET_VALUE[char] for char in msg]
    char_value_pairs = [char_values[i:i+chunk_size] for i in range(0, len(char_values), chunk_size)]

    binary_strs = []
    for pair in char_value_pairs:
        if len(pair) == 2:
            val = (pair[0]*45) + pair[1]
            bin_val = bin(val)[2:]
            pad_zeroes = "0" * (11 - len(bin_val))
        else:
            val = pair[0]
            bin_val = bin(val)[2:]
            pad_zeroes = "0" * (6 - len(bin_val))
        binary_str = pad_zeroes + bin_val
        binary_strs.append(binary_str)

    return binary_strs


def encode_byte(msg):
    """Encode each character of the message into an 8 bit binary string."""
    bin_vals = [bin(ord(char))[2:] for char in msg]
    binary_strs = []
    for val in bin_vals:
        pad_zeroes = "0" * (8 - len(val))
        binary_str = pad_zeroes + val
        binary_strs.append(binary_str)
    return binary_strs


###################################################################>


def get_num_required_bits(mode, version, ec_lvl):
    """Find required number of data bits for the QR code's version number, error
    correction level, and encoding mode."""
    required_codewords = CHARACTER_CAPACITIES[version][ec_lvl][mode]
    required_bits = required_codewords * 8
    return required_bits


# TODO!
def encode_msg(msg, ec_lvl="Q"):
    """Encode the message using the given mode and version number."""
    mode = analyze_data(msg)
    version = get_version_number(msg, mode, ec_lvl)
    mode_indicator = get_mode_indicator(mode)
    character_count_indicator = get_character_count_indicator(msg, version, mode)

    if mode == "NUMERIC":
        binary_strs = encode_numeric(msg)
    elif mode == "ALPHANUMERIC":
        binary_strs = encode_alphanumeric(msg)
    elif mode == "BYTE":
        binary_strs == encode_byte(msg)

    encoded_msg = f"{mode_indicator} {character_count_indicator} {binary_strs}"

    return encoded_msg


print(encode_msg("8675309"))
print(encode_msg("HELLO WORLD"))
print(encode_msg("Hello there, world!"))
