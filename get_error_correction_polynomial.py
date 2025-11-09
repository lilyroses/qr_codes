# get_error_correction_polynomial.py
from error_correction_polynomials import ERROR_CORRECTION_POLYNOMIALS
from create_generator_polynomials import format_polynomial_readable



def get_error_correction_polynomial(num_cws):
  p = ERROR_CORRECTION_POLYNOMIALS[num_cws]
  fp = format_polynomial_readable(p)
  print(f"\nERROR CORRECTION POLYNOMIAL FOR {num_cws} CODEWORDS:\n")
  print(fp)
  print("\n")


if __name__ == "__main__":
  num_cws = int(input("\nNumber of codewords: "))
  get_error_correction_polynomial(num_cws)
