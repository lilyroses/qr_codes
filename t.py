from error_correction_polynomials import error_correction_polynomials
from create_generator_polynomials import print_polynomial


def get_generator_polynomial(num_codewords:int) -> list[tuple[int]]:
  return error_correction_polynomials[num_codewords]


def get_readable_generator_polynomial(num_codewords:int) -> list[tuple[int]]:
  print(f"\nGENERATOR POLYNOMIAL FOR {num_codewords} CODEWORDS:")
  print(print_polynomial(error_correction_polynomials[num_codewords]))


if __name__ == "__main__":
  get_readable_generator_polynomial(8)
