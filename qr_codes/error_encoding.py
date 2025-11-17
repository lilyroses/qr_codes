# error_encoding.py
from encode import encode
from error_correction_polynomials import ERROR_CORRECTION_POLYNOMIALS as ECP
from data import (
  ANTILOG_TABLE,
  LOG_TABLE,
  NUM_CODEWORDS
)


class Polynomial:
  self.num_times_divided = 0

  def __init__(self, terms, notation):
    self.terms = terms
    self.notation = notation


  def get_alpha_notation(self):
    if self.notation == "int":
    alpha_terms = []
      for i, x in poly:
        alpha = ANTILOG_TABLE[i]
        alpha_terms.append((alpha, x))
    alpha_poly = Polynomial(alpha_terms)
    return alpha_poly


ec_lvl = "M"
version = 1
msg = "HELLO WORLD"
data_cws = encode(msg, ec_lvl)

num_ec_cws = NUM_CODEWORDS[version][ec_lvl]["total_ec_cws"]


coefs = [int(cw,2) for cw in data_cws]
x_exps = list(range(len(coefs)-1,-1,-1))
int_msg_poly = tuple(zip(coefs, x_exps))
print(f"\nSTEP 1: GET INT MSG POLY:\n{int_msg_poly}")


alpha_gen_poly = ECP[num_ec_cws]
print(f"\nSTEP 2: GET ALPHA GEN (EC) POLY:\n{alpha_gen_poly}")


new_int_msg_poly = multiply_polynomial(int_msg_poly, (0,num_ec_cws))
print(f"\nSTEP 3: MULTIPLY int_msg_poly BY (0,num_ec_cws):\n{new_int_msg_poly}")


x_exp_mult = new_int_msg_poly[0][1] - alpha_gen_poly[0][1]
new_alpha_gen_poly = multiply_polynomial(alpha_gen_poly, (0,x_exp_mult))
print(f"\nSTEP 4: MULTIPLY alpha_gen_poly BY (0,n) TO MAKE LEAD TERM MATCH int_msg_poly:\n{new_alpha_gen_poly}")


int_msg_poly_lead_term = int_msg_poly[0][0]
alpha_msg_poly_lead_term = ANTILOG_TABLE[int_msg_poly_lead_term]
alpha_result_poly = multiply_polynomial(new_alpha_gen_poly, (alpha_msg_poly_lead_term,0))
print(f"\nSTEP 5: MULTIPLY new_alpha_gen_poly BY LEAD TERM OF alpha_msg_poly:\n{alpha_result_poly}")


int_result_poly = get_int_poly(alpha_result_poly)
print(f"\nSTEP 6: GET INT RESULT POLY:\n{int_result_poly}")


int_xor_poly = xor_polynomials(int_result_poly, int_msg_poly)
print(f"\nSTEP 7: XOR INT RESULT POLY WITH INT MSG POLY:\n{int_xor_poly}")

