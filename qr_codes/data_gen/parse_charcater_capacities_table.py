INF = "character_capacities_table.txt"

with open(INF, "r") as f:
    lines = [line.strip() for line in f.readlines()]


char_caps = {}

for i in range(1, len(lines[1:]), 4):
    ec_levels = lines[i:i+4]

    for i, line in enumerate(ec_levels):
        items = line.split("\t")
        if i == 0:
            version = int(items[0])
            char_caps[version] = {}
            items = items[1:]

        ec_lvl = items[0]
        vals = [int(n) for n in items[1:-1]]

        char_caps[version][ec_lvl] = {}
        char_caps[version][ec_lvl]["NUMERIC"] = vals[0]
        char_caps[version][ec_lvl]["ALPHANUMERIC"] = vals[1]
        char_caps[version][ec_lvl]["BYTE"] = vals[2]


s = f"CHARACTER_CAPACITIES = {{"
for version, data in char_caps.items():
    s += f"\n\t{version}: {{"
    for ec_lvl, info in data.items():
        s += f"\n\t\t\"{ec_lvl}\": {{"
        for mode, val in info.items():
            if mode == "BYTE":
                s += f"\"{mode}\": {val}"
            else:
                s += f"\"{mode}\": {val}, "
        s += f"}},"
    s += f"\n\t}},"
s += "\n}"

with open("CHARACTER_CAPACITIES_DICT.py", "w") as f:
    f.write(s)