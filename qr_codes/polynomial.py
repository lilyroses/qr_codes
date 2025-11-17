from data import (
  ANTILOG_TABLE,
  LOG_TABLE
)


class Term:
  def __init__(self, n, e):
    self.n = n
    self.e = e

class Alpha(Term):
  notation = "alpha"
  def __init__(self, n, e):
    super().__init__(self, n, e)
    self.n = n
    self.e = e
  def get_int_notation(self):
    i = LOG_TABLE[self.n]
    int_term = Int(i,e)
    return int_term

class Int(Term):
  notation = "int"
  def __init__(self, n, e):
    super().__init__(self, n, e)
    self.n = n
    self.e = e
  def get_alpha_notation(self):
    a = LOG_TABLE[self.n]
    alpha_term = Int(a,e)
    return alpha_term



class Polynomial:
  def __init__(self, terms, notation):
    self.terms = terms
    self.notation = notation
    self.num_times_divided = 0

  def get_lead_term(self):
    return self.terms[0]

  def convert_to_alpha(self):
    if self.notation == "alpha":
      return self.terms
    alpha_terms = []
    for i, x in self.terms:
      a = ANTILOG_TABLE[i]
      alpha_terms.append((a,x))
    alpha_notation = "alpha"
    return Polynomial(alpha_terms, alpha_notation)

  def convert_to_int(self):
    if self.notation.lower() == "int_notation":
      return self.terms
    self.int_terms = []
    for a, x in self.terms:
      i = LOG_TABLE[a]
      self.int_terms.append((i,x))
    self.terms = self.int_terms
    self.notation = "int_notation"


int_terms = [(32,2),(91,1),(50,0)]
poly = Polynomial(int_terms, "int_notation")

poly.convert_to_int()
print("\nterms:",poly.terms)
print("notation:", poly.notation)

poly.convert_to_alpha()
print("\npoly converted to alpha terms", poly.terms)
print("notation:", poly.notation)

poly.convert_to_alpha()
print("\npoly converted to alpha terms", poly.terms)
print("notation:", poly.notation)

poly.convert_to_int()
print("\npoly converted to int terms:", poly.terms)
print("notation:", poly.notation)

print("lead term:", poly.get_lead_term())


term = Alpha(5,25)
print(term.n, term.e)
