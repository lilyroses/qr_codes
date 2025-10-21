# creator_generator_polynomials.py
import os
from operator import itemgetter
from data import ANTILOG_TABLE, LOG_TABLE

def print_polynomial(p):
  """Print polynomial in readable format. Each term has consistent variables of (a,x) which allows constructing
  readable format by attaching strings 'a', 'x' to each int in each tuple of the polynomial representation, p."""
#  ps = []
#  for t in p:
#    ps.append(f"a{t[0]}x{t[1]}")
#  return " + ".join(ps)
  return " + ".join([f"a{t[0]}x{t[1]}" for t in p])  # shortcut?

def fix_exponent(n):
  """Ensure exponents of all terms are within Galois field gf(256)."""
  return (n%256) + (n//256)

# TODO! DOUBLE CHECK DOCSTRING ACCURACY
def multiply_polynomials(p1,p2):
  """Multiply terms from each of the two polynomials to create the next step's p1 polynomial. Polynomials are
  represented as a list of tuples of ints where each tuple is the (coefficient, exponent) for a given term.

  p1: the starting polynomial; either the initial polynomial as detailed in the section on polynomial
      generation for error correction in the QR code documentation for the first step, or, for all
      subsequent steps, the polynomial generated in the previous step.

  p2: the multiplier polynomial; the initial multiplier polynomial is given in the documentation,
      and each subsequent step uses the previous p2 polynomial with second term's x variable
      incremented by 1."""
  new_terms = []
  for a, x in p1:
    for a2, x2 in p2:
      new_a = a+a2
      if new_a >= 256:
        new_a = fix_exponent(new_a)
      new_terms.append((new_a,x+x2))
  return new_terms

def combine_like_terms(new_terms):
  """Combine like terms from the generated polynomials."""
  x_vals = [x for a,x in new_terms]
  x_counts = {}
  for x_val in x_vals:
    c = x_vals.count(x_val)
    if c > 1:
      x_counts[x_val] = c
  final_terms = [t for t in new_terms if t[1] not in x_counts]
  for x_val in x_counts:
    terms_to_combine = [a for a,x in new_terms if x == x_val]
    ints = [LOG_TABLE[a] for a in terms_to_combine]
    xor_val = ints[0] ^ ints[1]
    if len(ints) > 2:
      return f"len(ints) = {len(ints)}"
    alpha = ANTILOG_TABLE[xor_val]
    final_terms.append((alpha, x_val))
  final_terms = sorted(final_terms, key=itemgetter(1), reverse=True)
  return final_terms


if __name__ == "__main__":

  # (coefficient, exponent) for each term of the starting polynomial a given in the QR code specification
  start_polynomial = [(0,1),(0,0)]
  polynomials = [start_polynomial]
  ec_polynomials = {1: start_polynomial}

  # there are 68 error correction codewords as detailed in QR code specification
  for j in range(1, 69):

    # initial values are as specified in documentation; j increments with each consecutive step
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
    s = f"ERROR_CORRECTION_POLYNOMIALS = {ec_polynomials}"
    f.write(s)
