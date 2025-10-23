# gf256.py
"""Create log and antilog tables for Galois field 256 (values
0-255. 
"""
from pprint import pprint


a = 2  # base (2**n)
mod_int = 285  # modulus value
gf_min, gf_max = (0,256)
gf256 = range(gf_min,gf_max)

powers = []  #
antilog_table = {}

for exp in gf256:
  if exp == 0:
    power = a**exp
  else:
    power = powers[-1] * a
    if power >= gf_max:
      power = power ^ mod_int

  powers.append(power)

  if power not in antilog_table:
    antilog_table[power] = exp


print("\n\nLOG TABLE:")
log_table = dict(zip(gf256, powers))
pprint(log_table)

print("\n\nANTILOG TABLE:")
pprint(antilog_table)
