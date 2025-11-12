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



def get_msg() -> str:
  while True:
    msg = input("Enter data to encode: ")
    if msg:
      return msg


def get_mode(msg:str) -> str:
  msg_chars = set(msg)
  if set(msg).issubset(NUMERIC_CHARSET):
    return "NUMERIC"
  if set(msg).issubset(ALPHANUMERIC_CHARSET):
    return "ALPHANUMERIC"
  return "BYTE"


def get_ec_lvl() -> str:
  while True:
    ec_lvl = input("Enter error correction level: ").upper()
    if not ec_lvl:
      return "Q"
    elif ec_lvl in ERROR_CORRECTION_LEVELS:
      return ec_lvl
    else:
      print("Error: Invalid error correction level.")


def get_version(msg:str, mode:str, ec_lvl:str) -> int:
  n = len(msg)
  for version, info in CHARACTER_CAPACITIES.items():
    char_cap = info[ec_lvl][mode]
    if char_cap >= n:
      return version
  return f"Message is too long for mode {mode}, EC level {ec_lvl}"


def encode(msg:str, mode:str, version:int) -> str:
  def encode_numeric(msg:str) -> str:
    chunk_size = 3
    msg_chunks = [msg[i:i+chunk_size] for i in range(0, len(msg), chunk_size)]
    return "".join([bin(int(chunk))[2:] for chunk in msg_chunks])
  def encode_alphanumeric(msg:str) -> str:
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
    return "".join(binary_strs)
  def encode_byte(msg:str) -> str:
    bin_vals = [bin(ord(char))[2:] for char in msg]
    binary_strs = []
    for val in bin_vals:
      pad_zeroes = "0" * (8 - len(val))
      binary_str = pad_zeroes + val
      binary_strs.append(binary_str)
    return "".join(binary_strs)
  assert mode in MODES, f"Mode {mode} not supported."
  if mode == "NUMERIC":
    data_bits = encode_numeric(msg)
  elif mode == "ALPHANUMERIC":
    data_bits = encode_alphanumeric(msg)
  elif mode == "BYTE":
    data_bits = encode_byte(msg)
  return data_bits


def get_data_cws(msg, mode, version, ec_lvl):
  mode_indicator = MODE_INDICATOR_BITS[mode]
  indicator_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
  char_count_indicator = bin(len(msg))[2:]
  if len(char_count_indicator) < indicator_len:
    pad_zeroes = "0" * (indicator_len - len(char_count_indicator))
    char_count_indicator = pad_zeroes + char_count_indicator
  msg_bits = encode(msg, mode, version)
  data_bits = mode_indicator + char_count_indicator + msg_bits

  req_bits = NUMBER_DATA_CODEWORDS[version][ec_lvl] * 8
  cur_bits = len(data_bits)
  b = req_bits - cur_bits
  t_bits = 4
  if b < t_bits:
    t_bits = b
  t_bits = t_bits * "0"

  data_bits += t_bits

  n = len(data_bits)
  pad_bits = "0" * (8 - (n % 8))

  data_bits += pad_bits

  byte_1 = "11101100"
  byte_2 = "00010001"

  n = len(data_bits)
  missing_bytes = (req_bits - n) // 8
  pad_bytes = []
  for i in range(missing_bytes):
    if i % 2 == 0:
      pad_bytes.append(byte_1)
    else:
      pad_bytes.append(byte_2)
  for pb in pad_bytes:
    data_bits += pb

  print(req_bits)
  data_cws = []
  for i in range(0, len(data_bits), 8):
    data_cws.append(data_bits[i:i+8])
  return data_cws


def convert_binary_codewords_to_ints(encoded_bytes):
  return [int(b,2) for b in encoded_bytes]



msg = "HELLO WORLD"
#msg = get_msg()

mode = get_mode(msg)

ec_lvl = "M"
#ec_lvl = get_ec_lvl()

version = get_version(msg, mode, ec_lvl)

cws = get_data_cws(msg, mode, version, ec_lvl)
print(cws)

ex = "00100000 01011011 00001011 01111000 11010001 01110010 11011100 01001101 01000011 01000000 11101100 00010001 11101100 00010001 11101100 00010001"
ex = ex.split()
print(cws==ex)
