from lsm.aoc import get_input
from string import ascii_lowercase

lines = get_input('input', day=3, year=2022).splitlines()

priority = ascii_lowercase + ascii_lowercase.upper()
total = 0

for line in lines:
	parts = (line[:len(line) // 2], line[len(line) // 2:])
	common = list(set(parts[0]).intersection(set(parts[1])))[0]

	total += priority.index(common) + 1

print('PART 1:', total)


total = 0
for i in range(0, len(lines), 3):
	group = [set(line) for line in lines[i:i+3]]
	common = group[0]

	for line in group:
		common = common.intersection(line)

	common = list(common)[0]
	total += priority.index(common) + 1


print('PART 1:', total)