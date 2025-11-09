from collections import defaultdict as dd
from ascii_table import create_ascii_table
from pprint import pprint


codewords_by_version = dd(dict)
CWS = dd(dict)


with open("table_codewords_by_version_ec_level.csv", "r") as f:
  rows = [line.strip() for line in f.readlines()]

for row in rows[1:]:
  items = row.split("\t")
  VERSION = int(items[0])
  EC_LEVEL = items[1]
  TOTAL_DATA_CWS = int(items[2])
  EC_CWS_PER_BLOCK = int(items[3])
  GROUP_1_BLOCKS = int(items[4])
  DATA_CWS_PER_GROUP_1_BLOCK = int(items[5])
  GROUP_2_BLOCKS = int(items[6])
  DATA_CWS_PER_GROUP_2_BLOCK = int(items[7])

  CWS[VERSION][EC_LEVEL] = {}

  CWS[VERSION][EC_LEVEL]["G1"] = {}
  CWS[VERSION][EC_LEVEL]["G1"]["BLOCKS"] = GROUP_1_BLOCKS
  CWS[VERSION][EC_LEVEL]["G1"]["DATA_CWS"] = DATA_CWS_PER_GROUP_1_BLOCK
  CWS[VERSION][EC_LEVEL]["G1"]["EC_CWS"] = EC_CWS_PER_BLOCK

  CWS[VERSION][EC_LEVEL]["G2"] = {}
  CWS[VERSION][EC_LEVEL]["G2"]["BLOCKS"] = GROUP_2_BLOCKS
  CWS[VERSION][EC_LEVEL]["G2"]["DATA_CWS"] = DATA_CWS_PER_GROUP_2_BLOCK
  if CWS[VERSION][EC_LEVEL]["G2"]["BLOCKS"] > 0:
    CWS[VERSION][EC_LEVEL]["G2"]["EC_CWS"] = EC_CWS_PER_BLOCK
  else:
    CWS[VERSION][EC_LEVEL]["G2"]["EC_CWS"] = 0

  codewords_by_version[VERSION][EC_LEVEL] = {}

  codewords_by_version[VERSION][EC_LEVEL]["TOTAL_DATA_CWS"] = TOTAL_DATA_CWS
  codewords_by_version[VERSION][EC_LEVEL]["EC_CWS_PER_BLOCK"] = EC_CWS_PER_BLOCK

  codewords_by_version[VERSION][EC_LEVEL]["GROUP_1_BLOCKS"] = GROUP_1_BLOCKS
  codewords_by_version[VERSION][EC_LEVEL]["DATA_CWS_PER_GROUP_1_BLOCK"] = DATA_CWS_PER_GROUP_1_BLOCK

  codewords_by_version[VERSION][EC_LEVEL]["GROUP_2_BLOCKS"] = GROUP_2_BLOCKS
  codewords_by_version[VERSION][EC_LEVEL]["DATA_CWS_PER_GROUP_2_BLOCK"] = DATA_CWS_PER_GROUP_2_BLOCK


pprint(codewords_by_version)
#pprint(CWS)

s = "CODEWORDS_BY_VERSION = {"
for version, e in codewords_by_version.items():
  s += f"\t{version}: {{"

with open("num_codewords_by_version_ec_level.py", "w") as f:
  pass

print("codewords_by_version = {")
for version, e in codewords_by_version.items():
  print(f"\t{version}: {{")
  for ec_lvl, info in e.items():
    print(f"\t\t{ec_level}: {info}")
