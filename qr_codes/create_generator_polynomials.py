# creator_generator_polynomials.py
import os
from operator import itemgetter
from data import ANTILOG_TABLE, LOG_TABLE
from pprint import pprint


def format_polynomial_readable(p, fmt_latex=False):
  """Print polynomial in readable format. Each term has consistent variables of (a,x) which allows constructing
  readable format by attaching strings 'a', 'x' to each int in each tuple of the polynomial representation, p."""
  terms = []
  for a_exp, x_exp in p:
    if fmt_latex == True:
      fmt_a = f"a^{{{a_exp}}}"
      fmt_x = f"x^{{{x_exp}}}"
    else:
      fmt_a = f"a^{a_exp}"
      fmt_x = f"x^{x_exp}"
    fmt_term = f"{fmt_a}{fmt_x}"
    terms.append(fmt_term)

  fpoly = " + ".join(terms)
  if fmt_latex == True:
    fpoly = f"${fpoly}$"
  return fpoly


# TODO! DOUBLE CHECK DOCSTRING ACCURACY
def multiply_polynomials(p1, p2):
  """Multiply terms from each of the two polynomials to create the next step's p1 polynomial. Polynomials are
  represented as a list of tuples of pairs of ints where each tuple is (a's exponent, x's exponent) for variables
  a and x respectively for each term in the polynomial.

  Polynomial terms are always a^{n}x^{n}. The terms only differ in their exponents; variables are always
  a and x and both always have coefficients of 1.

  p1: list of 2-int tuples; e.g. [(0,p10), (251,9), (67,8) ... ]
      the starting polynomial; either the initial polynomial as detailed in the section on polynomial
      generation for error correction in the QR code documentation for the first step, or, for all
      subsequent steps, the polynomial generated in the previous step.

  p2: list of 2-int tuples; e.g. [(0,p10), (251,9), (67,8) ... ]
      the multiplier polynomial; the initial multiplier polynomial is given in the documentation,
      and each subsequent step uses the previous p2 polynomial with second term's x variable
      incremented by 1.0
  """
  terms = []

  for a, x in p1:  # for exponents of a and x
    for a2, x2 in p2:  # for exponents of a and x
      new_a = a + a2
      if new_a >= 256:
        new_a = (new_a % 256) + (new_a // 256)  # as detailed in the specs
      new_x = x + x2
      term = (new_a, new_x)
      terms.append(term)
  return terms


def combine_like_terms(terms:list[tuple[int]]):
  """
  Combine like terms from the generated polynomials. To combine like terms,
  find all terms that have the same x exponent. Each tuple in `terms` has 2
  integers. The first integer represents the `a` variable's exponent. The
  second integer represents the `x` variable's exponent.

  For example, if:

      terms = [(0,3), (25,2), (1,1), (2,2), (27,1), (3,0)]

  There are 2 like terms with an x exponent of 2 (the second number in the
  tuple):

      (25,2) and (2,2)

  There are also 2 like terms with an x exponent of 1:

      (1,1) and (27,1)

  The next step is to find the integer representation of each `a` variable's
  exponent for the like terms (the first number in each tuple), using the
  LOG_TABLE:

    a variables for x^2: 25, 2 -> 3, 4
    a variables for x^1: 1, 27 -> 2, 12

  Then, XOR these integers together:

    a integers for x^2: 3^4 = 7
    a integers for x^1: 2^12 = 14

  Now, use the ANTILOG_TABLE to convert these integers
  back to alpha exponents:

    a exponent for x^2: ANTILOG[7] = 198
    a exponent for x^1: ANTILOG[14] = 199


  Create new terms for the combined terms:

    (198,2) and (199,1)

  The final terms are:

    [(0,3), (198,2), (199,1), (3,0)]


  """
  # Step 1: find all terms with the same x exponent. the x exponent is the second number in
  # each tuple in `terms`
  x_exps = [x_exp for (a_exp,x_exp) in terms]
  # find the x exponents that occur more than once
  x_exp_counts = {x_exp: x_exps.count(x_exp) for x_exp in x_exps if x_exps.count(x_exp) > 1}

  # start a list of tuples containing the final terms starting with non-like terms
  final_terms = [(a_exp,x_exp) for (a_exp,x_exp) in terms if x_exp not in x_exp_counts]

  # Step 2: get the a exponent integer values by looking up their log values
  for like_x_exp in x_exp_counts:
    like_a_exps = [a_exp for (a_exp, x_exp) in terms if x_exp == like_x_exp]
    a_exp_ints = [LOG_TABLE[a_exp] for a_exp in like_a_exps]
    xor_val = a_exp_ints[0] ^ a_exp_ints[1]
    if len(a_exp_ints) > 2:
      return f"len(a_exp_ints) = {len(a_exp_ints)}"
    alpha = ANTILOG_TABLE[xor_val]
    final_terms.append((alpha, like_x_exp))

  final_terms = sorted(final_terms, key=itemgetter(1), reverse=True)
  return final_terms


def generate_polynomial(current_polynomial, multiplier_polynomial):
  new_terms = multiply_polynomials(current_polynomial, multiplier_polynomial)
  final_terms = combine_like_terms(new_terms)
  return final_terms

if __name__ == "__main__":
  # (coefficient, exponent) for each term of the starting polynomial a given in the QR code specification
  start_polynomial = ((0,1),(0,0))
  polynomials = [start_polynomial]
  ec_polynomials = {1: start_polynomial}
  # there are 68 error correction codewords as detailed in QR code specification
  for j in range(1, 254):
    # initial values are as specified in documentation; j increments with each consecutive step
    multiplier_polynomial = ((0,1),(j,0))
    current_polynomial = polynomials[-1]
    polynomial = generate_polynomial(current_polynomial, multiplier_polynomial)

    polynomials.append(polynomial)
    ec_polynomials[j+1] = polynomial

    tw = "-" * (os.get_terminal_size()[0] - 2)
    print(f"\n{tw}\n")
    print(f"\n\nPOLYNOMIAL FOR {j+1} CODEWORDS:\n")
    print(f"MULTIPLIER POLYNOMIAL:  {format_polynomial_readable(multiplier_polynomial)}")
    print("\nNEW POLYNOMIAL:\n")

    print(f"{format_polynomial_readable(polynomial)}")

#    print(format_polynomial_latex(polynomial))
  import io
  output = io.StringIO()
  with open("error_correction_polynomials.py", "w") as f:
  
    p = pprint(ec_polynomials, sort_dicts=False, indent=4, stream=output)
    fp = output.getvalue()
    s = f"ERROR_CORRECTION_POLYNOMIALS = {fp}"
    f.write(s)
