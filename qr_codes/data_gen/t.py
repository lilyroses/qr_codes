from CHARACTER_CAPACITIES import CHARACTER_CAPACITIES as CAPS

max_chars = 0

for v in range(1,41):
  for ec in list("LMQH"):
    max_chars = max(max_chars, CAPS[v][ec]["BYTE"])

print(max_chars)

