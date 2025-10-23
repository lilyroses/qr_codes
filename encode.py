# create_qr_code.py
from data import (
  ALPHANUMERIC_CHARSET,
  CHARACTER_CAPACITIES,
  CHARACTER_COUNT_INDICATOR_LENGTHS,
  ERROR_CORRECTION_LEVELS,
  MODES,
  MODE_INDICATOR_BITS,
  NUMBER_DATA_CODEWORDS,
  NUMERIC_CHARSET,
  VERSIONS
)


########################################################################

# STEP 1 - ANALYZE DATA

# 1.1 - GET MESSAGE
def get_msg() -> str:
  while True:
    msg = input("Enter data to encode: ")
    if msg:
      return msg


# 1.2 - GET MODE
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


########################################################################

# STEP 2 - ENCODE DATA


# 2.1 - GET ECC LVL
def get_ec_lvl() -> str:
  ec_lvl_info = """ERROR CORRECTION LEVEL PERCENT
Letters L, M, Q, H represent the four error correction levels, from low to high.
The percent value is the amount of damage a QR code can sustain while still being readable by the scanner.

+---------+-------+
| ECC LVL | % DMG |
+---------+-------+
|    L    |   7 % |
|    M    |  15 % |
|    Q    |  25 % |
|    H    |  30 % |
+---------+-------+

Defaults to 'Q' if no input is given.
"""
  while True:
    ec_lvl = input("Enter error correction level: ").upper()
    if not ec_lvl:
      return "Q"
    elif ec_lvl in ERROR_CORRECTION_LEVELS:
      return ec_lvl
    else:
      print("Error: Invalid error correction level.")


# 2.2 - GET VERSION
def get_version(msg:str, mode:str, ec_lvl:str) -> int:
  n = len(msg)
  for version, info in CHARACTER_CAPACITIES.items():
    char_cap = info[ec_lvl][mode]
    if char_cap >= n:
      return version
  return f"Message is too long for mode {mode}, EC level {ec_lvl}"

def get_qr_matrix_size(version: int) -> tuple[int]:
  return VERSIONS[version]


# 2.3 - GET MODE INDICATOR
def get_mode_indicator(mode:str) -> str:
  assert mode in MODES, f"{mode} not a valid encoding mode (use one of: {MODES})"
  return MODE_INDICATOR_BITS[mode]


# 2.4 - GET CHARACTER COUNT INDICATOR
def get_character_count_indicator(msg:str, mode:str, version:int) -> str:
  indicator_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
  n = len(msg)
  char_count_indicator = bin(n)[2:]
  if len(char_count_indicator) < indicator_len:
    pad_zeroes = "0" * (indicator_len - len(char_count_indicator))
    char_count_indicator = pad_zeroes + char_count_indicator
  return char_count_indicator


########################################################################

# 2.5 - ENCODE USING CORRECT MODE

# 2.5.1 - ENCODE NUMERIC
def encode_numeric(msg:str) -> str:
  # TODO! DOCTSTRING
  chunk_size = 3
  msg_chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]
  # convert each chunk into a 10, 7, or 4-bit binary number.

#  Return list of bit strs
#  return [bin(int(chunk))[2:] for chunk in msg_chunks]

  # Return bit str
  return "".join([bin(int(chunk))[2:] for chunk in msg_chunks])


# 2.5.2 - ENCODE ALPHANUMERIC
def encode_alphanumeric(msg:str) -> str:
  # TODO! DOCSTRING
  chunk_size = 2
  char_values = [ALPHANUMERIC_CHARSET[char] for char in msg]
  char_value_pairs = [char_values[i:i+chunk_size] for i in range(0, len(char_values), chunk_size)]

  # Bit strings for encoded alphanumeric pairs of strs.
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
#  return binary_strs

  # Return one bit str instead of list of strs
  return "".join(binary_strs)


# 2.5.3 - ENCODE BYTE
def encode_byte(msg:str) -> str:
  # TODO! DOCSTRING
  bin_vals = [bin(ord(char))[2:] for char in msg]
  binary_strs = []
  for val in bin_vals:
    pad_zeroes = "0" * (8 - len(val))
    binary_str = pad_zeroes + val
    binary_strs.append(binary_str)
#  return binary_strs

  # Return one bit str instead of list of strs
  return "".join(binary_strs)


def encode(msg:str, mode:str, version:int) -> str:
  # TODO! DOCSTRING
  assert mode in MODES, f"Mode {mode} not supported."
  if mode == "NUMERIC":
    data_bits = encode_numeric(msg)
  elif mode == "ALPHANUMERIC":
    data_bits = encode_alphanumeric(msg)
  elif mode == "BYTE":
    data_bits = encode_byte(msg)
  return data_bits

########################################################################

# STEP 2.6 - BREAK UP INTO 8 BIT CODEWORDS AND ADD PAD BYTES

# 2.6.1 - GET REQUIRED NUMBER OF BITS
def get_req_bits(version:int, ec_lvl:str) -> int:
  """Get the required number of data bits needed for the QR code.
  Each data codeword is 1 byte (8 bits) long, so multiply the
  value by 8 for total number of bits."""
  req_bits = NUMBER_DATA_CODEWORDS[version][ec_lvl] * 8
  return req_bits


# 2.6.2 - ADD TERMINATOR BITS IF NECESSARY
def get_terminator_bits(encoded_bits:str) -> str:
  cur_bits = len(encoded_bits)
  req_bits = get_req_bits(version, ec_lvl)
  b = req_bits - cur_bits
  t_bits = 4
  if b < t_bits:
    t_bits = b
  return t_bits * "0"

# 2.6.3 - ADD MORE 0s TO MAKE BIT LENGTH A
#  MULTIPLE OF 8
def get_bits_for_full_bytes(encoded_bits):
  n = len(encoded_bits)
  pad_bits = "0" * (8 - (n % 8))
  return pad_bits


# 2.6.4 - ADD PAD BYTES TO FILL REQ BITS
def get_pad_bytes(encoded_bits:str, version:int, ec_lvl:str) -> list[str]:
  byte_1 = "11101100"
  byte_2 = "00010001"

  n = len(encoded_bits)
  req_bits = get_req_bits(version, ec_lvl)
  missing_bytes = (req_bits - n) / 8
  if int(missing_bytes) != missing_bytes:
    return missing_bytes

  missing_bytes = int(missing_bytes)
  pad_bytes = []
  for i in range(missing_bytes):
    if i % 2 == 0:
      pad_bytes.append(byte_1)
    else:
      pad_bytes.append(byte_2)
  return pad_bytes


########################################################################

# STEP 3.


########################################################################


# tests
#msg = get_msg()
#msg = "Hello, world!"
print(f"\n")
print("-"*45)
print("QR CODE GENERATOR\n")

#msg = get_msg()
msg = "HELLO WORLD"
mode = analyze_data(msg)
#ec_lvl = get_ec_lvl()
ec_lvl = "Q"
version = get_version(msg, mode, ec_lvl)
size = get_qr_matrix_size(version)

mode_indicator_bits = get_mode_indicator(mode)
char_count_indicator_bits = get_character_count_indicator(msg,mode,version)
encoded_msg_bits = encode(msg, mode, version)
encoded_msg_bytes = [encoded_msg_bits[i:i+8] for i in range(0,len(encoded_msg_bits),8)]

# COMBINE MODE, CHAR COUNT, MSG BITS
bit_strs = [mode_indicator_bits, char_count_indicator_bits, encoded_msg_bits]
encoded_bits = "".join(bit_strs)

# GET TERMINATOR BITS
term_bits = get_terminator_bits(encoded_bits)
encoded_bits += term_bits

# EXTRA BITS TO MAKE STR LEN A MULTIPLE OF 8
extra_bits = get_bits_for_full_bytes(encoded_bits)
encoded_bits += extra_bits

# PAD BYTES
pad_bytes = get_pad_bytes(encoded_bits, version, ec_lvl)

encoded_bytes = [encoded_bits[i:i+8] for i in range(0,len(encoded_bits),8)]
for pad_byte in pad_bytes:
  encoded_bytes.append(pad_byte)


print(f"\nMESSAGE : {msg}")
print(f"MODE : {mode}")
print(f"EC LVL : {ec_lvl}")
print(f"VERSION : {version}, type(version)={type(version)}")
print(f"SIZE : {size[0]}x{size[1]} px")

print(f"\nMODE INDICATOR BITS: {mode_indicator_bits}")
print(f"CHAR COUNT INDICATOR BITS: {char_count_indicator_bits}")
#print(f"MSG BITS: {encoded_msg_bits}")
print(f"MSG BYTES: {encoded_msg_bytes}")

print(f"TERMINATOR BITS: {term_bits}")
print(f"EXTRA BITS (TO MAKE FULL BYTES): {extra_bits}")
print(f"PAD BYTES: {pad_bytes}")

print(f"\nALL BYTES:\n")
for i, eb in enumerate(encoded_bytes,1):
  print(i, eb)

