INF = "num_codewords_by_version_ec_level.txt"
OUTF = "NUM_CODEWORDS.py"
with open(INF, "r") as f:
  lines = [line.strip() for line in f.readlines()]

headers = [
  "version",
  "error_correction_level",
  "total_data_cws",
  "total_ec_cws",
  "ec_cws_per_block",
  "g1_blocks",
  "data_cws_per_g1_block",
  "g2_blocks",
  "data_cws_per_g2_block"
]

NUM_CODEWORDS = {}

for line in lines[1:]:
  row = line.split("\t")[:-1]
  items = row[0].split("-")
  version = int(items[0])
  ec_lvl = items[1]
  total_data_cws = int(row[1])
  ec_cws_per_block = int(row[2])
  g1_blocks = int(row[3])
  data_cws_per_g1_block = int(row[4])
  if row[5]:
    g2_blocks = int(row[5])
    data_cws_per_g2_block = int(row[6])
  else:
    g2_blocks = 0
    data_cws_per_g2_block = 0
  total_ec_cws = (g1_blocks + g2_blocks) * ec_cws_per_block

  vals = [
    version, ec_lvl, total_data_cws,
    total_ec_cws, ec_cws_per_block,
    g1_blocks, data_cws_per_g1_block,
    g2_blocks, data_cws_per_g2_block
  ]

  if version not in NUM_CODEWORDS:
    NUM_CODEWORDS[version] = {}
  else:
    NUM_CODEWORDS[version] [ec_lvl] = {}
  d = dict(zip(headers[2:], vals[2:]))

  NUM_CODEWORDS[version][ec_lvl] = d

from pprint_to_file import pprint_to_file
pprint_to_file(NUM_CODEWORDS, "NUM_CODEWORDS", OUTF)
