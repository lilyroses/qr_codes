# create_qr_code.py
from data import (
  ALPHANUMERIC_CHARSET,
  CHARACTER_CAPACITIES,
  CHARACTER_COUNT_INDICATOR_LENGTHS,
  ERROR_CORRECTION_LEVELS,
  MODES,
  MODE_INDICATOR_BITS,
  NUMERIC_CHARSET,
  VERSIONS
)


########################################################################


# STEP 1 - ANALYZE DATA

# 1.1 - GET MESSAGE
def get_msg():
  while True:
    msg = input("Enter data to encode: ")
    if msg:
      return msg


# 1.2 - GET MODE
def analyze_data(msg):
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
def get_ec_lvl():
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
def get_version(msg, mode, ec_lvl):
  n = len(msg)
  for version, info in CHARACTER_CAPACITIES.items():
    char_cap = info[ec_lvl][mode]
    if char_cap >= n:
      return version
  return f"Message is too long for mode {mode}, EC level {ec_lvl}"

def get_qr_matrix_size(version):
  return VERSIONS[version]


# 2.3 - GET MODE INDICATOR
def get_mode_indicator(mode):
  assert mode in MODES, f"{mode} not a valid encoding mode (use one of: {MODES})"
  return MODE_INDICATOR_BITS[mode]


# 2.4 - GET CHARACTER COUNT INDICATOR
def get_character_count_indicator(msg, mode, version):
  indicator_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
  n = len(msg)
  char_count_indicator = bin(n)[2:]
  if len(char_count_indicator) < indicator_len:
    pad_zeroes = "0" * (indicator_len - len(char_count_indicator))
    char_count_indicator = pad_zeroes + char_count_indicator
  return char_count_indicator


# 2.5 - ENCODE USING CORRECT MODE

# 2.5.1 - ENCODE NUMERIC
def encode_numeric(msg):
  chunk_size = 3
  msg_chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]
  # convert each chunk into a 10, 7, or 4-bit binary number.
  binary_strs = [bin(int(chunk))[2:] for chunk in msg_chunks]
  return binary_strs


# 2.5.2 - ENCODE ALPHANUMERIC
def encode_alphanumeric(msg):
  chunk_size = 2
  char_values = [ALPHANUMERIC_CHARSET[char] for char in msg]
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


def encode(msg, mode, version):
  if mode == "NUMERIC":
    data_bits = encode_numeric(msg)
  elif mode == "ALPHANUMERIC":
    data_bits = encode_alphanumeric(msg)
  elif mode == "BYTE":
    


# 2.5.3 - ENCODE BYTE
def encode_byte(msg):
  bin_vals = [bin(ord(char))[2:] for char in msg]
  binary_strs = []
  for val in bin_vals:
    pad_zeroes = "0" * (8 - len(val))
    binary_str = pad_zeroes + val
    binary_strs.append(binary_str)
  return binary_strs


# STEP 2.6 - BREAK UP INTO 8 BIT CODEWORDS AND ADD PAD BYTES

# 2.6.1 - GET REQUIRED NUMBER OF BITS
def get_required_number_bits(version, ec_lvl):
  """Get the required number of data bits for the QR code based on
  its version and error correction level. To find this number, use the
  NUMBER_DATA_CODEWORDS table and multiply that value by 8, as each
  codeword is 1 byte (8 bits) long."""
  return NUMBER_DATA_CODEWORDS[version][ec_lvl] * 8


# 2.6.2 - ADD TERMINATOR BITS IF NECESSARY
def get_terminator_bits(

########################################################################

# STEO 3. 


########################################################################


# tests
#msg = get_msg()
#msg = "Hello, world!"
print(f"\n")
print("-"*45)
print("QR CODE GENERATOR\n")

msg = get_msg()
mode = analyze_data(msg)
ec_lvl = get_ec_lvl()
version = get_version(msg, mode, ec_lvl)
size = get_qr_matrix_size(version)

b = get_mode_indicator(mode)
cci = get_character_count_indicator(msg,mode,version)
bytes = encode_byte(msg)

print(f"\nMESSAGE : {msg}")
print(f"MODE : {mode}")
print(f"EC LVL : {ec_lvl}")
print(f"VERSION : {version}")
print(f"SIZE : {size[0]}x{size[1]} px")
print("ENCODED DATA :")
bs = f"{b} {cci}"
for byte in bytes:
  bs += f" {byte}"
print(f"\n{bs}\n")

