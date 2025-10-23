INF = "table_codewords_by_version_ec_level.csv"
with open(INF) as f:
  rows = [line.strip() for line in f.readlines()]

print(len(rows))

fixed = []
for row in rows:
  items = row.split("\t")
  n = 8 - len(items)
  for i in range(n):
    items.append("0")
  frow = "\t".join(items)
  fixed.append(frow)

OUTF = "table_codewords_by_version_ec_level2.csv"

with open(OUTF, "w") as f:
  for frow in fixed[:-1]:
    f.write(f"{frow}\n")
  f.write(fixed[-1])


