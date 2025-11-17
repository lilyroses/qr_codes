from data import (
  ALPHANUMERIC_CHARSET,
  CHARACTER_CAPACITIES,
  CHARACTER_COUNT_INDICATOR_LENGTHS,
  ERROR_CORRECTION_LEVELS,
  MODES,
  NUMERIC_CHARSET,
  NUM_CODEWORDS
)


# GET MSG
def get_msg():
  while True:
    msg = input("\nMessage to encode (q to quit): ")
    if not msg:
      print("Error: message cannot be empty.")
    else:
      if msg.lower() == "q":
        return "Exiting..."
      confirm = input(f"You entered:\n\n{msg}\n\nConfirm? (y/n): ")
      if confirm.lower() == "y":
        return msg
      else:
        continue


# GET EC LVL
def get_ec_lvl():
  while True:
    ec_lvl = input("EC lvl: ").upper()
    if not ec_lvl:
      ec_lvl = "Q"
    if ec_lvl in ERROR_CORRECTION_LEVELS:
      return ec_lvl
    print(f"Invalid error correction level. Options are: {list(ERROR_CORRECTION_LEVELS.keys())}")


# ------------------------------------------------------------


# ENCODE DATA
def encode(msg, ec_lvl):
  # GET MODE
  def get_mode(msg):
    if set(msg).issubset(NUMERIC_CHARSET):
      mode = "NUMERIC"
    elif set(msg).issubset(ALPHANUMERIC_CHARSET):
      mode = "ALPHANUMERIC"
    else:
      mode = "BYTE"
    return mode


  # GET VERSION
  def get_version(msg, ec_lvl, mode):
    n = len(msg)
    for version, info in CHARACTER_CAPACITIES.items():
      char_cap = info[ec_lvl][mode]
      if char_cap >= n:
        return version
    return f"Message is too long for mode {mode} and error correction level {ec_lvl}."


  # GET MODE INDICATOR
  def get_mode_indicator(mode):
    mode_indicator = MODES[mode]
    return mode_indicator


  # GET CHAR COUNT INDICATOR
  def get_char_count_indicator(msg, mode, version):
    """The character count indicator is a string of bits that indicates how many
    bits are in the original encoded mesaage. These bits are derived by
    counting the number of bits in the original encoded message, then converting
    that number to binary. This binary number must be a certain
    length, depending on the version and encoding mode used.
    The length is defined in the QR specification and a table has been made in
    `data.py` in the dict CHAR_COUNT_INDICATOR_LENS.
     """
    n = len(msg)
    bin_n = bin(n)[2:]
    char_count_indicator_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
    num_pad_bits = char_count_indicator_len - len(bin_n)
    pad_zeroes = "0" * num_pad_bits
    char_count_indicator = pad_zeroes + bin_n
    return char_count_indicator


# ------------------------------------------------------------


  # ENCODE MODES

  # ENCODE NUMERIC
  def encode_numeric(msg):
    """Split msg into 3-digit chunks. The last chunk may necessarily be
    less than 3 digits. Convert each digit chunk to an int value. If the
    resulting int has 3 digits, convert it to a 10-digit binary str.
    If it has 2 digits, convert it to a 7-digit binary str. If it has
    1 digit, convert it to a 4-digit binary str. Concatenate all the
    binary digit strings to produce the msg bits.
    """
    n = len(msg)
    chunk_size = 3
    encoded_data = ""
    for i in range(0, n, chunk_size):
      digits = msg[i:i+chunk_size]
      int_val = int(digits)
      if len(str(int_val)) == 3:
        bit_str_len = 10
      elif len(str(int_val)) == 2:
        bit_str_len = 7
      elif len(str(int_val)) == 1:
        bit_str_len = 4
      bin_str = bin(int_val)[2:]
      pad_zeroes = "0" * (bit_str_len - len(bin_str))
      bin_str = pad_zeroes + bin_str
      encoded_data += bin_str
    return encoded_data


  # ENCODE ALPHANUMERIC
  def encode_alphanumeric(msg):
    n = len(msg)
    chunk_size = 2
    encoded_data = ""
    for i in range(0, n, chunk_size):
      char_pair = msg[i:i+chunk_size]
      if len(char_pair) == 1:
        c1 = char_pair[0]
        val = ALPHANUMERIC_CHARSET[c1]
        bit_str_len = 6
      elif len(char_pair) == 2:
        c1, c2 = char_pair
        v1 = ALPHANUMERIC_CHARSET[c1]
        v2 = ALPHANUMERIC_CHARSET[c2]
        val = (v1 * 45) + v2
        bit_str_len = 11
      bin_str = bin(val)[2:]
      pad_zeroes = "0" * (bit_str_len - len(bin_str))
      bin_str = pad_zeroes + bin_str
      encoded_data += bin_str
    return encoded_data


  # ENCODE BYTE
  def encode_byte(msg):
    encoded_data = ""
    for char in msg:
      bin_val = bin(ord(char))[2:]
      num_pad_bits = 8 - len(bin_val)
      pad_zeroes = "0" * num_pad_bits
      bin_str = pad_zeroes + bin_val
      encoded_data += bin_str
    return encoded_data


# ------------------------------------------------------------


  # GET DATA CODEWORDS
  def get_data_codewords(ec_lvl, version, mode_indicator, char_count_indicator, encoded_data):
    bit_str = mode_indicator + char_count_indicator + encoded_data
    # get terminator bits
    req_num_data_codewords = NUM_CODEWORDS[version][ec_lvl]["total_data_cws"]
    req_num_bits = req_num_data_codewords * 8
    cur_num_bits = len(bit_str)
    num_term_bits = req_num_bits - cur_num_bits
    if num_term_bits >= 4:
      num_term_bits = 4
    term_bits = "0" * num_term_bits
    # add terminator bits
    bit_str += term_bits
    # get pad bits
    n = len(bit_str)
    if n % 8 == 0:
      pad_bits = ""
    else:
      num_bytes = n // 8
      req_bytes = num_bytes + 1
      req_bits = (req_bytes * 8) - n
      pad_bits = "0" * req_bits
    bit_str += pad_bits

    # Get pad bytes
    data_codewords = []
    for i in range(0, len(bit_str), 8):
      data_codeword = bit_str[i:i+8]
      data_codewords.append(data_codeword)
    assert len(data_codewords[-1]) == 8, "Error: bit str should have length that is multiple of 8."

    pad_byte_1 = "11101100"  # 236
    pad_byte_2 = "00010001"  # 17

    current_num_bytes = len(data_codewords)
    num_missing_bytes = req_num_data_codewords - current_num_bytes
    for i in range(num_missing_bytes):
      if i % 2 == 0:
        data_codewords.append(pad_byte_1)
      else:
        data_codewords.append(pad_byte_2)
    return data_codewords


  mode = get_mode(msg)
  version = get_version(msg, ec_lvl, mode)
  mode_indicator = get_mode_indicator(mode)
  char_count_indicator = get_char_count_indicator(msg, mode, version)

  if mode == "NUMERIC":
    encoded_data = encode_numeric(msg)
  elif mode == "ALPHANUMERIC":
    encoded_data = encode_alphanumeric(msg)
  elif mode == "BYTE":
    encoded_data = encode_byte(msg)

  data_codewords = get_data_codewords(ec_lvl, version, mode_indicator, char_count_indicator, encoded_data)
  return data_codewords


if __name__ == "__main__":
  msg = get_msg()
  ec_lvl = get_ec_lvl()
  data_codewords = encode(msg, ec_lvl)
  print(data_codewords)
