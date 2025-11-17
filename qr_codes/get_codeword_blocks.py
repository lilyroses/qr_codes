from data import (
  CHARACTER_COUNT_INDICATOR_LENGTHS,
  NUM_CODEWORDS
)


INF = "t.txt"
with open(INF,"r") as f:
  cws = [line.strip() for line in f.readlines()]
ec_lvl = "Q"
version = 5


def get_codeword_blocks(data_codewords, ec_lvl, version):
  g1_blocks = NUM_CODEWORDS[version][ec_lvl]["g1_blocks"]
  g2_blocks = NUM_CODEWORDS[version][ec_lvl]["g2_blocks"]
  g1_block_cws = NUM_CODEWORDS[version][ec_lvl]["data_cws_per_g1_block"]
  g2_block_cws = NUM_CODEWORDS[version][ec_lvl]["data_cws_per_g2_block"]
  total_data_cws = NUM_CODEWORDS[version][ec_lvl]["total_data_cws"]

  assert len(data_codewords) == total_data_cws, "Invalid number of data codewords (expected: {total_data_cws}, received: {len(data_codewords}"

  i = 0
  group_1_blocks = []

  for x in range(g1_blocks):
    j = i + g1_block_cws
    group_1_blocks.append(data_codewords[i:j])
    i = j

  group_2_blocks = []

  for x in range(g2_blocks):
    j = i + g2_block_cws
    group_2_blocks.append(data_codewords[i:j])
    i = j
  groups = [group_1_blocks, group_2_blocks]
  return groups


groups = get_codeword_blocks(cws, ec_lvl, version)
for i, group in enumerate(groups,1):
  print(f"\nGROUP #{i}:")
  for j, block in enumerate(group,1):
    print(f"\tBLOCK #{j}:")
    for cw in block:
      print(f"\t\t{cw}")


