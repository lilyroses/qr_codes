# error_encoding.py
from encode import encode
from error_correction_polynomials import ERROR_CORRECTION_POLYNOMIALS as ECP
from data import (
  ANTILOG_TABLE,
  LOG_TABLE,
  NUM_CODEWORDS
)

# for now, use these example vars
ec_lvl = "M"
version = 1
msg = "HELLO WORLD"

data_cws = encode(msg, ec_lvl)
num_ec_cws = NUM_CODEWORDS[version][ec_lvl]["total_ec_cws"]

# The polynomials used all follow the same structure:
# i{x}**e where i is some integer coefficient
# of x and e is x's exponent. This is the polynomial in integer notation, represented
# in this code as a list of tuples e.g.:
# `poly_int = [(32,2), (91,1), (8,0)]`
# When the polynomial is in alpha notation, `i` 
#  i becomes a**n where a is alpha=2 and n is
#  the alpha exponent derived from ANTILOG[i].

# NOTE ON POLYNOMIAL VARIABLE NAMES:
#
#  - polynomial_int : a list of tuples representing
#    polynomial terms in INTEGER NOTATION. In other
#    words, the polynomial is represented as a
#    `poly = [(i,e) ...]` where `i` is the x
#    var's integer coefficient and `e` is the
#    x variable's exponent value.
#    E.g. for the tuple (32, 10) this represents
#    a polynomial term with an x coefficient of
#    32 and an x exponent of 10: 32x**10
#
#  - polynomial_alpha : a list of tuples representing
#    polynomial terms in ALPHA NOTATION. In other
#    words, the first number in each tuple is
#    the x var's coefficient, but converted to
#    the form a**n where a=2 and n is the ANTILOGnumber in the tuple. in ALPHA notation (e.g. (5,10) is
#    a**5x**10)

# x exponents are x**(n-1) ... x**0 where n is
# the number of data codewords

# int > alpha (32 > a**5): ANTILOG_TABLE
# alpha > int (a**5 > 32): LOG_TABLE


# STEP 0:
# GET DATA CODEWORDS OF ENCODED MSG, CONVERT
# EACH CODEWORD'S BIN STR TO INT TO GET THE
# msg_polynomial's `x` COEFFICIENTS. THE `x_exps`
# ARE (x**n-1 ... x**0) WHERE `n` IS THE NUMBER
# OF DATA CODEWORDS.
#
# E.g.
# If data_codewords ints are:
#   [32, 91, 16]
#
# Then x_exps are:
#   [2, 1, 0]
#
# And the message polynomial is:
#   32x**2 + 91x**1 + 16x**0
#
# Represented as:
#   msg_polynomial_int = [(32,2), (91,1), (16,0)]
# (each tuple being the integer coefficient and
# x exponent for each term. For alpha notation,
# variable names end in 'alpha'.)
coefs = [int(cw,2) for cw in data_cws]
x_exps = list(range(len(coefs)-1,-1,-1))
msg_poly_int = tuple(zip(coefs, x_exps))
print(f"\nSTEP 1: GET int_msg_poly BY CONVERTING DATA CW BIN STRS TO INTS:\n{msg_poly_int}")


# STEP 2: GET GENERATOR POLYNOMIAL (ERROR CORRECTION
#  POLYNOMIAL)
gen_poly_alpha = ECP[num_ec_cws]
print(f"\nSTEP 2: GET ALPHA GEN (EC) POLY:\n{gen_poly_alpha}")


# STEP 3: MULTIPLY int_msg_poly BY (0,n) WHERE
#  n IS num_ec_cws TO HAVE LARGER X EXPONENTS FOR DIVISION.
msg_poly_int_divisible = []
mult_term = (0,num_ec_cws)  # term to multiply poly by
for i, e in msg_poly_int:  # i means int notation
  new_i = i + mult_term[0]  # unnecessary, included to hopefully clarify
  new_e = e + mult_term[1]
  new_term = (new_i, new_e)
  msg_poly_int_divisible.append(new_term)
msg_poly_int = msg_poly_int_divisible
print(f"\nSTEP 3: MULTIPLY msg_poly_int BY (0,num_ec_cws):\n{msg_poly_int}")


# STEP 4: MULTIPLY GEN POLY TO MATCH LEAD TERM
# TO msg_poly_int
x_exp_mult = msg_poly_int[0][1] - gen_poly_alpha[0][1]
gen_poly_alpha_mult = []
for a,e in gen_poly_alpha:
  new_e = x_exp_mult + e
  gen_poly_alpha_mult.append((a, new_e))
gen_poly_alpha = gen_poly_alpha_mult
print(f"\nSTEP 4: MULTIPLY gen_poly_alpha BY x**n SO LEAD TERM MATCHES LEAD TERM OF msg_poly_int:\n{gen_poly_alpha}")


# STEP 1a: MULTIPLY gen_poly_alpha by lead
# term of msg_poly_int
lead_term_msg_poly_int = msg_poly_int[0]
i, e = lead_term_msg_poly_int
a = ANTILOG_TABLE[i]
lead_term_msg_poly_alpha = (a,0)

result_1a_alpha = []
for a,e in gen_poly_alpha:
  new_a = a + lead_term_msg_poly_alpha[0]
  if new_a > 255:
    new_a = new_a % 255
  result_1a_alpha.append((new_a, e))

result_1a_int = []
for a,e in result_1a_alpha:
  i = LOG_TABLE[a]
  result_1a_int.append((i,e))
print(f"\nSTEP 1a: MULTIPLY gen_poly_alpha by lead term of msg_gen_poly_alpha:\n{result_1a_int}")


# STEP 1b: XOR
result_1b_int = []

for j in range(len(msg_poly_int)):
  i, e = msg_poly_int[j]
  if j > len(result_1a_int)-1:
    i2 = 0
    e2 = e
  else:
    i2, e2 = result_1a_int[j]
  new_i = i^i2
  result_1b_int.append((new_i, e))
result_1b_int = result_1b_int[1:]
print(f"\nSTEP 1b: XOR result 1a poly with msg_poly_int:\n{result_1b_int}")


# STEP 2a multiply gen_poly_alpha by lead term of result_1b_int
lead_term_result_1b_int = result_1b_int[0]
i, e = lead_term_result_1b_int
a = ANTILOG_TABLE[i]
lead_term_result_1b_alpha = (a,e)
print(f"\nlead term result 1b:\n{lead_term_result_1b_alpha}")
print(f"gen poly:\n{gen_poly_alpha}")
result_2a_alpha = []
for a2,e2 in gen_poly_alpha:
  new_a = a2 + a
  if new_a > 255:
    new_a = new_a % 255
  result_2a_alpha.append((new_a, e2))

result_2a_int = []
for a,e in result_2a_alpha:
  i = LOG_TABLE[a]
  result_2a_int.append((i,e))
print(f"\nSTEP 2a: MULTIPLY gen_poly_alpha by lead term of result_1b_alpha:\n{result_2a_int}")

print(len(gen_poly_alpha))
