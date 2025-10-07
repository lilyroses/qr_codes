# creator_generator_polynomials.py
import os
from collections import namedtuple
from operator import itemgetter

from log_table import log_table
from antilog_table import antilog_table


def print_polynomial(p):
  ps = []
  for t in p:
    ps.append(f"a{t[0]}x{t[1]}")
  return " + ".join(ps)


def fix_exponent(n):
  return (n%256) + (n//256)


def multiply_polynomials(p1,p2):
  new_terms = []
  for a, x in p1:
    for a2, x2 in p2:
      new_a = a+a2
      if new_a >= 256:
        new_a = fix_exponent(new_a)
      new_terms.append((new_a,x+x2))
  return new_terms


def combine_like_terms(new_terms):
  x_vals = [x for a,x in new_terms]
  x_counts = {}
  for x_val in x_vals:
    c = x_vals.count(x_val)
    if c > 1:
      x_counts[x_val] = c
  final_terms = [t for t in new_terms if t[1] not in x_counts]
  for x_val in x_counts:
    terms_to_combine = [a for a,x in new_terms if x == x_val]
    ints = [log_table[a] for a in terms_to_combine]
    xor_val = ints[0] ^ ints[1]
    if len(ints) > 2:
      return f"len(ints) = {len(ints)}"
    alpha = antilog_table[xor_val]
    final_terms.append((alpha, x_val))
  final_terms = sorted(final_terms, key=itemgetter(1), reverse=True)
  return final_terms


if __name__ == "__main__":
  start_polynomial = [(0,1),(0,0)]
  polynomials = [start_polynomial]
  ec_polynomials = {}

  for j in range(1, 69):

    multiplier_polynomial = [(0,1),(j,0)]
    current_polynomial = polynomials[-1]
    new_terms = multiply_polynomials(current_polynomial, multiplier_polynomial)
    final_terms = combine_like_terms(new_terms)

    mp = print_polynomial(multiplier_polynomial)
    cp = print_polynomial(current_polynomial)
    nt = print_polynomial(new_terms)
    ft = print_polynomial(final_terms)
    polynomials.append(final_terms)
    ec_polynomials[j+1] = final_terms

    tw = "-" * (os.get_terminal_size()[0] - 2)
    print(f"\n{tw}\n")
    print(f"\n\nSTEP {j}:")
    print(f"multiplier polynomial:")
    print(mp)
    print("\n")
    print(f"current polynomial:")
    print(cp)
    print("\n")
    print(f"new terms:")
    print(nt)
    print("\n")
    print(f"\nPOLYNOMIAL FOR {j+1} CODEWORDS:")
    print(ft)


  with open("error_correction_polynomials.py", "w") as f:
    s = f"error_correction_polynomials = {ec_polynomials}"
    f.write(s)
