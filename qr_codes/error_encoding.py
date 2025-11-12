# error_encoding.py
from encode import encode, convert_cws_to_ints
from error_correction_polynomials import ERROR_CORRECTION_POLYNOMIALS
from data import NUM_CODEWORDS


def get_message_polynomial(data_cws):
    polynomial_coefficients = convert_cws_to_ints(data_cws)
    x_exps = sorted(list(range(0, len(data_cws))), reverse=True)
    msg_polynomial = []
    for i in range(len(polynomial_coefficients)):
        term = (polynomial_coefficients[i], x_exps[i])
        msg_polynomial.append(term)
    return msg_polynomial


def get_num_error_correction_codewords(version, ec_level):
    num_ec_cws = NUM_CODEWORDS[version][ec_level]["total_ec_cws"]
    return num_ec_cws


def get_generator_polynomial(num_ec_cws):
    generator_polynomial = ERROR_CORRECTION_POLYNOMIALS[num_ec_cws]
    return generator_polynomial


def increase_lead_term_exponent(polynomial, n):
    """"""
    terms = []
    for a, x in polynomial:
        x += n
        term = (a,x)
        terms.append(term)
    return terms



cws = ['00100000', '01011011', '00001011', '01111000', '11010001', '01110010', '11011100', '01001101', '01000011', '01000000', '11101100', '00010001', '11101100', '00010001', '11101100', '00010001']
version = 1
ec_level = "M"

msg_poly = get_message_polynomial(cws)
num_ec_cws = get_num_error_correction_codewords(version, ec_level)
generator_poly = get_generator_polynomial(num_ec_cws)
increased_msg_poly = increase_lead_term_exponent(msg_poly, num_ec_cws)
msg_lead_x_exp = increased_msg_poly[0][1]
gen_lead_x_exp = generator_poly[0][1]
n = msg_lead_x_exp - gen_lead_x_exp
increased_generator_poly = increase_lead_term_exponent(generator_poly, n)
print(increased_generator_poly)