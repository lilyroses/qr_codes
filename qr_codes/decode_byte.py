from data import MODES, CHARACTER_COUNT_INDICATOR_LENGTHS


INF = "t.txt"
with open(INF) as f:
  bits = "".join([line.strip().split()[2] for line in f.readlines()])


def decode_mode(bits):
  mode_ind = bits[:4]
  for mode_name, ind in MODES.items():
    if ind == mode_ind:
      return mode_name

def decode_char_count_indicator(bits):
  cci_len = CHARACTER_COUNT_INDICATOR_LENGTHS[version][mode]
  return bits[4:4+cci_len]

def get_msg_bytes(bits, cci):
  n = len(cci)
  bits = bits[4+n:]
  bytes = []
  for i in range(0, len(bits), 8):
    bytes.append(bits[i:i+8])
  return bytes

def decode_byte(msg_bytes):
  chars = []
  for byte in msg_bytes:
    chars.append(chr(int(byte,2)))
  return "".join(chars)


ec_lvl = "Q"
version = 5
mode = decode_mode(bits)
cci = decode_char_count_indicator(bits)
msg_bytes = get_msg_bytes(bits, cci)
msg = decode_byte(msg_bytes)

print(f"mode: {mode}")
print(f"cci: {cci}")
print(f"msg: {msg}")
