from lsm.aoc import get_input

calories = []
total = 0

for line in get_input().splitlines():
	if line:
		total += int(line)
	else:
		calories.append(total)
		total = 0

calories = sorted(calories)
print('part 1:', calories[-1])
print('part 2:', sum(calories[-3:]))
