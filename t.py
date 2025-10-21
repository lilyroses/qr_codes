import csv
from pprint import pprint


INF = "error_correction_codewords.csv"
with open(INF, "r") as f:
  lines = [line.strip() for line in f.readlines()]


DATA_CODEWORDS_PER_MATRIX = {}

for line in lines[1:]:
  items = line.split("\t")
  version, ec_lvl = items[0].split("-")
  version = int(version)

  if version not in DATA_CODEWORDS_PER_MATRIX:
    DATA_CODEWORDS_PER_MATRIX[version] = {} 
  data_cw = int(items[1])
  DATA_CODEWORDS_PER_MATRIX[version][ec_lvl] = data_cw

pprint(DATA_CODEWORDS_PER_MATRIX)
